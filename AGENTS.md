# opencode-for-starters Pipeline

This project includes a team of specialized agents. Follow this pipeline when working on features or tasks.

## Core Workflow

```
Idea → Plan → Architecture → Implementation → Testing → Review → Ship
```

Each stage has a dedicated agent. The pipeline guides but does not block — you always retain control.

## Agent Invocation

### Primary Agents

- `@tech-lead` — Orchestrator. Routes work to the right specialist and integrates results.
- `@planner` — Requirements analysis, scope definition, milestone planning, risk identification. Generates PRD.md, ARCHITECTURE.md, ROADMAP.md, and TASKS.md as persistent project artifacts.
- `@big-pickle-simple-tasks` — Breaks down complex problems into small actionable steps.

### Specialist Agents

- `@requirements-clarifier` — Transforms vague or incomplete requests into structured specs with acceptance criteria.
- `@architect-designer` — Produces architecture decisions, ADRs, diagrams, and structural plans — zero code.
- `@implementation-specialist` — Executes focused coding tasks with strict scope discipline.
- `@test-automation-engineer` — Writes and runs tests, reports coverage, flags regressions.
- `@scan` — Scans for security vulnerabilities and dependency issues.

## Workflow Rules

1. **New project or feature** → Use `/plan` or delegate to @planner before any code
2. **Vague request** → Start with @requirements-clarifier or @planner before any code
3. **Complex feature** → Route through @tech-lead who chains: plan → architecture → implementation → testing → review → ship
4. **Bug fix** → Use `/investigate` for root-cause analysis, then fix, then `/review`
5. **Simple bug fix** → Use @implementation-specialist directly, verify with @test-automation-engineer
6. **Architecture question** → Use @architect-designer before writing code
7. **Uncertain direction** → Use @big-pickle-simple-tasks to break down into concrete steps
8. **Security audit** → Use @scan to check for vulnerabilities
9. **Complete work** → Use `/review` before merging, then `/ship` or "ship it"

## Commands

| Command | What it does |
|---------|-------------|
| `/build` | Build the project (auto-detects package manager) |
| `/scan` | Scan for vulnerabilities using security tools |
| `/plan` | Create an engineering plan with persistent artifacts |
| `/investigate` | Debug an issue using systematic root-cause analysis |
| `/review` | Review code changes before merging |
