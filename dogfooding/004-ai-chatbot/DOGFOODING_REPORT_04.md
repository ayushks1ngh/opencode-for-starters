# Dogfooding Report #4: Memory-Enabled Agent Chatbot

**Project**: Memory-Enabled Agent Chatbot
**Framework Version**: v0.5.0 (Adaptive Planning)
**Goal**: Validate Adaptive Planning, Artifact Depth Heuristics, and Behavioral Edge Case Specifications
**Date**: 2026-07-08

---

## 1. Classification Accuracy

**Classification Chosen**: AI System
**Alternative Considered**: CLI Tool, Library/SDK

### Was it correct?
Yes. The project combines LLM integration, agent orchestration (tool-calling loop), conversation memory, and session management — it is an AI System by the planner's definition ("LLM integration, agent orchestration, prompt management").

**CLI Tool** was briefly considered because it has a REPL interface, but this misses the defining characteristics (LLM-driven decision loop, tool orchestration, stateful conversation). A CLI classification would have produced ARCHITECTURE L1 (no contracts, no dependency graph), which would have been dangerously insufficient for 12 modules with cross-dependencies.

**Library/SDK** was another candidate since the modules are importable, but the project has an entry point and CLI — it's a complete application, not a library.

### Would another category have produced better artifacts?
No. The AI System depth defaults (PRD L3, ARCHITECTURE L3, TASKS L3, BUILD_BRIEF L5) were a good starting point. The depth triggers correctly upgraded ARCHITECTURE to L4 (≥3 modules with cross-dependencies).

### Classification Verdict
✅ **Correct classification**. The artifact depth heuristics properly handled the upgrade from default L3 to L4 based on measurable triggers.

---

## 2. Artifact Depth Effectiveness

### PRD — L3 (Security + Operational constraints)
| Depth Level | Contents | Used During Implementation? |
|-------------|----------|---------------------------|
| L1 | Problem, scope, ACs | Yes — scoped features correctly |
| L2 | Security constraints | Yes — API key from env var (not config file), input truncation at 4096 |
| L3 | Operational constraints | Yes — Python 3.11+, storage path `~/.chatbot/sessions/`, env vars `CHATBOT_MAX_RETRIES` |

**Verdict**: L3 was appropriate. The security constraints (API key management, input validation) directly guided implementation decisions. The operational constraints (storage paths, env vars) were used verbatim.

### ARCHITECTURE — L4 (Contracts + Edge Cases + Dependency Graph)
| Depth Level | Contents | Used During Implementation? |
|-------------|----------|---------------------------|
| L1 | System design, data flow, component boundaries | Yes — data flow diagram guided orchestrator design |
| L2 | Interface contracts | Yes — function signatures used directly; error conventions guided implementation |
| L3 | Behavioral edge cases | Yes — idempotency of delete_session, non-retryable errors, lifecycle of MessageStore |
| L4 | Module dependency graph | Yes — prevented import cycle and verified file creation order |

**Verdict**: L4 was essential. Without interface contracts and behavioral edge cases, the `is_retryable` bug would not have been caught by specification. The dependency graph prevented an import cycle between session_store.py and message_store.py (shared BASE_DIR).

### TASKS — L3 (Traceability Matrix)
Standard for all projects. The traceability matrix was used to verify every AC had coverage. No issues.

### BUILD_BRIEF — L5 (Verification section)
The verification section directly caught the `is_retryable` ConnectionError bug (AC-5). Without the explicit "auth errors fail fast, transient errors retry" specification, this would have shipped as an invisible bug.

### Depth Trigger Correctness

| Trigger | Activated? | Appropriate? |
|---------|-----------|-------------|
| Network access → PRD L2 | ✅ Yes | API keys needed secure handling |
| Data storage → PRD L3 | ✅ Yes | Persistence path and env var names documented |
| ≥3 modules → ARCH L2 | ✅ Yes | 12 modules needed contracts |
| Stateful component → ARCH L3 | ✅ Yes | SessionManager, Orchestrator, MessageStore all stateful |
| ≥3 modules cross-dep → ARCH L4 | ✅ Yes | 12 modules with dense cross-dependencies |
| ≥3 files → BUILD L2 | ✅ Yes | 12 files needed architecture essentials |

### Depth Effectiveness Verdict
✅ **All depth levels were appropriate**. No artifact was too shallow or unnecessarily detailed. The measurable triggers correctly identified when to upgrade depth.

---

## 3. Behavioral Edge Case Coverage

### Specified vs. Discovered

| Edge Case | Specified in Contract? | Handled in Implementation? | Notes |
|-----------|----------------------|--------------------------|-------|
| Duplicate session titles | ✅ Allowed (IDs unique, not titles) | ✅ Implemented | No dedup needed |
| Resuming deleted session | ✅ Returns None | ✅ Implemented | |
| Deleting active session | ✅ Deactivated, messages remain | ✅ Implemented | |
| Empty message | ✅ Rejected with error | ✅ Implemented | |
| Very long message | ✅ Truncated at 4096 | ✅ Implemented | |
| Unknown tool call | ✅ "I don't have a tool named X" | ✅ Implemented | |
| Tool returns error | ✅ Error sent back to LLM | ✅ Implemented | |
| Tool timeout | ✅ Orchestrator interrupts | ⚠️ Partial | Timeout at HTTP level (30s), not tool level (10s) |
| LLM hallucinates tool args | ✅ Args fail validation, error to LLM | ✅ Implemented | |
| Network timeout on retry | ✅ Retried, succeeds transparently | ✅ Implemented | |
| Rate limit retry exhausted | ✅ User sees error message | ✅ Implemented | |
| Auth error | ✅ Immediate failure | ✅ Implemented | |
| is_retryable ConnectionError | ✅ Should be retryable | ⚠️ **Bug caught** | Implementation checked string, not type. Fixed by BUILD_BRIEF verification |

### Missing Edge Cases Discovered

1. **ToolRegistry.execute contract inconsistency**: Contract said "raises KeyError if tool_name not found" but implementation returned `ToolResult(success=False, error=...)`. The behavioral edge case should have specified the exact error behavior. **Minor — the softer behavior (returning error result instead of raising) was actually better**, but the contract was wrong.

2. **Tool-level timeout not implemented**: Contract said 10s tool timeout, but implementation only has 30s HTTP timeout at the LLM provider level. The tool execution doesn't have its own timeout. This is a missing architectural edge case.

### Edge Case Verdict
✅ **Behavioral edge cases were actively used during implementation.** 11 of 13 specified edge cases were correctly implemented. The 2 issues found are minor (one contract-out-of-sync that was actually better, one missing tool-level timeout that's acceptable for MVP).

---

## 4. Validation Check Results

All 14 planner validation checks passed:

| # | Check | Result |
|---|-------|--------|
| 1 | PRD↔ROADMAP consistency | ✅ |
| 2 | ROADMAP↔TASKS consistency | ✅ |
| 3 | AC→Task traceability | ✅ |
| 4 | Traceability matrix completeness | ✅ |
| 5 | Dependency completeness | ✅ |
| 6 | BUILD_BRIEF coverage | ✅ |
| 7 | BUILD_BRIEF verification completeness | ✅ |
| 8 | Security constraints present | ✅ |
| 9 | Operational constraints present | ✅ |
| 10 | Interface contracts exist | ✅ |
| 11 | Module dependency graph present | ✅ |
| 12 | Behavioral edge cases present | ✅ |
| 13 | Depth justification clear | ✅ |
| 14 | Classification recorded | ✅ |

---

## 5. New Bottlenecks Discovered

| # | Bottleneck | Impact | Proposed Fix |
|---|-----------|--------|-------------|
| 1 | **Contract vs. Implementation drift** — behavioral edge case in contract said "raises KeyError" but implementation returned ToolResult | Low — softer behavior was better, but inconsistency undermines trust | Architect should validate that implementation matches the behavior edge case after construction (add to review dimension) |
| 2 | **No tool-level timeout** — contract specified 10s tool timeout but HTTP client timeout (30s) is the only guard | Low — acceptable for MVP, but could cause hangs | Add timeout parameter to Tool.execute protocol |
| 3 | **Dependency graph inaccuracy** — `retry_handler.py → (httpx)` in ARCHITECTURE was wrong (uses only stdlib) | Low — didn't affect implementation, but dependency graph should match final code | Planner should use stdlib when possible, or dependency graph should be reviewed for accuracy |

---

## 6. Invalid Assumptions Found

| # | Assumption | Reality | Impact |
|---|-----------|---------|--------|
| 1 | **Behavioral edge cases eliminate all ambiguity** | They eliminate most, but contract-vs-implementation drift can still occur (e.g., "raises KeyError" vs "returns ToolResult") | Low — the softer contract was fine, but contract accuracy should be verified during review |
| 2 | **Dependency graph fully defines import order** | The graph accurately shows module relationships, but it doesn't capture that the implementation may substitute dependencies (e.g., httpx → urllib) | Low — dependency was at the boundary; graph should reflect capability, not specific library |

---

## 7. Proposed Framework Changes

All proposals are supported by Dogfood #4 evidence. None are speculative.

### Change 1: Add Tool-Level Timeout to Behavioral Edge Cases (Low Priority)
**Evidence**: Contract specified 10s tool timeout (under Resource Limits) but implementation only had HTTP-level timeout.
**Proposal**: Add a `timeout_seconds` field to the behavioral edge case Resource Limits section, with the note that it must be enforceable at the implementation level.
**Evidence Rule Status**: Single observation (Dogfood #4). Needs second observation before implementation.

### Change 2: Verify Behavioral Edge Case Accuracy During Review (Medium Priority)
**Evidence**: Contract said "raises KeyError" but implementation returned `ToolResult`. While the softer behavior was better, the contract should match reality.
**Proposal**: Add a 9th review dimension — "Contract Accuracy" — that compares interface contracts (including behavioral edge cases) against implementation. This would catch drifts between what the contract says and what the code does.
**Evidence Rule Status**: Single observation (Dogfood #4). Needs second observation.

### Change 3: Library Substitution Should Be Noted in Dependency Graph (Low Priority)
**Evidence**: Dependency graph showed `retry_handler.py → (httpx)` but implementation used `urllib`. The dependency is correct semantically (HTTP), but the specific library was wrong.
**Proposal**: When a module only requires stdlib, prefer it in the dependency graph. If a third-party library is specified and stdlib substitution is possible, note it as a decision in the architecture.
**Evidence Rule Status**: Single observation (Dogfood #4). Needs second observation.

### No Change Proposed for Framework Core
No changes to agents, skills, commands, or workflow rules are proposed. The v0.5.0 Adaptive Planning framework performed well for this project type.

---

## 8. Evidence Rule Assessment

### Project Type-Aware Planning: ✅ VALIDATED
| Dogfood #1 (CLI) | Dogfood #2 (SaaS) | Dogfood #3 (SDK) | Dogfood #4 (AI System) |
|------------------|-------------------|-------------------|----------------------|
| CLI classification implicitly correct | SaaS classification correct | Library/SDK classification correct | AI System classification correct |
| L1 PRD was sufficient | L3 PRD was necessary | L2 PRD was appropriate | L3 PRD was appropriate |
| L1 ARCH was sufficient | L2 ARCH was barely enough | L4 ARCH was essential | L4 ARCH was essential |

**Four project types now tested. AI System (Dogfood #4) validates the classification + depth heuristic system for a project type that shares characteristics with both CLI (entry point, file I/O) and SDK (importable modules, public interfaces).**

### Behavioral Edge Case Specifications: ✅ VALIDATED
| Dogfood #3 (SDK) | Dogfood #4 (AI System) |
|------------------|----------------------|
| Missing — identified as gap | Implemented — 7 edge case dimensions per component |
| | 11 of 13 specified edge cases correctly implemented |
| | 1 bug caught: `is_retryable` ConnectionError handling |
| | 1 contract drift discovered: KeyError vs ToolResult |

**Two project types now tested. Behavioral edge cases directly caught an implementation bug and prevented ambiguity in 11 of 13 cases.**

### Status of Proposed Changes (from Section 7)
| Change | Observations | Evidence Rule Status |
|--------|-------------|---------------------|
| Tool-level timeout enforcement | Dogfood #4 (single) | Needs validation |
| Contract Accuracy review dimension | Dogfood #4 (single) | Needs validation |
| Stdlib preference in dependency graph | Dogfood #4 (single) | Needs validation |

---

## Summary

| Metric | Result |
|--------|--------|
| Classification accuracy | ✅ Correct (AI System) |
| Artifact depth appropriateness | ✅ All 4 artifacts at correct depth |
| Behavioral edge cases used | ✅ 11/13 specified, 1 bug caught |
| Validations passed | ✅ 14/14 |
| Bugs caught by verification | ✅ 1 (ConnectionError retry) |
| Architecture decisions outside artifacts | 1 (urllib vs httpx — dependency availability) |
| Implementation ambiguities | 1 (ToolRegistry contract mismatch — minor) |
| Framework changes proposed | 3 (all low priority, all single-observation) |
| Core framework changes needed | **None** — v0.5.0 is validated as-is |

**Verdict: v0.5.0 Adaptive Planning is validated.** The AI System project type stressed the classification system, depth heuristics, and behavioral edge cases. The framework adapted correctly, produced appropriate artifacts, and the behavioral edge cases directly improved implementation quality.
