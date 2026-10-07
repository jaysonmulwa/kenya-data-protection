"""Write the per-harness copies of this skill from their two sources.

- AGENTS.md is the compact, self-contained ruleset. Each rule-file harness
  (Cursor, Windsurf, Cline, Kiro, Qoder, Antigravity, Copilot) gets a copy of
  its body, with that host's frontmatter.
- skills/kenya-data-protection/ is the full skill. OpenClaw gets a copy whose
  description is one line under 160 characters, as ClawHub requires.

It also checks that every manifest carries the same version.

Usage:
    python scripts/sync_harness_files.py           # rewrite the copies
    python scripts/sync_harness_files.py --check   # exit 1 if anything drifted (CI)
"""
import json
import re
import shutil
import sys
import tempfile
from filecmp import dircmp
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "kenya-data-protection"
SKILL = ROOT / "skills" / NAME
SHORT_DESCRIPTION = ("Check a product, codebase or data practice against Kenya's Data Protection "
                     "Act 2019 and ODPC rules, and say what to fix.")

# path -> frontmatter placed above the AGENTS.md body ("" for none).
RULE_COPIES = {
    f".cursor/rules/{NAME}.mdc":
        f"---\ndescription: {SHORT_DESCRIPTION}\nglobs:\nalwaysApply: false\n---\n\n",
    f".windsurf/rules/{NAME}.md":
        f"---\ntrigger: model_decision\ndescription: {SHORT_DESCRIPTION}\n---\n\n",
    f".kiro/steering/{NAME}.md":
        "---\ntitle: Kenya data protection (ODPC) check\ninclusion: always\n---\n\n",
    f".clinerules/{NAME}.md": "",
    f".qoder/rules/{NAME}.md": "",
    f".agents/rules/{NAME}.md": "",
    ".github/copilot-instructions.md": "",
}

# Files whose "version" must match .claude-plugin/plugin.json.
VERSIONED = [".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".devin-plugin/plugin.json",
             ".github/plugin/plugin.json", ".qoder-plugin/plugin.json", "gemini-extension.json",
             "package.json"]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


def openclaw_skill(out):
    """Copy the skill to out/, swapping in the one-line description."""
    shutil.copytree(SKILL, out, ignore=shutil.ignore_patterns("__pycache__"))
    text = (out / "SKILL.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    head, body = re.match(r"^(---\n.*?\n---\n)(.*)$", text, re.S).groups()
    head = re.sub(r"^description: .*$", f"description: {SHORT_DESCRIPTION}", head, flags=re.M)
    head = head.replace("\n---\n", f"\nhomepage: https://github.com/jaysonmulwa/{NAME}\nlicense: MIT\n---\n", 1)
    (out / "SKILL.md").write_text(head + body, encoding="utf-8", newline="\n")


def same_tree(a, b):
    d = dircmp(a, b, ignore=["__pycache__"])
    return (not d.left_only and not d.right_only and not d.diff_files and not d.funny_files
            and all(same_tree(a / s, b / s) for s in d.common_dirs))


def main(check):
    problems = []
    body = read("AGENTS.md").strip() + "\n"
    for rel, front in RULE_COPIES.items():
        want = front + body
        path = ROOT / rel
        if check:
            if not path.exists() or read(rel) != want:
                problems.append(f"{rel} is out of date with AGENTS.md")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(want, encoding="utf-8", newline="\n")

    claw = ROOT / ".openclaw" / "skills" / NAME
    if check:
        with tempfile.TemporaryDirectory() as tmp:
            fresh = Path(tmp) / NAME
            openclaw_skill(fresh)
            if not claw.exists() or not same_tree(fresh, claw):
                problems.append(f"{claw.relative_to(ROOT).as_posix()} is out of date with skills/{NAME}")
    else:
        shutil.rmtree(claw, ignore_errors=True)
        openclaw_skill(claw)

    versions = {rel: json.loads(read(rel)).get("version") for rel in VERSIONED}
    want = versions[VERSIONED[0]]
    problems += [f"{rel} has version {v}, expected {want}" for rel, v in versions.items() if v != want]
    yaml_version = re.search(r"^version: (.+)$", read("plugin.yaml"), re.M).group(1).strip()
    if yaml_version != want:
        problems.append(f"plugin.yaml has version {yaml_version}, expected {want}")

    for p in problems:
        print(p)
    if problems:
        print("Run: python scripts/sync_harness_files.py" if check else "")
        return 1
    print("in sync" if check else "wrote harness copies")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
