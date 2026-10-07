"""Benchmark the skill against the plain model, using headless Claude Code.

Each eval prompt runs N times in each of three setups:
- with_skill: the skill, no web;
- without_skill: the plain model, no tools at all;
- with_web: the plain model, told to research the ODPC website first. It can
  search the web but fetch pages only from odpc.go.ke.
The code-check eval also gets read-only tools on a copy of the sample app,
outside this repo, so the no-skill setups can't stumble on the skill. A blind
grader then scores every answer against the eval's expectations.

Usage:
    python evals/run_skill_benchmark.py <workspace> [--runs 3] [--jobs 8] [--model claude-opus-5-5]
    python evals/run_skill_benchmark.py <workspace> --configs with_web
    python evals/run_skill_benchmark.py <workspace> --grade-only

Writes <workspace>/eval-<id>-<name>/<config>/run-<n>/{outputs/answer.md,
timing.json, grading.json} and prints a summary. Needs the `claude` CLI.
"""
import argparse
import json
import shutil
import statistics
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "kenya-data-protection"
APP = REPO / "evals" / "files" / "acorns-parent-app"
CONFIGS = ("with_skill", "without_skill", "with_web")
ODPC_FETCH = ("WebFetch(domain:odpc.go.ke)", "WebFetch(domain:www.odpc.go.ke)")

ANSWER_ONLY = "Your final reply must be only your complete answer to the user, exactly as you would send it."
WITH_SKILL = ("Use the skill at {skill}: read its SKILL.md first and follow it, including its "
              "reference files and scripts where it says to.\n\nUser's message:\n{prompt}\n\n" + ANSWER_ONLY)
WITHOUT_SKILL = "Answer from your own knowledge.\n\nUser's message:\n{prompt}\n\n" + ANSWER_ONLY
WITH_WEB = ("Before answering, research the question on the web. Start with the website of Kenya's "
            "Office of the Data Protection Commissioner, https://www.odpc.go.ke, and use what you find "
            "there (regulations, guidance notes, forms, notices). You can search the web, but you can "
            "fetch pages only from odpc.go.ke.\n\nUser's message:\n{prompt}\n\n" + ANSWER_ONLY)
GRADER = """You are a strict grader of answers about Kenya's data protection law.

The assertions below were checked against the official texts. Treat them as the correct law.
For each one, decide whether the ANSWER clearly and correctly states it. If the answer
contradicts it, leaves it out, or hedges so a reader would not get the correct fact, it fails.
Quote the answer briefly as evidence, or say what is missing or wrong. Also list any clearly
wrong legal claims in the answer that the assertions do not cover.

Reply with only a JSON object, no code fence:
{{"expectations": [{{"text": "<assertion verbatim>", "passed": true, "evidence": "..."}}],
 "other_errors": ["..."]}}

QUESTION:
{prompt}

ASSERTIONS:
{assertions}

ANSWER:
{answer}"""


def claude(prompt, model, cwd, tools=(), add_dirs=(), allowed=None):
    """tools: what the model has. allowed: permission rules, defaulting to all of tools."""
    cmd = ["claude", "-p", "--model", model, "--output-format", "json",
           "--strict-mcp-config", "--no-session-persistence", "--tools", " ".join(tools)]
    no_web = [t for t in ("WebFetch", "WebSearch") if t not in tools]
    if no_web:
        cmd += ["--disallowedTools", " ".join(no_web)]
    allowed = tools if allowed is None else allowed
    if allowed:
        cmd += ["--allowedTools", " ".join(allowed)]
    for d in add_dirs:
        cmd += ["--add-dir", str(d)]
    for attempt in range(2):
        p = subprocess.run(cmd, cwd=cwd, input=prompt, capture_output=True, text=True,
                           encoding="utf-8", timeout=900)
        try:
            out = json.loads(p.stdout)
            if not out.get("is_error"):
                return out
        except json.JSONDecodeError:
            pass
    raise RuntimeError(f"claude failed: {p.stderr[-500:] or p.stdout[-500:]}")


def safely(fn):
    def wrapped(job, *args):
        try:
            fn(job, *args)
        except Exception as e:  # one failed run shouldn't stop the batch; rerun to fill gaps
            print(f"FAILED {job[2]}: {e}", flush=True)
    return wrapped


@safely
def run_one(job, model, app_copy):
    ev, config, run_dir = job
    if (run_dir / "outputs" / "answer.md").exists():
        return
    uses_app = bool(ev.get("files"))
    prompt = ev["prompt"].replace(APP.as_posix(), app_copy.as_posix())
    cwd = app_copy if uses_app else Path(tempfile.mkdtemp())
    if config == "with_skill":
        out = claude(WITH_SKILL.format(skill=SKILL.as_posix(), prompt=prompt), model, cwd,
                     tools=("Read", "Bash", "Glob", "Grep"), add_dirs=(SKILL,))
    elif config == "with_web":
        read = ("Read", "Glob", "Grep") if uses_app else ()
        out = claude(WITH_WEB.format(prompt=prompt), model, cwd,
                     tools=read + ("WebSearch", "WebFetch"), allowed=read + ("WebSearch",) + ODPC_FETCH)
    else:
        out = claude(WITHOUT_SKILL.format(prompt=prompt), model, cwd,
                     tools=("Read", "Glob", "Grep") if uses_app else ())
    (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
    (run_dir / "outputs" / "answer.md").write_text(out["result"], encoding="utf-8")
    u = out.get("usage", {})
    tokens = sum(u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens",
                                       "cache_read_input_tokens", "output_tokens"))
    (run_dir / "timing.json").write_text(json.dumps({
        "total_tokens": tokens, "duration_ms": out["duration_ms"],
        "total_duration_seconds": round(out["duration_ms"] / 1000, 1),
        "cost_usd": out.get("total_cost_usd")}, indent=2))
    print(f"ran   {run_dir.relative_to(run_dir.parents[2])}", flush=True)


@safely
def grade_one(job, model):
    ev, _, run_dir = job
    if (run_dir / "grading.json").exists():
        return
    answer = (run_dir / "outputs" / "answer.md").read_text(encoding="utf-8")
    out = claude(GRADER.format(prompt=ev["prompt"], answer=answer,
                               assertions="\n".join(f"- {a}" for a in ev["expectations"])),
                 model, Path(tempfile.mkdtemp()))
    text = out["result"].strip()
    g = json.loads(text[text.find("{"):text.rfind("}") + 1])
    passed = sum(e["passed"] for e in g["expectations"])
    total = len(g["expectations"])
    g["summary"] = {"passed": passed, "failed": total - passed, "total": total,
                    "pass_rate": round(passed / total, 4)}
    (run_dir / "grading.json").write_text(json.dumps(g, indent=2), encoding="utf-8")
    print(f"graded {run_dir.relative_to(run_dir.parents[2])}: {passed}/{total}", flush=True)


def summarise(jobs):
    rows, checks = {}, {}
    for ev, config, run_dir in jobs:
        if not (run_dir / "grading.json").exists():
            continue
        g = json.loads((run_dir / "grading.json").read_text(encoding="utf-8"))
        t = json.loads((run_dir / "timing.json").read_text())
        r = rows.setdefault(ev["name"], {c: [] for c in CONFIGS})[config]
        r.append((g["summary"]["passed"], g["summary"]["total"], len(g.get("other_errors", [])),
                  t["total_duration_seconds"]))
        for text, e in zip(ev["expectations"], g["expectations"]):
            checks.setdefault((ev["name"], text), {c: [] for c in CONFIGS})[config].append(e["passed"])
    cols = [c for c in CONFIGS if any(r[c] for r in rows.values())]
    print("\n| Eval | Check | " + " | ".join(cols) + " |\n|---|---|" + "---|" * len(cols))
    for (name, text), c in checks.items():
        print(f"| {name} | {text} | " + " | ".join(f"{sum(c[k])}/{len(c[k])}" for k in cols) + " |")
    def fmt(runs):
        p = sum(x[0] for x in runs); t = sum(x[1] for x in runs)
        return f"{p}/{t} ({p / t:.0%}), errors {sum(x[2] for x in runs)}" if t else "-"
    print("\n| Eval | " + " | ".join(cols) + " |\n|---|" + "---|" * len(cols))
    for name, r in rows.items():
        print(f"| {name} | " + " | ".join(fmt(r[k]) for k in cols) + " |")
    # Machine-readable copy for scripts/render_eval_charts.py.
    out = {name: {k: {"passed": sum(x[0] for x in r[k]), "total": sum(x[1] for x in r[k])} for k in cols}
           for name, r in rows.items()}
    (jobs[0][2].parents[2] / "results.json").write_text(json.dumps(out, indent=2) + "\n")
    for c in cols:
        allruns = [x for r in rows.values() for x in r[c]]
        rates = [x[0] / x[1] for x in allruns]
        print(f"{c}: {fmt(allruns)}; per-run pass rate mean {statistics.mean(rates):.1%} "
              f"sd {statistics.stdev(rates):.1%}; mean time {statistics.mean(x[3] for x in allruns):.0f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace", type=Path)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--grade-only", action="store_true")
    ap.add_argument("--configs", nargs="+", choices=CONFIGS, default=list(CONFIGS))
    a = ap.parse_args()

    evals = json.loads((REPO / "evals" / "evals.json").read_text(encoding="utf-8"))["evals"]
    jobs = [(ev, c, a.workspace / f"eval-{ev['id']}-{ev['name']}" / c / f"run-{n}")
            for ev in evals for c in a.configs for n in range(1, a.runs + 1)]
    for ev in evals:
        d = a.workspace / f"eval-{ev['id']}-{ev['name']}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "eval_metadata.json").write_text(json.dumps({
            "eval_id": ev["id"], "eval_name": ev["name"], "prompt": ev["prompt"],
            "assertions": ev["expectations"]}, indent=2))

    # The sample app is copied outside the repo, so no-skill runs can't stumble on the skill.
    app_copy = Path(tempfile.mkdtemp()) / APP.name
    shutil.copytree(APP, app_copy)
    with ThreadPoolExecutor(a.jobs) as pool:
        if not a.grade_only:
            list(pool.map(lambda j: run_one(j, a.model, app_copy), jobs))
        list(pool.map(lambda j: grade_one(j, a.model), jobs))
    summarise(jobs)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
