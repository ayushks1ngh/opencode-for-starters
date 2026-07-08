---
name: plan
description: >-
  Convert a raw software idea into an executable engineering plan. Produces
  PRD.md, ARCHITECTURE.md, ROADMAP.md, TASKS.md, and BUILD_BRIEF.md as
  persistent project artifacts. Plans adapt artifact depth to project type (CLI,
  SaaS, Library, AI System, Infrastructure Platform) using measurable heuristics.
  Includes security constraints, operational constraints, interface contracts,
  module dependency graphs, and behavioral edge case specifications when
  triggered by project complexity. BUILD_BRIEF.md includes executable
  verification steps for every acceptance criterion. Use when asked to "plan
  this", "create a plan", "scope this feature", "break this down", or "design
  the architecture".
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

### Step 1 — Classify and understand the idea

First, classify the project type. Ask the user to confirm one of:
- **CLI Tool** — executable, stdin/stdout, file I/O, no network server
- **Application / SaaS** — HTTP server, database, network-bound, auth
- **Library / SDK** — imported by consumers, public API surface, no entry point
- **AI System** — LLM integration, agent orchestration
- **Infrastructure Platform** — containers, networking, deployment config

Then, ask clarifying questions to determine artifact depth triggers:
- What problem is being solved?
- Who is the user?
- What does success look like?
- What are the constraints?
- **Module count**: How many components/modules are expected?
- **Network access**: Does this make network calls or listen on a network?
- **Data storage**: Does this persist data? What kind?
- **Public API**: Is there an external-facing API?
- **Statefulness**: Are there stateful components? Lifecycle management?
- **Concurrency**: Could multiple callers interact simultaneously?
- **Security context**: What data is involved? What are the trust boundaries?
- **Operational context**: Where will this run? What's the deployment model?

Answering these questions determines what artifact depth (L1-L4) each document needs.

### Step 2 — Delegate to @planner with classification context

Pass the project type and depth triggers to the planner. The planner agent drives the rest of the workflow:
- Project classification (confirmed in Step 1)
- Artifact depth selection based on triggers
- Requirements analysis
- Scope definition
- Milestone planning
- Task breakdown
- Risk identification
- Acceptance criteria generation
- Security constraint documentation (depth-dependent)
- Operational constraint documentation (depth-dependent)
- Interface contract specification (depth-dependent)
- Behavioral edge case documentation (depth-dependent)
- Module dependency ordering (depth-dependent)

Delegate to @requirements-clarifier if requirements are vague.
Delegate to @architect-designer if architecture decisions are needed.

### Step 3 — Generate artifacts at appropriate depth

Use the classification and depth triggers to determine what each artifact contains. Apply the **Artifact Depth Heuristics** from the planner agent:

| Artifact | CLI | SaaS | Library | AI System | Infra Platform |
|----------|-----|------|---------|-----------|----------------|
| PRD | L1 | L3 | L2 | L3 | L3 |
| ARCHITECTURE | L1 | L2 (L3 if stateful) | L4 | L3 | L2 |
| TASKS | L3 | L3 | L3 | L3 | L3 |
| BUILD_BRIEF | L3 (L4 if ≥5 tasks) | L5 | L5 (if ≥5 ACs) | L5 | L5 |

Create or update these files at the determined depth:

- **PRD.md** — Problem, users, scope, success metrics, security constraints (L2+), operational constraints (L3+). Tag each AC with its target phase (e.g. `AC-1 (Phase 1)`)
- **ARCHITECTURE.md** — System design, data flow, technology choices, interface contracts (L2+), behavioral edge cases (L3+), module dependency graph (L4+)
- **ROADMAP.md** — Phases, milestones, deliverables, timelines. Map each phase to its ACs by ID
- **TASKS.md** — Granular tasks. Each task must:
  - Reference ACs it satisfies (e.g. `(AC-1, AC-5)`)
  - Declare dependencies on other tasks (e.g. `depends_on: T1.2`)
  - Include a traceability matrix at the end
- **BUILD_BRIEF.md** — Phase-specific implementation brief. Must include:
  - Tasks with ordering and dependencies
  - ACs to satisfy
  - Architecture essentials (L2+)
  - Interface contracts keyed to this phase (L3+)
  - Dependency chain (L4+)
  - **Verification section** for every AC (all projects): verification steps, validation commands, expected outcomes, definition of done

### Step 4 — Validate cross-references

Before presenting, run these checks:
- Every PRD AC is referenced in ROADMAP phase mapping
- Every ROADMAP phase has at least one TASKS item
- Every TASKS item references at least one AC
- Traceability matrix covers every AC
- Every TASKS dependency points to an existing task
- BUILD_BRIEF.md covers all tasks and ACs for the phase
- BUILD_BRIEF.md has verification steps for every AC
- PRD includes security constraints (L2+) and operational constraints (L3+)
- ARCHITECTURE includes interface contracts (L2+) and module dependency graph (L4+) at the required depth
- ARCHITECTURE includes behavioral edge cases for stateful/concurrent components (L3+)
- Artifact depth levels are recorded in the plan summary with rationale
- Project type classification is recorded in the plan summary

Report any validation failures to the user.

### Step 5 — Present the plan

Summarize the plan to the user:
- **Project classification** (type and why)
- **Artifact depths selected** with rationale per artifact
- What was decided
- What needs sign-off
- What risks were identified
- What security constraints were documented (depth-dependent)
- What operational assumptions were documented (depth-dependent)
- What behavioral edge cases were specified (depth-dependent)
- What validation checks passed or failed
- Recommended next step (typically implementation)

## Rules

- No implementation
- No coding
- No premature optimization
- Prefer simple architectures over complex ones
- Prefer incremental delivery over big-bang releases
- Treat output documents as living assets — update them as the project evolves
- Validate cross-references before presenting — PRD↔ROADMAP, AC→task, dependency completeness, verification completeness
- Generate BUILD_BRIEF.md for the current phase after the other artifacts
- Document security and operational constraints before implementation — do not leave them to be discovered during coding
- Get user sign-off before implementation begins
