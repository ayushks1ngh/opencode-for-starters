# Dogfooding Report 02: URL Shortener SaaS

## Summary
Built a 5-endpoint URL shortener MVP (create, redirect, stats, list, delete) using the opencode-for-starters v0.3.1 pipeline. The project is a significant complexity jump from Dogfood #01 (CLI task tracker) — it has an HTTP server, SQLite persistence, URL routing, request parsing, click tracking, and error handling across 5 source files.

---

## 1. What Worked

### 1a. v0.3.1 workflow improvements all validated
- **BUILD_BRIEF.md**: I implemented from BUILD_BRIEF.md alone without re-reading PRD/ARCH/ROADMAP/TASKS. The distillation was sufficient. This is a clear win.
- **AC→Task traceability**: During implementation, I could verify "am I done?" by checking which ACs each task satisfied. The `(AC-1)` annotations in TASKS.md made coverage obvious.
- **Dependency ordering**: `depends_on` declarations prevented out-of-order implementation. T1.5 (handlers) correctly depended on T1.2 (storage) + T1.3 (shortcode) + T1.4 (router).
- **Cross-reference validation**: The checkpoint caught the pytest/dependency inconsistency before implementation began.

### 1b. Artifact quality scaled acceptably
- PRD acceptance criteria were specific enough to test against (I verified each AC with curl)
- ARCHITECTURE.md data model was implemented exactly as specified
- The 5-module file structure (server / router / handlers / storage / shortcode) matched the plan

### 1c. Code quality
- Zero external dependencies (as specified in PRD)
- All endpoints work correctly (verified with curl)
- Error handling covers the specified cases (400, 404, 500, invalid JSON, missing URL)

---

## 2. What Failed

### 2a. Plan Accuracy gaps (CRITICAL — affects every project)
During implementation, I had to make decisions that were not specified in the plan artifacts:

| Missing spec | Decision made during implementation | Should have been in |
|-------------|-------------------------------------|---------------------|
| URL scheme validation — which URL schemes are allowed? | I chose http/https only (manual check) | PRD acceptance criteria or ARCHITECTURE security section |
| Server bind address | 0.0.0.0 (exposes to all interfaces) | ARCHITECTURE deployment section or config spec |
| Database file location | ~/.url-shortener/data.db | ARCHITECTURE storage section |
| WAL mode for SQLite | Enabled (beneficial but unspecified) | ARCHITECTURE — should document intentional decisions |
| Short code character set (exclude lookalikes?) | Full alphanumeric (0/O, 1/l/I ambiguous) | ARCHITECTURE short code spec |

**Root cause**: The planner generates structure (file layout, API endpoints, data model) but not operational details (security constraints, deployment config, edge case behavior). These decisions get made ad-hoc during implementation, which means:
- Different implementers would make different choices
- No documentation of WHY a choice was made
- Security-sensitive decisions bypass review

### 2b. No test specification (HIGH — affects quality)
TASKS phased testing to Phase 3. For a project with persistence (SQLite), this means:
- No verification that database schema is correct
- No verification that data survives restarts (AC-6)
- No verification of error paths (invalid JSON, missing URL, 404)
- Regressions are undetectable

The PRD has 7 acceptance criteria. Zero of them have automated tests. For a CLI, this was acceptable. For a SaaS with persistence and multiple interacting components, it's not.

### 2c. Router design fragility (MEDIUM — discovered in review)
The routing in router.py uses raw regex matching with procedural if/elif blocks. This works but:
- DELETE and GET redirect share the same path pattern (`^/([a-zA-Z0-9]+)$`) — differentiated only by method check
- Adding new methods (PUT, PATCH) requires careful ordering
- Adding path parameters (e.g., `/api/v1/<code>`) means rewriting the routing block

The architecture specified the routing approach but didn't anticipate growth. A routing table (declarative list of method+pattern→handler tuples) would scale better. This is a design-level gap that the planner should capture: "What happens when this pattern grows?"

---

## 3. Friction Points

### F1: Cross-module dependency during implementation (HIGH)
The router imports from handlers, which import from storage and shortcode. The dependency chain in TASKS is correct (T1.2 → T1.5), but the planner doesn't specify the **import graph**. This means:
- Implementer must discover the import structure themselves
- Circular imports or missing imports surface during runtime, not planning
- Fix: ARCHITECTURE should include a module dependency graph (not just data flow)

### F2: Handler→router coupling is implicit (MEDIUM)
Handlers return `tuple[int, dict | str]`, and router has special-case logic for status 301 (Location header). This coupling is undocumented. If a new handler returns 301 in the future, the router must be updated. The planner didn't specify the handler contract.

- Fix: ARCHITECTURE should specify the handler interface (return type, status codes, header requirements)

### F3: BUILD_BRIEF needs a "verification" section (LOW)
After implementing, I had to manually verify each endpoint with curl. The BUILD_BRIEF should include a `## Verification` section with curl commands for each AC. This would make AC verification systematic rather than ad-hoc.

### F4: Review feedback has no back-link to planner (MEDIUM)
The Plan Accuracy dimension in review found 4 plan gaps. But there's no mechanism to automatically feed these back to the planner skill for improvement. The tech lead's build-to-plan feedback loop (v0.3.1) requires manual processing by the tech lead agent.

---

## 4. Missing Artifacts

| Missing artifact | Why it's needed | Criticality |
|-----------------|----------------|-------------|
| **Module dependency graph** | ARCHITECTURE shows data flow but not import graph. During implementation, the import order matters (no circular deps, correct init sequence). | HIGH |
| **Security constraints document** | PRD has non-requirements but no security section. URL scheme validation, bind address, input sanitization — all discovered ad-hoc. | HIGH |
| **Handler interface contract** | Handlers and router share implicit assumptions about return types and status codes. These should be explicitly documented. | MEDIUM |
| **Test specification** | ACs describe behavior but not how to verify it. A `test_cases.md` or test matrix would make ACs machine-checkable. | HIGH |
| **Verification script in BUILD_BRIEF** | BUILD_BRIEF has "what to build" but not "how to verify it was built correctly." A curl-based smoke test suite would help. | LOW |

---

## 5. Missing Skills

None discovered. The existing skill set (plan, investigate, review, docs, ship) covered the pipeline end-to-end. The gaps are in artifact **content quality**, not missing skills.

---

## 6. Missing Agents

None discovered. The existing 9 agents (tech-lead, planner, requirements-clarifier, architect-designer, implementation-specialist, test-automation-engineer, scan, big-pickle-simple-tasks, build) covered the workflow.

---

## 7. Missing Workflow Steps

| Missing step | Where it belongs | Criticality |
|-------------|-----------------|-------------|
| **Security review before implementation** | After ARCHITECTURE generation, before TASKS. The planner should flag security constraints (allowed URL schemes, bind address, input validation) and include them in the ARCHITECTURE. | HIGH — security decisions made during implementation are invisible |
| **Test case generation during planning** | After TASKS, before implementation. The planner should generate a test matrix mapping ACs to test scenarios, even if tests are implemented later. | HIGH — without this, ACs are unverifiable |
| **Handler contract specification during architecture** | In ARCHITECTURE.md. The interface between router and handlers should be explicitly specified (return types, error conventions, header handling). | MEDIUM |

---

## 8. Recommended Changes (Prioritized)

### Critical (blocking for unsupervised use)

1. **PRD.md: Add security section** — After problem statement, add a "Security Constraints" section with URL scheme whitelist, input validation rules, binding defaults, and CORS strategy (even if deferred).
2. **ARCHITECTURE.md: Add module dependency graph** — After project structure, add a text-based module dependency diagram showing import order and initialization sequence.
3. **ARCHITECTURE.md: Add handler interface spec** — Document the contract between router and handlers: return type format, status code conventions, header requirements for special statuses (301, 201, 204).

### High (significant workflow improvement)

4. **TASKS.md: Add test cases alongside tasks** — Each task should include a `verify_with` section (curl commands, assertion examples). This makes ACs machine-checkable from day one.
5. **BUILD_BRIEF.md: Add verification section** — After tasks, add a `## Verification` section with curl/HTTPie commands testing each AC.
6. **ROADMAP.md: Include security milestones** — Security constraints should appear as a Phase 0.5 milestone, not deferred.

### Medium (quality of life)

7. **skills/plan/SKILL.md: Add security constraint prompt** — The plan skill should instruct the planner to explicitly enumerate security decisions that would otherwise be made ad-hoc during implementation.
8. **agent/tech-lead.md: Formalize plan gap processing** — The build-to-plan feedback loop currently requires the tech lead to "process" gap reports. Make this more prescriptive: update artifacts, generate diff, notify planner skill.

---

## 9. Severity Summary

| Issue | Severity | Area |
|-------|----------|------|
| No security constraints in planning artifacts | CRITICAL | planner / PRD |
| No automated tests for 7 ACs | HIGH | planner / TASKS / PRD |
| Handler interface not specified | HIGH | ARCHITECTURE |
| Module import graph not documented | HIGH | ARCHITECTURE |
| Router design doesn't scale | MEDIUM | ARCHITECTURE |
| BUILD_BRIEF missing verification section | MEDIUM | planner / BUILD_BRIEF |
| Global DB connection singleton | LOW | implementation |
| Single-threaded server | LOW | ARCHITECTURE (documented) |

---

## 10. Key Takeaways

1. **The pipeline works**. The plan→implement→review process was followed end-to-end and produced working software. v0.3.1 improvements (BUILD_BRIEF, AC traceability, dependencies) were all validated as useful.

2. **Content quality is the bottleneck, not process**. The pipeline steps are correct. What's missing is the *depth* of content within the artifacts. PRD needs security constraints. ARCHITECTURE needs module graphs and handler contracts. These are content improvements to existing artifacts, not new artifacts.

3. **SaaS vs CLI: the difference is state**. The CLI task tracker had simple file I/O. The URL shortener has a database with concurrent access, a server lifecycle, and network I/O. The planner needs to generate more operational detail for stateful projects. This suggests the planner should ask "is this stateful?" and generate deeper artifacts accordingly.

4. **The review caught what it should**. Plan Accuracy dimension found 4 plan gaps. This validates the v0.3.1 addition to the review skill. The gap is in feeding these findings back to the planner.

5. **Dogfooding methodology works**. Two dogfooding projects (CLI + SaaS) revealed distinct sets of issues. The CLI tested task granularity and plan→build handoff. The SaaS tested artifact depth and security planning. Running multiple dogfooding projects with different characteristics is essential for framework validation.
