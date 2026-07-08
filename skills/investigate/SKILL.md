---
name: investigate
description: >-
  Systematic debugging and root-cause analysis. Reproduce the issue, gather
  evidence, analyze the data flow, form a hypothesis, verify it, implement
  the fix, and confirm the resolution. No fixes before root cause. Use when
  asked to "debug this", "fix this bug", "investigate this issue", "why is
  this broken", or "root cause analysis".
---

# Investigate

Systematic debugging workflow: reproduce → gather evidence → analyze → hypothesize → verify → fix → confirm.

## When to Use This Skill

Invoke this skill when the user says things like:
- "debug this"
- "fix this bug"
- "why is this broken"
- "investigate this error"
- "root cause analysis"
- "this doesn't work"
- "something is wrong"

## Iron Law

**NO FIXES BEFORE ROOT CAUSE IS IDENTIFIED.**

Do not skip steps. Do not patch symptoms. Fix the root cause.

## Workflow

Follow these steps in order. Do not proceed to the next step until the current one is complete.

### Step 1 — Reproduce

Ensure the issue can be consistently reproduced:
- Document exact steps to reproduce
- Note the environment, inputs, and expected vs. actual behavior
- If it cannot be reproduced, gather as much context as possible

### Step 2 — Gather evidence

Collect information about the issue:
- Error messages, stack traces, logs
- Relevant source code paths
- Recent changes that may have introduced the issue
- Metrics or monitoring data if available

### Step 3 — Analyze

Trace the data flow from input to output:
- Identify where behavior diverges from expected
- Isolate the failing component or code path
- Check related tests for insights

### Step 4 — Form hypothesis

State the suspected root cause clearly:
- What is wrong and why
- What mechanism causes the failure
- What evidence supports this hypothesis

### Step 5 — Verify hypothesis

Test the hypothesis before implementing a fix:
- Add targeted logging, write a minimal reproduction, or run a focused test
- If the hypothesis is wrong, return to Step 3
- If confirmed, proceed to the fix

### Step 6 — Implement fix

Apply the minimal fix that addresses the root cause:
- Change only what is necessary
- Do not add unrelated improvements or refactoring
- Preserve existing behavior for unaffected code paths

### Step 7 — Verify resolution

Confirm the fix works:
- Run the reproduction steps — the issue should be gone
- Run existing tests — nothing should be broken
- Add a regression test if one does not exist
- Report the results

## Output

Present findings in this structure:

### Problem
What was the issue? Steps to reproduce.

### Evidence
Logs, stack traces, metrics, relevant code paths examined.

### Root Cause
What caused the issue? Why was it missed?

### Fix
What changed? Why is this the correct fix?

### Verification
How was the fix verified? Regression test added?

## Rules

- Never guess at root cause
- Never patch symptoms
- Always document root cause in the output
- Always add a regression test when fixing a bug
- Always verify the fix resolves the issue
- If stuck after 3 failed hypotheses, escalate to the user
