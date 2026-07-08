# Framework Learnings

Central repository of confirmed assumptions, invalid assumptions, recurring bottlenecks, open questions, and planned improvements — sourced from dogfooding projects.

## Confirmed Assumptions

| # | Assumption | Evidence | Source |
|---|-----------|----------|--------|
| 1 | BUILD_BRIEF.md makes implementation faster | Implemented from BUILD_BRIEF alone in Dogfood #2 without re-reading other 4 docs | 002-url-shortener |
| 2 | AC→Task traceability prevents ambiguity | Could verify "am I done?" by checking AC annotations on each task | 001-cli-task-tracker, 002-url-shortener |
| 3 | Dependency ordering prevents out-of-order implementation | T1.5 depended on T1.2+T1.3+T1.4 — correct order was obvious | 002-url-shortener |
| 4 | Review finds plan gaps that implementation misses | Plan Accuracy dimension found 4 missing specs in #2 | 002-url-shortener |
| 5 | Pipeline works end-to-end | Both projects went from idea → plan → implement → review → ship | 001, 002 |

## Invalid Assumptions

| # | Assumption | Reality | Source |
|---|-----------|---------|--------|
| 1 | PRD scope boundaries are sufficient for implementation | Security and operational decisions were made ad-hoc during implementation | 002-url-shortener |
| 2 | Architecture structure is enough without interface contracts | Router→handler coupling was undocumented, fragile to extend | 002-url-shortener |
| 3 | Data flow diagram replaces module dependency graph | Import order matters for implementation but was not specified | 002-url-shortener |
| 4 | ACs can be verified manually without test specification | 7 ACs in #2 had zero automated tests — verification was ad-hoc curl commands | 002-url-shortener |

## Recurring Bottlenecks

| # | Bottleneck | Appears In | Impact |
|---|-----------|-----------|--------|
| 1 | Security constraints not documented in plan | 002-url-shortener | Security decisions made invisibly during implementation |
| 2 | No test specification during planning | 001-cli-task-tracker, 002-url-shortener | ACs exist but no machine-checkable verification |
| 3 | Module dependency ordering absent from architecture | 002-url-shortener | Import graph discovered ad-hoc during implementation |
| 4 | Build handoff requires re-reading multiple documents | 001-cli-task-tracker | Fixed by BUILD_BRIEF in v0.3.1 |

## Open Questions

| # | Question | Context | Need |
|---|---------|---------|------|
| 1 | At what complexity threshold should the planner generate interface contracts? | #2 needed them, #1 didn't | A complexity heuristic for the planner |
| 2 | Should test cases be generated alongside ACs or deferred? | Both projects deferred testing | Trade-off analysis: speed vs quality |
| 3 | How does the pipeline behave with a multi-person team? | All projects were single-developer | Need team-based dogfooding |

## Planned Improvements

| # | Improvement | Evidence Rule Status | Target Release |
|---|-----------|---------------------|----------------|
| 1 | Security constraints in PRD | Validated in #2 (critical gap) | v0.4.0 ✅ |
| 2 | Interface contracts in ARCHITECTURE | Validated in #2 (high gap) | v0.4.0 ✅ |
| 3 | Module dependency graph in ARCHITECTURE | Validated in #2 (high gap) | v0.4.0 ✅ |
| 4 | Verification section in BUILD_BRIEF | Validated in #2 (medium gap) | v0.4.0 ✅ |
| 5 | Planning Completeness review dimension | Validated in #2 (high gap) | v0.4.0 ✅ |
| 6 | Dogfooding archive system | Framework governance need | v0.4.0 ✅ |

## Evidence Rule

A framework improvement is considered **validated** when:
- It appears in **two or more** dogfooding projects, OR
- It **blocks successful project completion**

Single-project observations should be recorded here but not automatically implemented. This prevents feature creep.

### Current Evidence Status
- **BUILD_BRIEF**: Validated (appeared in 001 and 002) ✅
- **AC→Task traceability**: Validated (001 and 002) ✅
- **Task dependencies**: Validated (001 and 002) ✅
- **Security constraints in plan**: Single observation (002) — marked critical because it blocks production readiness
- **Interface contracts**: Single observation (002) — needs validation in #3
- **Module dependency graph**: Single observation (002) — needs validation in #3
- **Verification section**: Single observation (002) — needs validation in #3
