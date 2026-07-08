# opencode-for-starters Pipeline

This project includes a team of specialized agents. Follow this pipeline when working on features or tasks.

## Agent Invocation

- `@tech-lead` — Orchestrator. Routes work to the right specialist and integrates results.
- `@requirements-clarifier` — Transforms vague or incomplete requests into structured specs with acceptance criteria.
- `@architect-designer` — Produces architecture decisions, ADRs, diagrams, and structural plans — zero code.
- `@implementation-specialist` — Executes focused coding tasks with strict scope discipline.
- `@test-automation-engineer` — Writes and runs tests, reports coverage, flags regressions.
- `@scan` — Scans for security vulnerabilities and dependency issues.
- `@big-pickle-simple-tasks` — Breaks down complex problems into small actionable steps.

## Workflow Rules

1. **Vague request** → Start with @requirements-clarifier before any code
2. **Complex feature** → Route through @tech-lead who chains: requirements → architecture → implementation → testing
3. **Simple bug fix** → Use @implementation-specialist directly, verify with @test-automation-engineer
4. **Architecture question** → Use @architect-designer before writing code
5. **Uncertain direction** → Use @big-pickle-simple-tasks to break down into concrete steps
6. **Security audit** → Use @scan to check for vulnerabilities

## Commands

- `/build` — Build the project (auto-detects package manager)
- `/scan` — Scan for vulnerabilities using security tools
