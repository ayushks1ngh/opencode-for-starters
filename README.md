<p align="center">
  <img src="https://opencode.ai/opencode.svg" alt="opencode" width="120"/>
</p>

<h1 align="center">opencode-for-starters</h1>

<p align="center">
  <b>Turn a raw software idea into a production-ready project through structured AI-driven workflows.</b>
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
    <img src="https://img.shields.io/badge/version-0.5.0-22AA55?style=for-the-badge" alt="Version 0.5.0"/>
  </a>
</p>

---

## What is This?

[opencode](https://opencode.ai) is an open-source AI coding agent that runs in your terminal — like Claude Code, but free and extensible.

This repository is a **project execution framework** that transforms opencode from a blank prompt into a structured engineering team. It guides you through the full software delivery lifecycle:

```
Idea → Plan → Architecture → Implementation → Testing → Review → Ship
```

Clone it into `.opencode/`, paste a link, or run the one-liner.

---

## Features

### Agents

| Agent | Mode | Role |
|---|---|---|
| `tech-lead` | primary | Orchestrator — routes work to specialists, enforces pipeline order |
| `planner` | primary | Requirements analysis, scope, milestones, risks. Adapts artifact depth to project type (CLI, SaaS, Library, AI System, Infra Platform) using measurable heuristics. Generates persistent project docs with security constraints, operational constraints, interface contracts, module dependency graphs, and behavioral edge case specifications |
| `big-pickle-simple-tasks` | primary | Breaks complex work into small actionable steps |
| `requirements-clarifier` | subagent | Vague ideas → structured specs with acceptance criteria |
| `architect-designer` | subagent | Design docs, ADRs, diagrams — zero code |
| `implementation-specialist` | subagent | Writes code with strict scope discipline |
| `test-automation-engineer` | subagent | Writes and runs tests, reports coverage |
| `scan` | subagent | Scans for security vulnerabilities |

### Commands

| Command | What it does |
|---------|-------------|
| `/build` | Auto-detects project type, runs the correct build command |
| `/scan` | Detects project type, runs security audit |
| `/plan` | Creates an engineering plan with PRD, architecture, roadmap, and tasks |
| `/investigate` | Systematic root-cause debugging workflow |
| `/review` | Pre-merge code review with severity-ranked findings across 8 dimensions including Planning Completeness |

### Skills

| Skill | Trigger | What it does |
|-------|---------|-------------|
| `plan` | "plan this", "create a plan" | Converts ideas into executable plans with persistent artifacts |
| `investigate` | "debug this", "fix this bug" | Systematic debugging — reproduce, analyze, fix, verify |
| `review` | "review this pr", "code review" | Pre-merge review across 8 dimensions (incl. Planning Completeness) with severity levels |
| `docs` | "document this", "write docs" | Generates README, architecture, API, and setup documentation. Automatically checks output against writing-guidelines |
| `ship` | "ship it", "commit push pr" | Stages, commits, pushes, opens PR, triggers review |
| `web-design-guidelines` | "review my UI", "check accessibility" | Reviews UI code against 100+ accessibility, UX, and visual compliance rules |
| `writing-guidelines` | "review my docs", "check writing style" | Reviews prose against 80+ writing style and voice rules |

### Installation Modes

- **Global** — clone to `~/.config/opencode/` for every project
- **Local** — clone to `.opencode/` for one project
- **Paste-link** — no clone needed, load instructions remotely

---

## Architecture

```
You
 └─ build (default orchestrator)
      ├─ @planner                    (idea → plan + artifacts)
      ├─ @requirements-clarifier     (vague → structured)
      ├─ @architect-designer         (design → architecture)
      ├─ @implementation-specialist  (plan → code)
      ├─ @test-automation-engineer   (code → verified)
      ├─ @scan                       (security audit)
      └─ @big-pickle-simple-tasks    (complex → steps)
```

Work flows through a defined pipeline: idea → plan → architecture → implementation → testing → review → ship. Each stage has a dedicated agent with clear scope boundaries. The pipeline guides but does not block — you always retain control.

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
agent/                   # Agent definitions (8 agents)
  tech-lead.md
  planner.md
  requirements-clarifier.md
  architect-designer.md
  implementation-specialist.md
  test-automation-engineer.md
  scan.md
  big-pickle-simple-tasks.md
command/                 # Slash commands (5 commands)
  build.md
  scan.md
  plan.md
  investigate.md
  review.md
  skills/                  # Skill packs (7 skills)
    plan/SKILL.md          #   Planning workflow
    investigate/SKILL.md   #   Debugging workflow
    review/SKILL.md        #   Code review workflow (8 dimensions)
    docs/SKILL.md          #   Documentation workflow
    ship/SKILL.md          #   One-command PR pipeline
    web-design-guidelines/ #   UI/accessibility review (100+ rules)
    writing-guidelines/    #   Documentation style review (80+ rules)
  dogfooding/              # Dogfooding archive (evidence for framework changes)
    PROJECT_INDEX.md       #   Dogfooding project tracker
    FRAMEWORK_LEARNINGS.md #   Confirmed assumptions, bottlenecks, open questions
    001-cli-task-tracker/  #   Dogfood #1 artifacts
    002-url-shortener/     #   Dogfood #2 artifacts
    templates/             #   Dogfooding templates
  .github/                 # Community health files
  ISSUE_TEMPLATE/
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

The pipeline rules load remotely — no files needed. Cloning is required for full agent and skill functionality.

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

### Plan a feature

```
/plan
```

Creates an engineering plan with persistent artifacts:
- **PRD.md** — Product requirements, user personas, scope, success metrics, security constraints, operational constraints
- **ARCHITECTURE.md** — System design, data flow, technology choices, interface contracts, module dependency graphs
- **ROADMAP.md** — Milestones, phases, deliverables, timelines
- **TASKS.md** — Granular tasks with AC references, explicit dependencies, and traceability matrix
- **BUILD_BRIEF.md** — Phase-specific implementation brief with verification commands for every acceptance criterion

### Build a project

```
/build
```

Auto-detects your project type and runs the correct build command.

### Debug an issue

```
/investigate
```

Follows a systematic debugging workflow: reproduce → gather evidence → analyze → hypothesize → fix → verify.

### Review code changes

```
/review
```

Analyzes the diff for architecture, security, testing, performance, maintainability, developer experience, plan accuracy, and planning completeness. Reports findings with severity levels.

### Scan for vulnerabilities

```
/scan
```

Detects your project type and runs the appropriate audit tool.

### Ship a change

```
ship it
```

Stages relevant files, commits, pushes, opens a PR, and triggers a review.

---

## Roadmap

### v0.5.0 — Adaptive Planning ✅

- **Adaptive Planning**: Planner classifies projects (CLI, SaaS, Library, AI System, Infra Platform) and adapts artifact depth using measurable triggers
- **Artifact Depth Heuristics**: Each artifact has 3-5 depth levels with explicit required-when conditions
- **Behavioral Edge Cases**: Interface contracts extended with duplicate calls, concurrency, idempotency, retry, lifecycle, and resource limit specifications
- **No scope creep**: Zero new agents, skills, or commands

### v0.4.0 — Planning Maturity ✅

- **Planning Maturity**: Security constraints, operational constraints, interface contracts, module dependency graphs now part of standard planning
- **BUILD_BRIEF v2**: Verification section with executable curl/command examples for every acceptance criterion
- **Planning Completeness review**: 8th review dimension checks planning artifact quality
- **Dogfooding archive**: Structured evidence repository for framework governance

### Phase 6 — Quality & Design

- **qa** — Web QA with test-fix-verify loop
- **cso** — Security audit with OWASP and STRIDE threat modeling
- **design** — Design consultation with system proposals

### Phase 6 — Operations

- **deploy** — Deployment automation
- **monitor** — Post-deployment monitoring and alerting

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
