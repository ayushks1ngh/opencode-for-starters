# opencode-for-starters Pipeline

This project includes a team of specialized agents. Follow this pipeline when working on features or tasks.

## Agent Invocation

- `@tech-lead` — Orchestrator. Delegate complex multi-step work here. The tech-lead will break down the request and invoke the right specialists in sequence.
- `@requirements-clarifier` — Use when requirements are vague, incomplete, or need formalization before any code is written. Outputs structured specs with acceptance criteria.
- `@architect-designer` — Use when architecture decisions, design patterns, or system structure needs to be defined. Produces ADRs, diagrams, and trade-off analysis — zero code.
- `@implementation-specialist` — Use for focused coding tasks after requirements and architecture are settled. Strictly follows existing patterns, no scope creep.
- `@test-automation-engineer` — Use after implementation to write and execute tests. Reports coverage and flags regressions.

## Workflow Rules

1. **Vague request** → Start with @requirements-clarifier before any code
2. **Complex feature** → Route through @tech-lead who chains: requirements → architecture → implementation → testing
3. **Simple bug fix** → Use @implementation-specialist directly, verify with @test-automation-engineer
4. **Architecture question** → Use @architect-designer before writing code
5. **Uncertain direction** → Use @big-pickle-simple-tasks to break down into concrete steps

## Commands

- `/build` — Build the project (auto-detects package manager)
- `/scan` — Scan for vulnerabilities using security tools
