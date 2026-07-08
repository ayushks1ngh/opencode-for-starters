# Dogfooding Plan: CLI Task Tracker

## Goal
Validate the opencode-for-starters workflow (Idea → Plan → Architecture → Implementation → Review → Ship) by building a real CLI task tracker from scratch.

## Project: Task Tracker CLI

A minimal but functional CLI task tracker with:
- CRUD operations: add, list, update, delete tasks
- Task fields: id, title, description, status (todo/in-progress/done), priority (low/medium/high), created_at, updated_at
- Storage: JSON file in ~/.task-tracker/tasks.json
- Output: pretty-formatted table (no external dependencies)
- Commands: `task-tracker add "title"`, `task-tracker list`, `task-tracker list --status done`, `task-tracker update <id> --status done`, `task-tracker delete <id>`

Success criteria are organized by pipeline stage to identify gaps.

---

## Success Criteria

### Stage 1: /plan (Idea → Documents)

**Must produce:**
- [ ] PRD.md — product requirements with acceptance criteria
- [ ] ARCHITECTURE.md — data model, CLI design, file layout
- [ ] ROADMAP.md — phased delivery (MVP → enhancements)
- [ ] TASKS.md — broken down into implementable units

**Gap hunting:**
- Are documents comprehensive enough to implement from?
- Is anything missing or ambiguous?
- How long does the planning phase take?
- Are there redundant steps?

### Stage 2: /build (Implementation)

**Must produce:**
- [ ] Working CLI tool matching the specification
- [ ] Clean code with error handling
- [ ] Tests (at minimum unit tests for core logic)
- [ ] Setup/install instructions

**Gap hunting:**
- Can the implementation specialist work from TASKS.md alone?
- Are tasks granular enough? Too granular?
- Does context get lost between task handoffs?
- Are there missing patterns/boilerplate that should be templated?

### Stage 3: /review (Pre-merge)

**Must produce:**
- [ ] Review covering architecture, security, testing, performance, maintainability, DX
- [ ] Issues categorized by severity (critical/high/medium/low)
- [ ] Actionable recommendations

**Gap hunting:**
- Is the review actionable?
- Does it catch real issues?
- Are there dimensions that are under-evaluated?

### Stage 4: /ship (Release)

**Must produce:**
- [ ] Clean commit history
- [ ] Descriptive commit messages
- [ ] PR with description
- [ ] Automated review triggered

**Gap hunting:**
- Are there any friction points in the release flow?

### Stage 5: Post-mortem

- [ ] Document all gaps, friction, and improvements
- [ ] Propose concrete fixes for each issue found

---

## What We're Testing

| Dimension | What to watch for |
|-----------|-------------------|
| **Tech lead orchestration** | Does tech-lead route correctly? Does it fail at any handoff? |
| **Planning quality** | Are outputs actionable? Missing details? |
| **Task granularity** | Too coarse? Too fine? Just right? |
| **Context retention** | Do agents lose context across handoffs? |
| **Review quality** | Does review catch real issues? False positives? |
| **Pipeline friction** | Where does the user get stuck or confused? |
| **Documentation gaps** | What's missing from AGENTS.md, SKILL.md, README? |
| **Missing agents/skills** | What would have made this smoother? |
