# v1.0.0 Readiness Report

**Date**: 2026-07-08
**Current Version**: 0.5.0 (Adaptive Planning)
**Projects Dogfooded**: 4 (CLI, SaaS, SDK, AI System)

---

## 1. Framework Strengths

### 1.1 Proven Pipeline
The `Idea → Plan → Architecture → Implementation → Testing → Review → Ship` pipeline has been validated end-to-end across 4 project types with zero failures. The soft enforcement (recommend but don't block) provides guidance without friction.

### 1.2 Evidence-Driven Governance
The Evidence Rule has prevented 3 speculative features from being implemented (Contract Accuracy review, tool-level timeout, stdlib preference in dep graph). All 11 implemented features have 2+ dogfooding observations.

### 1.3 Adaptive Planning (v0.5.0)
Project classification + artifact depth heuristics correctly adapt planning depth to project type. Measurable triggers (≥3 modules, stateful components, network access) prevent both over-engineering and under-specification. Validated across all 4 project types.

### 1.4 Behavioral Edge Cases (v0.5.0)
7-dimension behavioral edge case specifications (duplicate calls, invalid inputs, concurrency, idempotency, retry, lifecycle, resource limits) caught a real bug during Dogfood #4 (ConnectionError retry). Previously, these were discovered ad-hoc during implementation.

### 1.5 BUILD_BRIEF with Verification (v0.4.0)
The verification section with per-AC commands, expected outcomes, and definition of done has caught bugs in 2 consecutive dogfooding projects (MockProvider infinite loop in #3, ConnectionError retry in #4).

### 1.6 No External Dependencies
All files are plain markdown with YAML frontmatter. No build tools, no compilers, no package.json. The framework is installable via git clone, paste-link, or one-liner.

### 1.7 Dogfooding Archive
`dogfooding/` provides a structured evidence repository with project index, confirmed/invalid assumptions, recurring bottlenecks, open questions, and evidence rule status. Every framework change is traceable to specific dogfooding findings.

---

## 2. Evidence Rule Check

### Validated Features (11 total, all with 2+ observations)

| Feature | First Observed | Second+ Observed | Version |
|---------|---------------|------------------|---------|
| BUILD_BRIEF | 001 | 002, 003 | v0.3.1 |
| AC→Task traceability | 001 | 002, 003 | v0.3.1 |
| Task dependencies | 001 | 002, 003 | v0.3.1 |
| Security constraints in PRD | 002 | 003 | v0.4.0 |
| Operational constraints in PRD | 002 | 003 | v0.4.0 |
| Interface contracts | 002 | 003 | v0.4.0 |
| Module dependency graph | 002 | 003 | v0.4.0 |
| BUILD_BRIEF verification | 002 | 003, 004 | v0.4.0 |
| Planning Completeness review | 002 | 003 | v0.4.0 |
| Project type-aware planning | 003 | 004 | v0.5.0 |
| Behavioral edge case spec | 003 | 004 | v0.5.0 |

### Proposed Changes (ALL single-observation — do NOT implement)

| Proposal | Observed In | Evidence Rule Status |
|----------|------------|---------------------|
| Contract Accuracy review dimension | 004 only | Needs validation ❌ |
| Tool-level timeout enforcement | 004 only | Needs validation ❌ |
| Stdlib preference in dep graph | 004 only | Needs validation ❌ |
| Test specification alongside ACs | 001, 002, 003 (bottleneck #2) | Open (no proposed implementation) |

**Verdict**: No proposed change satisfies the Evidence Rule. The framework is feature-complete for v1.0.0.

---

## 3. Remaining Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Single-developer bias** — all dogfooding was solo | High | Framework may not work for teams | Dogfood #5 should be team-based |
| **No test specification** — AC-5 (retry) bug was caught by manual verification, not automated tests | Medium | Bugs may ship between verification steps | Open bottleneck #2; acceptable for v1.0.0 |
| **Contract drift** — behavioral edge cases may drift from implementation without a review dimension | Low | Minor trust erosion | Single observation; defer to post-v1.0 |
| **3 proposed changes deferred** — users may encounter these issues | Low | Minor friction | Documented in FRAMEWORK_LEARNINGS |
| **No production deployment tested** — all projects were local/dev | Medium | Deployment planning unvalidated | Dogfood #5 could address this |

---

## 4. Framework Snapshot

| Metric | Count |
|--------|-------|
| Agents | 8 (3 primary, 5 subagent) |
| Commands | 5 |
| Skills | 7 |
| Dogfooding projects | 4 |
| Confirmed assumptions | 12 |
| Invalid assumptions (corrected) | 7 |
| Recurring bottlenecks (resolved) | 5 of 7 |
| Open questions | 4 |
| Validated features | 11 |
| Proposed changes (pending validation) | 3 |

---

## 5. Unsupported Assumptions (Not Yet Tested)

| # | Assumption | Why Untested | Risk if Wrong |
|---|-----------|-------------|---------------|
| 1 | Pipeline works for multi-person teams | All dogfooding was solo | Coordination overhead may break flow |
| 2 | AI System and Infrastructure Platform categories produce correct depth | AI System tested (#4), Infra Platform untested | Depth defaults may be wrong for Infra |
| 3 | Memory-enabled agents (opencode sessions >30 min) retain context effectively | All sessions were <30 min | Long sessions may lose artifact context |
| 4 | framework runs reliably on Windows/macOS | Tested on Linux only | setup.sh and path conventions may break |
| 5 | Paste-link mode (no clone) provides equivalent experience | Only clone mode tested | Remote instructions may have latency/caching issues |

---

## 6. Documentation Audit Results

### Issues Found and Fixed

| Issue | File | Fix Applied |
|-------|------|-------------|
| Missing BUILD_BRIEF.md from artifact list | `command/plan.md` | ✅ Added |
| Missing 2 review dimensions from description | `command/review.md` | ✅ Added Plan Accuracy + Planning Completeness |
| Outdated agent count (7 → 8) and structure | `CONTRIBUTING.md` | ✅ Updated |
| Outdated project structure tree | `CONTRIBUTING.md` | ✅ Updated with all agents, commands, skills, dogfooding |
| Versioning guidelines didn't match actual scheme | `CONTRIBUTING.md` | ✅ Updated to semantic versioning with major/minor/patch |
| Installation section missing troubleshooting | `README.md` | Not fixed (see recommendation below) |
| No quickstart example showing output | `README.md` | Not fixed (see recommendation below) |

### Remaining Documentation Gaps

1. **README.md** lacks a "Quick Start" section showing what `/plan` output looks like (a concrete example)
2. **README.md** lacks troubleshooting for common issues (API keys, missing dependencies, git errors)
3. **setup.sh** does not validate prerequisites (git, Python version)
4. **No onboarding guide** for new users — the README jumps directly to installation without a "try it in 30 seconds" section

---

## 7. Recommended Release Plan: v1.0.0

### Version: 1.0.0

**Rationale**: The framework has been validated across 4 project types through 4 dogfooding cycles. All 11 features meet the Evidence Rule (2+ observations). The 3 proposed changes are single-observation and should not block a stable release. The framework is feature-complete for its intended scope.

### Changes Required for v1.0.0 (Documentation Only)

1. **VERSION** → 1.0.0
2. **CHANGELOG.md** → Add v1.0.0 entry summarizing the journey from v0.2.0 through v0.5.0
3. **README.md** → Mark roadmap items as complete, add Stability section
4. **AGENTS.md** → Add v1.0.0 stability commitment

### Changes Explicitly NOT Required

- No new agents, skills, or commands
- No planner features (all validated)
- No review dimensions (all proposed are single-observation)
- No workflow rule changes

### Release Checklist

- [ ] VERSION updated to 1.0.0
- [ ] CHANGELOG.md v1.0.0 entry written
- [ ] README.md roadmap finalized, Stability section added
- [ ] AGENTS.md updated with stability commitment
- [ ] All documentation audit fixes applied
- [ ] GitHub release tag v1.0.0 created
- [ ] Release notes written summarizing framework evolution

### Post-Release Commitment

After v1.0.0:
- **No breaking changes** without a major version bump (v2.0.0)
- **Minor versions** (v1.x.0) add features validated by Evidence Rule
- **Patch versions** (v1.0.x) fix bugs and documentation
- **Dogfooding continues** as the evidence mechanism for future changes
- **New project types** require dogfooding validation before classification is considered stable

---

## 8. Suggested Dogfood #5: Adoption-Focused

### Goal
Validate adoption, not framework evolution. Test whether a new user can successfully use the framework without prior training.

### Approach
Give the framework to a developer who has never used opencode-for-starters. Ask them to build a simple project (CLI tool or small web app) using only the README, /plan, and generated artifacts. Observe without intervening.

### What to Measure
- Time from clone to first `/plan` success
- Time from `/plan` to first working feature
- Number of times the user re-reads README or AGENTS.md
- Number of questions asked
- Number of incorrect assumptions about how the pipeline works
- Whether the user reads the dogfooding examples
- Whether the user finds the Evidence Rule useful or confusing
- Whether the user discovers and uses all 5 commands and 7 skills

### Success Criteria
- Project reaches ship-ready state within a single session
- User does not need to ask "how do I..." more than 3 times
- User at least reads one dogfooding example
- User discovers at least 3 of 5 commands and 3 of 7 skills

### Why This Dogfood
All 4 previous dogfooding projects were executed by the framework author, who understood the design intent. Dogfood #5 is the first test of whether the framework is self-documenting and self-guiding — which determines whether it's ready for public adoption.

---

## 9. Summary

| Dimension | Assessment |
|-----------|-----------|
| Framework maturity | ✅ Ready for v1.0.0 |
| Feature completeness | ✅ All planned features validated by Evidence Rule |
| Documentation | ⚠️ Gaps remain (quickstart, troubleshooting) |
| Adoption readiness | ⚠️ Untested (Dogfood #5 recommended) |
| Evidence Rule compliance | ✅ 11 features validated, 3 proposals deferred |
| Risk level | Low — no blocking issues |
| **Recommended action** | **Release v1.0.0 with documentation improvements, then run Dogfood #5 for adoption validation** |
