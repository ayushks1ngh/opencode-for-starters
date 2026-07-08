<p align="center">
  <img src="https://opencode.ai/opencode.svg" alt="opencode" width="120"/>
</p>

<h1 align="center">opencode-for-starters</h1>

<p align="center">
  <b>Turn opencode into a full development team — one command.</b>
</p>

<p align="center">
  <a href="https://github.com/ayushks1ngh/opencode-for-starters/stargazers">
    <img src="https://img.shields.io/github/stars/ayushks1ngh/opencode-for-starters?style=for-the-badge&color=gold" alt="Stars"/>
  </a>
  <a href="https://github.com/ayushks1ngh/opencode-for-starters/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/ayushks1ngh/opencode-for-starters?style=for-the-badge&color=blue" alt="License"/>
  </a>
  <a href="https://opencode.ai">
    <img src="https://img.shields.io/badge/powered%20by-opencode-7C3AED?style=for-the-badge" alt="Powered by opencode"/>
  </a>
  <a href="./VERSION">
    <img src="https://img.shields.io/badge/version-0.2.0-22AA55?style=for-the-badge" alt="Version 0.2.0"/>
  </a>
</p>

---

## What is This?

[opencode](https://opencode.ai) is an open-source AI coding agent that runs in your terminal — like Claude Code, but free and extensible.

This repository is a **starter kit** that transforms opencode into a structured development pipeline. Instead of a blank prompt, you get:

- **7 specialized agents** — an orchestrator, requirements clarifier, architect, implementer, tester, security scanner, and task decomposer
- **Slash commands** — `/build` auto-detects your project, `/scan` checks for vulnerabilities
- **Skill packs** — multi-step workflows like `ship` (commit → push → PR → review in one command)
- **Pipeline orchestration** — AGENTS.md instructions loaded every session, so the model always knows how to route your work

Clone it into `.opencode/`, paste a link, or run the one-liner. That's it.

---

## Features

### Agents

| Agent | Mode | Role |
|---|---|---|
| `tech-lead` | primary | Orchestrator — routes work to specialists, integrates results |
| `requirements-clarifier` | subagent | Vague ideas → structured specs with acceptance criteria |
| `architect-designer` | subagent | Design docs, ADRs, diagrams — zero code |
| `implementation-specialist` | subagent | Writes code with strict scope discipline |
| `test-automation-engineer` | subagent | Writes and runs tests, reports coverage |
| `scan` | subagent | Scans for security vulnerabilities |
| `big-pickle-simple-tasks` | primary | Breaks complex work into small steps |

### Commands

| Command | What it does |
|---|---|
| `/build` | Auto-detects project type, runs the correct build command |
| `/scan` | Detects project type, runs security audit |

### Skills

| Skill | Trigger | What it does |
|---|---|---|
| `ship` | "ship it", "commit push pr" | Stages, commits, pushes, opens PR, triggers review |

### Installation Modes

- **Global** — clone to `~/.config/opencode/` for every project
- **Local** — clone to `.opencode/` for one project
- **Paste-link** — no clone needed, load instructions remotely

### Workflow Orchestration

The default `build` agent is overridden with a pipeline-aware prompt. Every session starts with orchestration knowledge: ambiguous requests route to the requirements clarifier, architectural work to the architect, implementation to the specialist, testing to the test engineer, and security to the scanner. Trivial fixes are handled directly.

---

## Architecture

```
You
 └─ build (default orchestrator)
      ├─ @requirements-clarifier    (vague → structured)
      ├─ @architect-designer        (design → plan)
      ├─ @implementation-specialist (plan → code)
      ├─ @test-automation-engineer  (code → verified)
      ├─ @scan                      (security audit)
      └─ @big-pickle-simple-tasks   (complex → steps)
```

Work flows through a defined pipeline: requirements → architecture → implementation → testing. Each stage has a dedicated agent with clear scope boundaries.

---

## Repository Structure

```
opencode.json            # Config: model, autoupdate, instructions, agent overrides
AGENTS.md                # Pipeline rules (loaded every session as instructions)
VERSION                  # Current version
CHANGELOG.md             # Release history
CONTRIBUTING.md          # Contributor guide
setup.sh                 # Bootstrap script (global / local / auto)
LICENSE                  # MIT license
agent/                   # Agent definitions (7 agents)
  tech-lead.md
  requirements-clarifier.md
  architect-designer.md
  implementation-specialist.md
  test-automation-engineer.md
  scan.md
  big-pickle-simple-tasks.md
command/                 # Slash commands (2 commands)
  build.md
  scan.md
skills/                  # Skill packs
  ship/SKILL.md          #   One-command PR pipeline
.github/                 # Community health files
  ISSUE_TEMPLATE/        #   Bug report + feature request
  pull_request_template.md
```

---

## Installation

### One-liner (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/ayushks1ngh/opencode-for-starters/main/setup.sh | bash
```

Installs opencode if missing, then clones the starter kit globally to `~/.config/opencode/`.

### Paste-link (no clone)

Add this to your project's `opencode.json`:

```json
{
  "instructions": ["https://raw.githubusercontent.com/ayushks1ngh/opencode-for-starters/main/AGENTS.md"]
}
```

The pipeline rules load remotely — no files needed. The default `build` agent and agents defined in `agent/` still require cloning for full functionality.

### Global installation

```bash
bash setup.sh --global
```

Clones to `~/.config/opencode/`. Works in every project.

### Local installation

```bash
bash setup.sh --local
```

Clones to `.opencode/` in the current directory. Per-project setup, ideal for team repos.

### Manual installation

Clone into any project as `.opencode/`:

```bash
git clone https://github.com/ayushks1ngh/opencode-for-starters.git .opencode
```

---

## Usage

### Build a project

```bash
# In any project directory
/build
```

The build agent auto-detects your project type:
- `package.json` → `npm run build`
- `Cargo.toml` → `cargo build`
- `go.mod` → `go build`
- `Makefile` → `make`
- `requirements.txt` + `pyproject.toml` → `pip install -e .`
- `mix.exs` → `mix compile`
- `build.gradle` / `pom.xml` → `./gradlew build` / `mvn compile`

### Scan for vulnerabilities

```bash
/scan
```

Detects your project type and runs the appropriate audit tool: `npm audit`, `cargo audit`, `pip-audit`, `go list`, `bundle audit`, or `composer audit`.

### Ship a change

```bash
# After making changes, just say:
ship it
```

The `ship` skill stages relevant files, fetches and rebases, commits with a conventional commit message, pushes the branch, opens a PR, and triggers an opencode review comment.

---

## Roadmap

### Phase 2 — Planning & Analysis

- **plan** — Structured planning with effort estimation and dependency tracking
- **investigate** — Root-cause debugging workflow
- **review** — Pre-merge code review with automated fix suggestions
- **docs** — Documentation generation and staleness detection

### Phase 3 — Quality & Design

- **qa** — Web QA with test-fix-verify loop
- **cso** — Security audit with OWASP and STRIDE threat modeling
- **design** — Design consultation with system proposals

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide.

Quick start:
1. Read the repository structure and how agents/commands/skills work
2. Make changes following the coding and documentation standards
3. Test with `opencode debug config`
4. Update VERSION and CHANGELOG.md
5. Open a PR

---

## License

MIT — see [LICENSE](./LICENSE).
