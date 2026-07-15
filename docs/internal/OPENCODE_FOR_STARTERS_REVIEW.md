# opencode-for-starters — Overall Review & Improvement Backlog

**Date**: 2026-07-09
**Author**: big-pickle
**Status**: Archived internal review — committed to `docs/internal/` for historical reference
**Scope**: Holistic retrospective of what works, what's broken, and what should improve

---

## 1. Executive Summary

opencode-for-starters is a structured AI engineering team that runs inside opencode. It has been validated across 4 project types (CLI, SaaS, SDK, AI System) through 4 dogfooding cycles. The Evidence Rule has successfully prevented feature creep. The framework is **release-ready at v1.0.0**.

**But**: self-dogfooding exposed that the framework doesn't always catch its own rot. Several issues found in the pre-release audit (wrong tree diagram, stale counts, empty directories) are exactly the kind of documentation/structure drift the framework is *designed* to prevent — they just weren't caught because the pipeline wasn't followed rigorously on the framework's own repo.

**Self-rating**: 8/10 for external projects, 7.5/10 for internal maintenance.

---

## 2. What Works Well (Keep)

| Area | Rating | Why |
|------|--------|-----|
| Pipeline structure | 9/10 | Idea → Plan → Architecture → Implementation → Testing → Review → Ship is intuitive and complete |
| Evidence Rule | 10/10 | Prevented 3 speculative features from v1.0.0. Every change is traceable to dogfooding evidence |
| Adaptive Planning | 9/10 | Classification + depth heuristics correctly adapt to project type without over/under-specifying |
| Behavioral Edge Cases | 8/10 | Caught real bugs (ConnectionError retry). 7 dimensions cover the most common failure modes |
| BUILD_BRIEF verification | 9/10 | Per-AC commands caught bugs in 2 consecutive dogfooding projects |
| Dogfooding archive | 9/10 | FRAMEWORK_LEARNINGS.md + PROJECT_INDEX.md make every decision auditable |
| Agent specialization | 9/10 | 8 agents with clear scope boundaries, no overlap |
| Skill design | 8/10 | Plan/Investigate/Review/Ship workflows are actionable and well-structured |

---

## 3. Issues Found (Categorized by Severity)

### 3.1 Critical (Would Block Unsupervised Use)

| # | Issue | Evidence | Fix |
|---|-------|----------|-----|
| C1 | **Single-developer bias** — all 4 dogfooding projects were solo | V1_READINESS_REPORT, FRAMEWORK_LEARNINGS open question #3 | Run Dogfood #5 with a real team or at least a second developer |
| C2 | **No team-based validation** — pipeline behavior with multiple humans is untested | Same as C1 | Same as C1 |

### 3.2 High (Significant Friction)

| # | Issue | Evidence | Fix |
|---|-------|----------|-----|
| H1 | **Build-to-plan feedback loop is manual** | tech-lead.md says "process gap reports" but provides no automation. Plan gaps found in review are not auto-fed back to planner | Add a feedback step: after review, extract plan gaps and update artifacts automatically |
| H2 | **No CI/CD** | `.github/workflows/` missing. Release is manual | Add a basic workflow: lint markdown, validate agent/skill frontmatter, run `opencode debug config` |
| H3 | **External URL dependency in 2 skills** | web-design-guidelines and writing-guidelines fetch from `raw.githubusercontent.com/vercel-labs/...` at runtime | Vendor the rule files into the repo, or add a cached fallback |
| H4 | **Onboarding unvalidated** | No user has successfully used the framework without author involvement | Dogfood #5: give to a new dev, observe without intervening |

### 3.3 Medium (Quality of Life)

| # | Issue | Evidence | Fix |
|---|-------|----------|-----|
| M1 | **README tree diagram was wrong** (`skills/` under `command/`) | Found in audit, fixed in v1.0.0 cleanup | The framework didn't catch its own doc rot — running `/review` after restructure would have |
| M2 | **Skills count mismatch** (V1_READINESS_REPORT said 5, actual 7) | Found in audit, fixed | Same as M1 — cross-reference validation missing |
| M3 | **Empty `dogfooding/templates/` directory** | Found in audit, removed | Add a repo-hygiene check to ship skill |
| M4 | **setup.sh doesn't validate prerequisites** | Audit noted, not fixed | Add `command -v git && command -v curl` checks |
| M5 | **Stale agent count in DOGFOODING_REPORT_02** (said 9, actual 8) | Found in audit, fixed | No stale-reference checker exists |
| M6 | **No automated test for framework itself** | No test suite validates agent frontmatter, skill triggers, or cross-references | Add a lightweight markdown linter / schema validator |
| M7 | **Paste-link mode untested** | V1_READINESS_REPORT risk | Test loading AGENTS.md remotely without clone |
| M8 | **Windows/macOS untested** | V1_READINESS_REPORT risk | Test setup.sh on non-Linux platforms |

### 3.4 Low (Minor / Acceptable for v1.0.0)

| # | Issue | Note |
|---|-------|------|
| L1 | `.agents/skills/` duplicate of `skills/` | Git-ignored, local-only artifact. Harmless but confusing |
| L2 | No "example output" in Quick Start | Deliberate choice to avoid stale content |
| L3 | ROADMAP in README lists future phases (Phase 6) that aren't started | Acceptable as roadmap, but could confuse new users about what's shipped |
| L4 | CONTRIBUTING.md doesn't mention dogfooding process | Minor — the dogfooding section is implicit |

---

## 4. Design Gaps (Framework Limitations)

### 4.1 The "Self-Dogfooding" Paradox

The framework is designed to prevent exactly the issues found in its own audit:
- Wrong tree diagram → `/review` checks "documentation updated?"
- Stale counts → `/plan` validates cross-references
- Empty dirs → `/ship` should check for dead files

**But nobody ran `/review` on the README after the skills restructure.** The framework works best when you follow the pipeline. When steps are skipped, drift accumulates silently.

**Recommendation**: The framework needs a "meta" check — a way to run its own review on itself. A `verify-framework.sh` or a `/audit` command that validates:
- All agent/skill/command counts match README/CONTRIBUTING/AGENTS
- All directory references in docs match reality
- All links resolve
- Frontmatter is valid YAML

### 4.2 No Machine-Checkable Verification

BUILD_BRIEF verification steps are manual (run command, check output). There's no `make verify` or `verify_phase_1.sh` that runs all AC checks automatically.

**Evidence**: Dogfood #3 recommended this. Still not implemented (would require a template output, not a new skill).

### 4.3 Contract-vs-Implementation Drift

Behavioral edge cases specify behavior, but nothing verifies the implementation matches. Dogfood #4 found "raises KeyError" vs "returns ToolResult" drift.

**Evidence Rule**: Single observation. Deferred. But it's a real gap — the framework can't self-verify contract fidelity.

### 4.4 Dependency Graph Accuracy

The module dependency graph showed `retry_handler.py → (httpx)` but implementation used `urllib`. Graphs can be semantically correct but library-wrong.

**Evidence Rule**: Single observation. Deferred.

### 4.5 Tool-Level Timeout Not Enforceable

Behavioral edge cases specify `timeout_seconds` but the implementation only has HTTP-level timeout.

**Evidence Rule**: Single observation. Deferred.

---

## 5. Onboarding Weaknesses

| Gap | Impact |
|------|--------|
| No "try it in 30 seconds" before installation | Users may bounce before understanding value |
| Quick Start shows the flow but not actual CLI output | Users can't see what success looks like |
| Troubleshooting added late (v1.0.0 cleanup) | Earlier versions had zero help for common failures |
| No video/screenshot demo | Text-only onboarding has higher friction |
| No "concepts" page explaining agents vs skills vs commands | New users may confuse them |

---

## 6. Operational Gaps

| Gap | Impact |
|-----|--------|
| No CI/CD | Releases are manual; no automated quality gate |
| No versioning automation | VERSION + CHANGELOG + git tag must be done by hand |
| No issue/PR automation | `.github/` has templates but no workflows |
| No dependency scanning for the framework itself | Low risk (markdown-only) but unmonitored |
| No telemetry/usage data | Can't tell if anyone actually uses it |

---

## 7. Evidence Rule Limitations

The Evidence Rule is the framework's strength — but it has blind spots:

1. **Single-developer bias can validate wrong things**: If the author makes the same mistake in 2 dogfooding projects, it becomes "validated." The rule counts observations, not correctness.

2. **Conflicting evidence is under-weighted**: When Dogfood #3 said "behavioral edge cases needed" and Dogfood #4 confirmed, that's 2 observations. Good. But when an observation appears once and is clearly a real gap (contract drift), it's deferred indefinitely.

3. **No negative evidence**: The rule tracks "appears in 2+ projects" but doesn't track "tried in 2+ projects and wasn't useful." A feature could be perpetually re-validated without anyone questioning whether it's needed.

4. **Team validation is a single untested assumption**: The biggest risk (C1/C2) isn't covered by the rule at all — the rule validates features, not the framework's behavior under team load.

---

## 8. Prioritized Improvement Backlog

### Must-Do (Post-v1.0.0, before v1.1.0)

| Priority | Item | Effort | Evidence Rule Status |
|----------|------|--------|---------------------|
| P0 | Dogfood #5: team-based adoption test | Medium | N/A (validates assumption) |
| P0 | `verify-framework.sh` / `/audit` self-check | Medium | New capability, needs design |
| P1 | CI/CD workflow (markdown lint + frontmatter validation) | Low | Operational need |
| P1 | Vendor or cache Vercel rule files | Low | H3 |
| P1 | setup.sh prerequisite validation | Low | M4 |

### Should-Do (v1.x minor releases)

| Priority | Item | Effort | Evidence Rule Status |
|----------|------|--------|---------------------|
| P2 | Auto plan-gap feedback loop | Medium | H1, single observation |
| P2 | `verify_phase_N.sh` generation from BUILD_BRIEF | Low | M2 from #3, single obs |
| P2 | Contract Accuracy review dimension | Medium | Single observation (#4) |
| P2 | Tool-level timeout enforcement | Low | Single observation (#4) |
| P2 | Stdlib preference in dependency graph | Low | Single observation (#4) |

### Nice-to-Have (Future)

| Priority | Item | Effort |
|----------|------|--------|
| P3 | Onboarding video/screenshot | Medium |
| P3 | "Concepts" page (agents vs skills vs commands) | Low |
| P3 | Cross-platform setup.sh testing | Medium |
| P3 | Paste-link mode validation | Low |
| P3 | Usage telemetry | Medium |

---

## 9. The Honest Verdict

> **The framework is good. It is not yet proven.**

It works for the author. It has been validated across 4 project types. The Evidence Rule has kept it disciplined. But:

1. **It has never been used by someone who didn't build it.**
2. **It doesn't reliably catch its own documentation drift.**
3. **It has no automated quality gate (CI/CD).**
4. **Its biggest risk (team behavior) is completely untested.**

These are not blocking for v1.0.0 — the framework is stable and useful today. But they are the **exact things that should be on the v1.1.0 backlog**.

The single most important next step is **Dogfood #5**: hand the framework to a new developer and watch where they get stuck. Everything else is secondary to that evidence.

---

## 10. What I'd Tell a Skeptic

**"Why not just prompt an AI directly?"**

Because this framework makes the *same* AI:
- Plan before coding (no more "oops, I should've scoped that")
- Document security/operational decisions explicitly (no more ad-hoc choices)
- Verify against acceptance criteria (no more "looks done, ship it")
- Review before merging (no more silent regressions)

**"But it's just markdown files?"**

Yes. And that's the point. Zero dependencies, zero build step, works in any opencode session. The complexity is in the *process*, not the *tooling*.

**"What's the catch?"**

It's only been used by one person. Until Dogfood #5 proves it works for strangers, treat v1.0.0 as "stable for the author, promising for everyone else."
