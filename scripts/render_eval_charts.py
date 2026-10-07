"""Draw the README's eval charts from evals/results.json.

Writes a light and a dark SVG for each chart into assets/, for a
<picture> element that follows the reader's GitHub theme. The colours are
the first three slots of a categorical palette checked for colour-blind
separation in both modes; the README's tables are the text alternative.

Usage: python scripts/render_eval_charts.py
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SETUPS = [("with_skill", "With skill"), ("without_skill", "Plain model"), ("with_web", "Plain model + ODPC web")]
QUESTIONS = {
    "registration-12-staff-under-5m": "Bakery: must it register?",
    "access-and-erasure-deadlines": "Access and deletion deadlines",
    "breach-digital-lender": "Digital lender data breach",
    "telemedicine-hosting-abroad": "Telemedicine hosted abroad",
    "wedding-marketing-sensitive-data": "Marketing with sensitive data",
    "school-parent-app-repo-check": "School app code check",
    "exempt-startup-still-needs-policy": "Exempt startup's paperwork",
    "mall-cctv-facial-recognition": "Mall facial recognition",
}
THEMES = {
    "light": {"surface": "#fcfcfb", "text": "#0b0b0b", "muted": "#52514e", "grid": "#e4e3df",
              "series": ["#2a78d6", "#eb6834", "#1baf7a"]},
    "dark": {"surface": "#1a1a19", "text": "#ffffff", "muted": "#c3c2b7", "grid": "#3a3a37",
             "series": ["#3987e5", "#d95926", "#199e70"]},
}
FONT = "font-family=\"-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif\""
W = 760


def bar(x, y, w, h, fill):
    """A bar anchored at the baseline (square left) with a 4px rounded data end."""
    r = min(4, h / 2, w)
    return (f'<path d="M{x},{y} h{w - r:.1f} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r:.1f} '
            f'a{r},{r} 0 0 1 {-r},{r} h{-(w - r):.1f} z" fill="{fill}"/>')


def frame(t, height, title, subtitle, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '
            f'viewBox="0 0 {W} {height}" role="img" aria-label="{escape(title)}">\n'
            f'<rect width="{W}" height="{height}" rx="8" fill="{t["surface"]}"/>\n'
            f'<text x="24" y="34" {FONT} font-size="17" font-weight="600" fill="{t["text"]}">{escape(title)}</text>\n'
            f'<text x="24" y="56" {FONT} font-size="13" fill="{t["muted"]}">{escape(subtitle)}</text>\n'
            + body + "</svg>\n")


def grid(t, x0, width, top, bottom):
    out = []
    for pct in (0, 25, 50, 75, 100):
        x = x0 + width * pct / 100
        out.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" stroke="{t["grid"]}" stroke-width="1"/>')
        out.append(f'<text x="{x}" y="{bottom + 18}" {FONT} font-size="12" fill="{t["muted"]}" '
                   f'text-anchor="middle">{pct}%</text>')
    return "\n".join(out) + "\n"


def overall(results, t):
    x0, width, top = 210, 430, 84
    rows = []
    for i, (key, label) in enumerate(SETUPS):
        passed = sum(q[key]["passed"] for q in results.values())
        total = sum(q[key]["total"] for q in results.values())
        y = top + i * 44
        w = width * passed / total
        rows.append(f'<text x="{x0 - 14}" y="{y + 16}" {FONT} font-size="14" fill="{t["text"]}" '
                    f'text-anchor="end">{escape(label)}</text>')
        rows.append(bar(x0, y + 2, w, 20, t["series"][i]))
        rows.append(f'<text x="{x0 + w + 8}" y="{y + 17}" {FONT} font-size="14" font-weight="600" '
                    f'fill="{t["text"]}">{passed / total:.1%}</text>')
    bottom = top + len(SETUPS) * 44
    body = grid(t, x0, width, top - 6, bottom) + "\n".join(rows) + "\n"
    return frame(t, bottom + 40, "Checks passed",
                 f"{total} checks: 8 questions × 3 runs, scored by a blind grader. Claude Opus 5.5.", body)


def by_question(results, t):
    x0, width, top, bar_h, gap, group = 250, 440, 108, 8, 2, 40
    legend = []
    lx = 24
    for i, (_, label) in enumerate(SETUPS):
        legend.append(f'<rect x="{lx}" y="72" width="12" height="12" rx="2" fill="{t["series"][i]}"/>')
        legend.append(f'<text x="{lx + 18}" y="82" {FONT} font-size="13" fill="{t["text"]}">{escape(label)}</text>')
        lx += 36 + len(label) * 7.2
    rows = []
    for g, (name, label) in enumerate(QUESTIONS.items()):
        y = top + g * group
        rows.append(f'<text x="{x0 - 14}" y="{y + 18}" {FONT} font-size="13" fill="{t["text"]}" '
                    f'text-anchor="end">{escape(label)}</text>')
        for i, (key, _) in enumerate(SETUPS):
            r = results[name][key]
            rows.append(bar(x0, y + i * (bar_h + gap), width * r["passed"] / r["total"], bar_h, t["series"][i]))
    bottom = top + len(QUESTIONS) * group - 8
    body = "\n".join(legend) + "\n" + grid(t, x0, width, top - 6, bottom) + "\n".join(rows) + "\n"
    return frame(t, bottom + 40, "Checks passed, by question",
                 "Share of each question's checks passed across 3 runs. Exact counts are in the table below.", body)


def main():
    results = json.loads((ROOT / "evals" / "results.json").read_text(encoding="utf-8"))
    (ROOT / "assets").mkdir(exist_ok=True)
    for mode, t in THEMES.items():
        for name, draw in (("eval-overall", overall), ("eval-by-question", by_question)):
            (ROOT / "assets" / f"{name}-{mode}.svg").write_text(draw(results, t), encoding="utf-8", newline="\n")
    print("wrote assets/eval-*.svg")


if __name__ == "__main__":
    main()
