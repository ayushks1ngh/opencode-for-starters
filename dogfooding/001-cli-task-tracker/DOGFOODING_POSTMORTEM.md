# Dogfooding Post-Mortem: CLI Task Tracker

## Overview
Built Phase 1 of a CLI task tracker using the opencode-for-starters pipeline (Plan → Build). This document captures gaps, friction, and recommendations.

---

## 1. Plan Artifact Quality Analysis

### What worked well
- **TASKS.md granularity was correct for Phase 1** — each task was a single file or a single command. No task took more than 5 minutes.
- **ARCHITECTURE.md prevented design drift** — the data model, storage path, file structure, and CLI shape were locked upfront.
- **PRD acceptance criteria** were specific enough to verify against (`task-tracker add "Buy groceries"` → output with ID).

### What was missing or wrong

#### 1a. PRD/Roadmap inconsistency
- **AC-3 (Update task)** is listed as "MVP (Must Have)" in PRD user stories, but ROADMAP puts `update` in Phase 2.
- The two documents contradict each other. The planner should cross-reference user stories with roadmap phases.

#### 1b. No test specification
- PRD has acceptance criteria but no mapping to test cases.
- TASKS defers testing to Phase 3, but ACs should be testable from day one.
- Missing: a `test_spec.md` or AC→test mapping in the planning phase.

#### 1c. AC→Task traceability missing
- TASKS items don't reference which acceptance criteria they satisfy.
- Makes it hard to verify coverage: "Did we implement AC-3?" requires manual cross-referencing.
- Fix: each task should annotate `(AC-1, AC-5)` or equivalent.

#### 1d. Task dependency ordering
- TASKS lists items sequentially but doesn't declare dependencies.
- T1.4 depends on T1.3 depends on T1.2 — obvious in this case, but for complex projects it should be explicit.

---

## 2. Implementation Reality vs Plan

### Discrepancies found

| # | Plan said | Reality | Impact |
|---|-----------|---------|--------|
| 1 | `exit code 2` for system errors in ARCHITECTURE error handling | `sys.exit(2)` in storage.py for corrupt JSON | Works but hard to test — `sys.exit()` aborts the process |
| 2 | AC-3 (Update) is MVP | Not implemented (Phase 2 in ROADMAP) | Minor — inconsistency, not a bug |
| 3 | `T1.1: Create pyproject.toml with build config` | Used setuptools backend | ARCHITECTURE didn't specify build system — made a reasonable choice but unclear |

### Missing from plan (discovered during implementation)

| What was missing | Why it matters |
|-----------------|----------------|
| Validation regex/spec for title (min/max length, allowed chars) | Users could add empty titles or 10KB strings |
| Strategy for concurrent access (file locking) | Two terminal sessions would corrupt data — low priority but should be documented |
| Help text for subcommands (`add --help`, `list --help`) | ARCHITECTURE shows top-level help only |

---

## 3. Pipeline Friction Points

### F1: No handoff summary between plan and build
- After `/plan`, the implementer must re-read 4 documents to find the relevant parts.
- A "build brief" — a single document distilling what Phase 1 needs — would reduce context-switching.
- **Fix idea**: planner should produce a `BUILD_BRIEF.md` for the current phase, referencing but not duplicating the other docs.

### F2: Task ordering is implicit
- TASKS lists items but doesn't say "do them in this order" or declare dependencies.
- Implementer must infer order from content.
- **Fix idea**: add `depends_on` or ordering to TASKS format.

### F3: No feedback loop from build back to plan
- During implementation, I found plan gaps (empty title validation, subcommand help, concurrency). There's no mechanism to feed these back.
- **Fix idea**: during `/review`, include a "Plan accuracy" dimension that checks implementation against plan and flags gaps.

### F4: AC verification is manual
- No way to systematically verify all ACs are met.
- Currently: read PRD ACs, check implementation manually.
- **Fix idea**: PRD should include test commands that can be run for each AC, or ACs should be in a machine-checkable format.

---

## 4. Specific Recommendations for opencode-for-starters

### Agent improvements

#### Planner agent (`agent/planner.md`)
- Add: Generate a `BUILD_BRIEF.md` for the first/current phase — single-page distillation of what to build, how to build it, and acceptance criteria.
- Add: Cross-reference ACs in TASKS — each TASKS item should list which ACs it satisfies.
- Add: Include a "Dependencies" section in TASKS — which tasks depend on which.
- Fix: Ensure PRD user story tiers (MVP/Should/Could) match ROADMAP phases.

#### Tech lead agent (`agent/tech-lead.md`)
- Add: After plan completion, produce a "Phase Brief" that tells the implementer exactly what to build.
- Add: Task sequencing guidance — "Start with T1.2, then T1.3, etc."

#### Implementation specialist (`agent/implementation-specialist.md`)
- Add: After implementation, auto-generate a "Plan gap report" — what was missing from the plan that had to be decided during implementation.

### Skill improvements

#### Plan skill (`skills/plan/SKILL.md`)
- After generating artifacts, validate: cross-check PRD user stories vs ROADMAP phases for consistency.
- After generating artifacts, validate: each TASKS item maps to at least one AC.

#### Review skill (`skills/review/SKILL.md`)
- Add a "Plan accuracy" dimension: does the implementation match the PRD? Are there unimplemented ACs? Were plan gaps discovered during implementation?

#### New skill needed: handoff skill
- Generate a build brief from plan artifacts.
- Context: a distilled version of the plan for the implementer.

### Command improvements

#### `/plan` command
- Should produce: PRD.md, ARCHITECTURE.md, ROADMAP.md, TASKS.md, BUILD_BRIEF.md (new).

---

## 5. Summary

| Dimension | Verdict | 
|-----------|---------|
| Planning quality | Good — artifacts were usable, actionable, and mostly accurate |
| Task granularity | Excellent — no task was too large or too small |
| Plan implementation fidelity | High — implementation matched plan documents closely |
| Gaps found | PRD/ROADMAP inconsistency, no test spec, no AC traceability, no task dependencies |
| Friction points | Handoff between plan→build, no feedback loop, manual AC verification |
| Pipeline readiness | **Not yet ready for unsupervised use** — needs the improvements above before users can run `/plan → build → review → ship` without human intervention |
