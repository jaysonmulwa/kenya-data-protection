# Install

Pick your agent below. Not listed? Most agents read [`AGENTS.md`](AGENTS.md): copy it into your project, or ask your agent to install [`skills/kenya-data-protection/`](skills/kenya-data-protection/) as a skill.

**Two ways it runs:**

- **As a skill** (Claude Code, Codex, Copilot CLI, Gemini CLI, Pi and the other plugin hosts): the full version, with the complete law reference and the codebase scanner. It loads only when a task touches Kenyan personal data.
- **As a rules file** (Cursor, Windsurf, Cline, Kiro and the other rules hosts): [`AGENTS.md`](AGENTS.md), a compact version with every key rule, figure and deadline. It links to the full reference on GitHub for anything more.

**Tested:** the Claude Code install below was tested end to end: it installs, triggers on its own for a plain question, and runs the scanner on a codebase. The other hosts use each host's documented plugin or rules format, following [ponytail](https://github.com/DietrichGebert/ponytail)'s working setup, but haven't been tested here yet. If one doesn't work, please [open an issue](https://github.com/jaysonmulwa/kenya-data-protection/issues).

The scanner needs Python 3 on your PATH. Without it, the skill does the same search by hand.

## Claude Code

```
/plugin marketplace add jaysonmulwa/kenya-data-protection
```
```
/plugin install kenya-data-protection@kenya-data-protection-marketplace
```

Send them as two separate prompts. In the Claude desktop app's Code tab, type the same commands, or use **+** → **Plugins** → **Add plugin**. From a terminal: `claude plugin marketplace add jaysonmulwa/kenya-data-protection`, then `claude plugin install kenya-data-protection@kenya-data-protection-marketplace`.

Claude then uses it whenever a request matches. Run it directly with `/kenya-data-protection:kenya-data-protection`.

## Claude.ai

1. Turn on **Code execution and file creation** under Settings › Capabilities (Pro, Max, Team or Enterprise plans).
2. Zip the [`skills/kenya-data-protection`](skills/kenya-data-protection/) folder.
3. Upload the zip at **Customize › Skills**.

## Codex

```bash
codex plugin marketplace add jaysonmulwa/kenya-data-protection
codex plugin add kenya-data-protection@kenya-data-protection
```

Covers the Codex desktop app too; restart it after installing.

## GitHub Copilot CLI

```bash
copilot plugin marketplace add jaysonmulwa/kenya-data-protection
copilot plugin install kenya-data-protection@kenya-data-protection
```

Or inside a session: `/plugin marketplace add jaysonmulwa/kenya-data-protection`, then `/plugin install kenya-data-protection@kenya-data-protection`.

## Gemini CLI

```bash
gemini extensions install https://github.com/jaysonmulwa/kenya-data-protection
```

Loads [`AGENTS.md`](AGENTS.md) as context and adds a `/kenya-data-protection <what to check>` command.

**Qwen Code** installs the same extension: `qwen extensions install jaysonmulwa/kenya-data-protection`.

**Antigravity CLI:** `agy plugin install https://github.com/jaysonmulwa/kenya-data-protection`. To use it as a rule instead, copy [`.agents/rules/kenya-data-protection.md`](.agents/rules/kenya-data-protection.md) into your project's `.agents/rules/`.

## Pi

```bash
pi install git:github.com/jaysonmulwa/kenya-data-protection
```

## Kimi Code

Run `/plugins install https://github.com/jaysonmulwa/kenya-data-protection`, then `/reload` or start a new session.

## Devin CLI

```bash
devin plugins install jaysonmulwa/kenya-data-protection
```

The skill is available as `/kenya-data-protection:kenya-data-protection`.

## Grok Build

```bash
grok plugin install jaysonmulwa/kenya-data-protection --trust
```

Plugins are off by default: enable it under `/plugins`, or add it to `enabled` under `[plugins]` in `~/.grok/config.toml`. Then start a new session.

## Hermes Agent

```bash
hermes plugins install jaysonmulwa/kenya-data-protection --enable
```

Restart Hermes after installing.

## Qoder

Qoder reads [`AGENTS.md`](AGENTS.md) from the project root. For a per-project rule, copy [`.qoder/rules/kenya-data-protection.md`](.qoder/rules/kenya-data-protection.md) into your project's `.qoder/rules/`. For the skill, install the plugin: `qodercli plugins install <path-to-this-repo>`.

## Goose

```bash
goose plugin install https://github.com/jaysonmulwa/kenya-data-protection.git
```

## OpenClaw

Copy [`.openclaw/skills/kenya-data-protection`](.openclaw/skills/) into `~/.openclaw/skills/`.

## OpenCode

OpenCode reads [`AGENTS.md`](AGENTS.md) from the project root. Copy it into your project, and copy [`.opencode/command/kenya-data-protection.md`](.opencode/command/kenya-data-protection.md) into your project's `.opencode/command/` for a `/kenya-data-protection` command.

## Skills CLI

The [skills CLI](https://skills.sh) copies the skill into many agents' skills folders:

```bash
npx skills add jaysonmulwa/kenya-data-protection
```

Choose the agent with `--agent`, and add `--global` to install it for your user instead of the project.

## Rules-file agents

Copy the matching file into your project:

| Agent | File | Where it goes |
|---|---|---|
| Cursor | [`.cursor/rules/kenya-data-protection.mdc`](.cursor/rules/kenya-data-protection.mdc) | `.cursor/rules/` (applied when relevant) |
| Windsurf | [`.windsurf/rules/kenya-data-protection.md`](.windsurf/rules/kenya-data-protection.md) | `.windsurf/rules/` (applied when relevant) |
| Cline | [`.clinerules/kenya-data-protection.md`](.clinerules/kenya-data-protection.md) | `.clinerules/` |
| Kiro | [`.kiro/steering/kenya-data-protection.md`](.kiro/steering/kenya-data-protection.md) | `.kiro/steering/`, or `~/.kiro/steering/` for every project. Change `inclusion: always` to `manual` to load it only when you reference it. |
| GitHub Copilot Chat (VS Code, JetBrains, Visual Studio) | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | `.github/` (merge with any existing file) |
| Antigravity | [`.agents/rules/kenya-data-protection.md`](.agents/rules/kenya-data-protection.md) | `.agents/rules/` |
| Aider, Zed, Amp, Jules, Junie, CodeWhale | [`AGENTS.md`](AGENTS.md) | project root (Junie: point Settings › Tools › Junie › Guidelines Path at it) |

Every rules file is a copy of [`AGENTS.md`](AGENTS.md) with that host's header, generated by [`scripts/sync_harness_files.py`](scripts/sync_harness_files.py).

## Uninstall

| Host | Command |
|------|---------|
| Claude Code | `/plugin uninstall kenya-data-protection@kenya-data-protection-marketplace` |
| Codex | `codex plugin remove kenya-data-protection` |
| Copilot CLI | `copilot plugin uninstall kenya-data-protection` |
| Gemini CLI | `gemini extensions uninstall kenya-data-protection` |
| Pi | `pi uninstall kenya-data-protection` |
| Devin CLI | `devin plugins remove kenya-data-protection` |
| Grok Build | `grok plugin uninstall kenya-data-protection` |
| Skills CLI | `npx skills remove kenya-data-protection` (same `--agent` / `--global` flags as the install) |
| Rules files, OpenClaw, OpenCode | Delete the copied file or folder |
