# Framework Learnings

Central repository of confirmed assumptions, invalid assumptions, recurring bottlenecks, open questions, and planned improvements — sourced from dogfooding projects.

## Confirmed Assumptions

| # | Assumption | Evidence | Source |
|---|-----------|----------|--------|
| 1 | BUILD_BRIEF.md makes implementation faster | Implemented from BUILD_BRIEF alone in Dogfood #2 without re-reading other 4 docs | 002-url-shortener |
| 2 | AC→Task traceability prevents ambiguity | Could verify "am I done?" by checking AC annotations on each task | 001-cli-task-tracker, 002-url-shortener |
| 3 | Dependency ordering prevents out-of-order implementation | T1.5 depended on T1.2+T1.3+T1.4 — correct order was obvious | 002-url-shortener |
| 4 | Review finds plan gaps that implementation misses | Plan Accuracy dimension found 4 missing specs in #2 | 002-url-shortener |
| 5 | Pipeline works end-to-end | Both projects went from idea → plan → implement → review → ship | 001, 002, 003 |
| 6 | Interface contracts prevent design drift | SDK code matched ARCHITECTURE contracts line-for-line | 003-research-agent-sdk |
| 7 | Module dependency graphs prevent import errors | Implemented in dependency order, zero import errors | 003-research-agent-sdk |
| 8 | BUILD_BRIEF verification steps catch bugs | MockProvider infinite-loop discovered via AC-5 verification | 003-research-agent-sdk |
| 9 | Project classification produces correct artifact depth | AI System classification gave ARCHITECTURE L4 (via triggers), which was essential | 004-ai-chatbot |
| 10 | Behavioral edge cases actively used during implementation | 11/13 specified edge cases correctly implemented; 1 bug caught | 004-ai-chatbot |
| 11 | Depth heuristics triggers correctly identify when to upgrade | ≥3 modules with cross-deps → ARCHITECTURE L4 triggered correctly | 004-ai-chatbot |
| 12 | AI System classification works for LLM-driven agent projects | Agent orchestration + conversation memory + tool calling matched "AI System" definition | 004-ai-chatbot |

## Invalid Assumptions

| # | Assumption | Reality | Source |
|---|-----------|---------|--------|
| 1 | PRD scope boundaries are sufficient for implementation | Security and operational decisions were made ad-hoc during implementation | 002-url-shortener |
| 2 | Architecture structure is enough without interface contracts | Router→handler coupling was undocumented, fragile to extend | 002-url-shortener |
| 3 | Data flow diagram replaces module dependency graph | Import order matters for implementation but was not specified | 002-url-shortener |
| 4 | ACs can be verified manually without test specification | 7 ACs in #2 had zero automated tests — verification was ad-hoc curl commands | 002-url-shortener |
| 5 | Same artifact depth works for all project types | Library projects need deeper interface contracts; apps need deeper security/ops | 003-research-agent-sdk |
| 6 | Behavioral edge cases eliminate all implementation ambiguity | Contract drift can still occur (e.g., "raises KeyError" vs "returns ToolResult") — review dimension needed | 004-ai-chatbot |
| 7 | Dependency graph library choices are accurate | Graph showed `retry_handler.py → (httpx)` but implementation used `urllib` — graph should use stdlib when possible | 004-ai-chatbot |

## Recurring Bottlenecks

| # | Bottleneck | Appears In | Impact | Status |
|---|-----------|-----------|--------|--------|
| 1 | Security constraints not documented in plan | 002-url-shortener | Security decisions made invisibly during implementation | Fixed in v0.4.0 ✅ |
| 2 | No test specification during planning | 001, 002, 003 | ACs exist but no machine-checkable verification | Open |
| 3 | Module dependency ordering absent from architecture | 002-url-shortener | Import graph discovered ad-hoc during implementation | Fixed in v0.4.0 ✅ |
| 4 | Build handoff requires re-reading multiple documents | 001-cli-task-tracker | Fixed by BUILD_BRIEF | Fixed in v0.3.1 ✅ |
| 5 | Behavioral edge cases not specified in contracts | 003-research-agent-sdk | MockProvider multi-turn behavior was ambiguous | Closed in v0.5.0 ✅ — Behavioral Edge Cases added to interface contracts |
| 6 | Contract-vs-implementation drift | 004-ai-chatbot | Behavioral edge case said "raises KeyError" but implementation returned ToolResult (softer was better, but contract was wrong) | Open — proposed Contract Accuracy review dimension |
| 7 | Tool-level timeout not enforceable | 004-ai-chatbot | Contract specified 10s tool timeout but only HTTP-level timeout existed | Open — needs timeout parameter on Tool protocol |

## Open Questions

| # | Question | Context | Need |
|---|---------|---------|------|
| 1 | At what complexity threshold should the planner generate interface contracts? | #2 needed them, #1 didn't | Resolved in v0.5.0 ✅ — "≥3 modules, OR any module has public API surface" trigger in Artifact Depth Heuristics |
| 2 | Should test cases be generated alongside ACs or deferred? | All 3 projects deferred testing | Trade-off analysis: speed vs quality |
| 3 | How does the pipeline behave with a multi-person team? | All projects were single-developer | Need team-based dogfooding |
| 4 | Should the planner adapt artifact depth based on project type? | Library (#3) needed deeper contracts than CLI (#1) | Resolved in v0.5.0 ✅ — Artifact Depth Heuristics provide measurable triggers and per-type defaults |
| 5 | Should a Contract Accuracy review dimension be added? | #4 found behavioral edge case contract drift (KeyError vs ToolResult) | Needs second observation |
| 6 | Should tool-level timeout enforcement be added to behavioral edge cases? | #4 specified 10s but only HTTP timeout existed | Needs second observation |

## Planned Improvements

| # | Improvement | Evidence Rule Status | Target Release |
|---|-----------|---------------------|----------------|
| 1 | Security constraints in PRD | Validated (#2 critical, #3 confirmed) | v0.4.0 ✅ |
| 2 | Interface contracts in ARCHITECTURE | Validated (#2 partial, #3 full) | v0.4.0 ✅ |
| 3 | Module dependency graph in ARCHITECTURE | Validated (#2, #3) | v0.4.0 ✅ |
| 4 | Verification section in BUILD_BRIEF | Validated (#2 proposed, #3 tested) | v0.4.0 ✅ |
| 5 | Planning Completeness review dimension | Validated (#2 proposed, #3 tested) | v0.4.0 ✅ |
| 6 | Dogfooding archive system | Framework governance need | v0.4.0 ✅ |
| 7 | Project type-aware planning | Single observation (#3) — validated by implementation in v0.5.0 | v0.5.0 ✅ |
| 8 | Behavioral edge case specification | Single observation (#3) — validated by implementation in v0.5.0 | v0.5.0 ✅ |

## Evidence Rule

A framework improvement is considered **validated** when:
- It appears in **two or more** dogfooding projects, OR
- It **blocks successful project completion**

Single-project observations should be recorded here but not automatically implemented. This prevents feature creep.

### Current Evidence Status
| Feature | Observations | Status |
|---------|-------------|--------|
| BUILD_BRIEF | 001, 002, 003 | **Validated** ✅ |
| AC→Task traceability | 001, 002, 003 | **Validated** ✅ |
| Task dependencies | 001, 002, 003 | **Validated** ✅ |
| Security constraints in plan | 002 (critical), 003 | **Validated** ✅ |
| Operational constraints in plan | 002 (critical), 003 | **Validated** ✅ |
| Interface contracts | 002 (partial), 003 (full) | **Validated** ✅ |
| Module dependency graph | 002 (partial), 003 (full) | **Validated** ✅ |
| BUILD_BRIEF verification | 002 (partial), 003 (full) | **Validated** ✅ |
| Planning Completeness review | 002 (proposed), 003 (tested) | **Validated** ✅ |
| Project type-aware planning | 003 (single), 004 (full), implemented in v0.5.0 | **Validated** ✅ |
| Behavioral edge case spec | 003 (single), 004 (full), implemented in v0.5.0 | **Validated** ✅ |
| Contract Accuracy review | 004 (single) | Needs validation |
| Tool-level timeout enforcement | 004 (single) | Needs validation |
| Stdlib preference in dependency graph | 004 (single) | Needs validation |
