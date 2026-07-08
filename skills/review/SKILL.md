---
name: review
description: >-
  Pre-merge engineering code review. Analyzes the diff for architecture
  violations, security issues, testing gaps, performance problems,
  maintainability concerns, and developer experience regressions. Reports
  findings with severity levels and an approval status. Use when asked to
  "review this PR", "code review", "review my changes", or "check the diff".
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

Evaluate the diff against each dimension.

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
