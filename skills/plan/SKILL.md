---
name: plan
description: >-
  Convert a raw software idea into an executable engineering plan. Produces
  PRD.md, ARCHITECTURE.md, ROADMAP.md, TASKS.md, and BUILD_BRIEF.md as
  persistent project artifacts. Use when asked to "plan this", "create a plan",
  "scope this feature", "break this down", or "design the architecture".
---

# Plan

Convert a raw software idea into an executable engineering plan with persistent artifacts.

## When to Use This Skill

Invoke this skill when the user says things like:
- "plan this feature"
- "create a plan"
- "scope this idea"
- "break this down into tasks"
- "design the architecture"
- "how should I build this"
- "what's the plan for"

## Workflow

Follow these steps in order.

### Step 1 — Understand the idea

Ask clarifying questions if needed:
- What problem is being solved?
- Who is the user?
- What does success look like?
- What are the constraints?

### Step 2 — Delegate to @planner

The planner agent drives the rest of the workflow:
- Requirements analysis
- Scope definition
- Milestone planning
- Task breakdown
- Risk identification
- Acceptance criteria generation

Delegate to @requirements-clarifier if requirements are vague.
Delegate to @architect-designer if architecture decisions are needed.

### Step 3 — Generate artifacts

Create or update these files:

- **PRD.md** — Problem, users, scope, success metrics. Tag each AC with its target phase (e.g. `AC-1 (Phase 1)`)
- **ARCHITECTURE.md** — System design, data flow, technology choices
- **ROADMAP.md** — Phases, milestones, deliverables, timelines. Map each phase to its ACs by ID
- **TASKS.md** — Granular tasks. Each task must:
  - Reference ACs it satisfies (e.g. `(AC-1, AC-5)`)
  - Declare dependencies on other tasks (e.g. `depends_on: T1.2`)
- **BUILD_BRIEF.md** — Phase-specific implementation brief distilling all artifacts into a single actionable document for the current/next phase

### Step 4 — Validate cross-references

Before presenting, run these checks:
- Every PRD AC is referenced in ROADMAP phase mapping
- Every ROADMAP phase has at least one TASKS item
- Every TASKS item references at least one AC
- Every TASKS dependency points to an existing task
- BUILD_BRIEF.md covers all tasks and ACs for the phase

Report any validation failures to the user.

### Step 5 — Present the plan

Summarize the plan to the user:
- What was decided
- What needs sign-off
- What risks were identified
- What validation checks passed or failed
- Recommended next step (typically implementation)

## Rules

- No implementation
- No coding
- No premature optimization
- Prefer simple architectures over complex ones
- Prefer incremental delivery over big-bang releases
- Treat output documents as living assets — update them as the project evolves
- Validate cross-references before presenting — PRD↔ROADMAP, AC→task, dependency completeness
- Generate BUILD_BRIEF.md for the current phase after the other artifacts
- Get user sign-off before implementation begins
