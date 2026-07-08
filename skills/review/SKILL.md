---
name: review
description: >-
  Pre-merge engineering code review. Analyzes the diff for architecture
  violations, security issues, testing gaps, performance problems,
  maintainability concerns, developer experience regressions, UI/accessibility
  compliance (via web-design-guidelines), and documentation quality (via
  writing-guidelines). Reports findings with severity levels and an approval
  status. Use when asked to "review this PR", "code review", "review my
  changes", or "check the diff".
---

# Review

Pre-merge engineering code review with severity-ranked findings.

## When to Use This Skill

Invoke this skill when the user says things like:
- "review this pr"
- "code review"
- "review my changes"
- "check the diff"
- "review before merging"
- "review this branch"

## Checklist

Evaluate the diff against each dimension. For UI-related reviews, also invoke the **web-design-guidelines** skill to check accessibility, UX, and visual compliance. For documentation reviews, invoke the **writing-guidelines** skill for style and voice consistency.

### Architecture
- Does the change follow the existing architecture?
- Are component boundaries respected?
- Are abstractions appropriate for the problem?
- Is there unnecessary complexity or over-engineering?

### Security
- Are inputs validated and sanitized?
- Are there injection vulnerabilities (SQL, XSS, command)?
- Are secrets, tokens, or credentials handled safely?
- Are permissions and access controls checked?
- Is sensitive data exposed in logs or output?

### Testing
- Are there tests covering the change?
- Do tests cover edge cases and error paths?
- Are tests meaningful (not just coverage padding)?
- Do existing tests still pass?

### Performance
- Are there N+1 queries, unnecessary loops, or redundant work?
- Are resources (connections, memory, file handles) properly released?
- Could this change cause a regression under load?

### Maintainability
- Is the code clear and readable?
- Are naming conventions consistent with the project?
- Is error handling appropriate and consistent?
- Is the change self-contained with minimal coupling?
- Are there TODOs or commented-out code that should be addressed?

### Developer Experience
- Is the change easy to understand without deep context?
- Are there migration or deployment steps?
- Is documentation or README updated if needed?

### Plan Accuracy
- Does the implementation match the PRD acceptance criteria for this phase?
- Are all ACs for the current phase implemented? If not, are unimplemented ACs documented and justified?
- Were plan gaps discovered during implementation (missing specs, ambiguous requirements, incorrect assumptions)?
- Does the implementation respect ARCHITECTURE.md decisions (data model, file structure, interfaces, dependency graph)?
- Are there discrepancies between TASKS.md task descriptions and what was actually built?
- If plan gaps were found, are they documented for planner feedback?

### Planning Completeness
- **Security constraints**: Are PRD security constraints (input validation, allowed protocols, auth, trust boundaries) documented and implemented? If missing, flag as a planning gap.
- **Operational assumptions**: Are PRD operational constraints (storage location, binding, environment, database config) documented and followed? If missing, flag as a planning gap.
- **Interface contracts**: Does ARCHITECTURE specify component interfaces? Does the implementation follow them? If missing, flag as a planning gap.
- **Module dependency graph**: Does ARCHITECTURE include a dependency graph? Does the implementation's import structure match it? If missing, flag as a planning gap.
- **Verification steps**: Does BUILD_BRIEF include verification commands for each AC? Are they accurate? If missing, flag as a planning gap.
- **Acceptance criteria sufficiency**: Were the ACs sufficient to guide implementation? Were there questions the ACs didn't answer? Flag gaps.
- **Output**: For each gap found, categorize as:
  - `Planning gap — missing from artifacts`
  - `Planning gap — incorrect in artifacts`
  - `Implementation deviation — justified`
  - `Implementation deviation — unjustified`

## Severity Levels

| Level | Meaning | Action Required |
|-------|---------|-----------------|
| Critical | Production risk, data loss, security vulnerability | Must fix before merge |
| High | Incorrect behavior, significant tech debt, maintainability issue | Should fix before merge |
| Medium | Minor issue, style inconsistency, non-critical improvement | Fix if convenient |
| Low | Suggestion, nitpick, future consideration | Optional |

## Output

Present findings in this structure:

### Summary
One-paragraph overview of the review: what was reviewed, overall quality assessment.

### Findings
Numbered list with:
- **Severity**: [Critical/High/Medium/Low]
- **File**: Path and line number
- **Issue**: What is wrong
- **Recommendation**: How to fix it

### Recommendations
Prioritized action items in order of importance.

### Approval Status
- **Approved** — No critical or high issues. Ready to merge.
- **Approved with concerns** — Only medium/low issues. Merge after addressing.
- **Changes requested** — Critical or high issues must be resolved before merge.

## Rules

- Prioritize high-impact issues over nitpicks
- Focus on production readiness
- Be specific — include file paths and line numbers
- Suggest fixes, not just problems
- Do not rewrite the code — flag issues and recommend changes
- Be constructive, not critical
