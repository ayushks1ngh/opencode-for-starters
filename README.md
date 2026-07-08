# opencode starter kit

Batteries-included [opencode](https://opencode.ai) configuration — drop it into any project and get a full AI development pipeline.

## What's inside

| Path | What |
|---|---|
| `opencode.json` | Default model + autoupdate |
| `tui.json` | Vim-inspired keybindings (leader: `Ctrl+O`) |
| `agent/` | 6 custom agents (see below) |
| `command/` | Custom `/build` and `/scan` commands |
| `skills/ship/` | One-command "ship it" skill |

## Agents

| Agent | Role |
|---|---|
| `tech-lead` | Orchestrator — routes work to specialists |
| `requirements-clarifier` | Turns vague ideas into specs |
| `architect-designer` | Design docs, ADRs, diagrams — zero code |
| `implementation-specialist` | Writes code, no architectural drift |
| `test-automation-engineer` | Writes & runs tests |
| `big-pickle-simple-tasks` | Breaks big work into small steps |

## Usage

### Per-project (clone into your repo)

```bash
git clone <this-repo-url> .opencode
# opencode will auto-detect .opencode/ in project root
```

### Global (use everywhere)

```bash
git clone <this-repo-url> ~/.config/opencode
# or after cloning per-project, run:
bash setup.sh --global
```

### Ship skill

In any session with staged changes:

```
ship it
```

This will commit, push, create a PR, and trigger an opencode review.

## Credits

Inspired by [omerxx/dotfiles](https://github.com/omerxx/dotfiles).
