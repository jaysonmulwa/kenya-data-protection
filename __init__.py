"""Hermes Agent plugin: registers the bundled Kenya data protection skill."""

from pathlib import Path
from typing import Any

SKILLS_DIR = Path(__file__).resolve().parent / "skills"


def register(ctx: Any) -> None:
    for child in sorted(SKILLS_DIR.iterdir()):
        if (child / "SKILL.md").exists():
            ctx.register_skill(child.name, child / "SKILL.md")
