---
name: docs
description: >-
  Generate and maintain project documentation following engineering best
  practices. Creates README, architecture documentation, API documentation,
  setup guides, and onboarding guides. Reads existing code and documentation
  first, identifies gaps, and produces clear, example-driven content. Use
  when asked to "document this", "write docs", "update README", or "create
  documentation".
---

# Docs

Generate and maintain project documentation.

## When to Use This Skill

Invoke this skill when the user says things like:
- "document this feature"
- "write docs for this"
- "update the readme"
- "create documentation"
- "write an api reference"
- "document the architecture"
- "create a setup guide"

## Approach

1. Read existing code and documentation in the relevant area first
2. Identify gaps, stale content, and inconsistencies
3. Generate or update documentation following structured formats
4. Cross-reference with existing docs for consistency
5. Flag any issues found in existing documentation

## Documentation Types

| Type | Purpose | Audience |
|------|---------|----------|
| README | Project overview, quick start | New users |
| Architecture | System design, component map, data flow | Contributors |
| API | Endpoints, parameters, examples, responses | Integrators |
| Setup | Installation, configuration, prerequisites | Developers |
| Onboarding | Getting started guide, common workflows | New team members |

## Output Structure

Each document should follow this structure:

### Purpose
What is this document for? Who should read it? What will they learn?

### Usage
How to use the documented system. Include concrete, runnable examples.

### Examples
Realistic examples that demonstrate common workflows. Show inputs and expected outputs.

### Reference
Complete reference information: configuration options, API parameters, edge cases, error codes. Include tables where appropriate.

## Quality Check

After generating documentation, invoke the **writing-guidelines** skill to review the output for style, voice, and structure compliance against Vercel's writing handbook (80+ rules covering tone, structure, code samples, typography). Fix any issues found before presenting the final documentation.

## Rules

- Read the existing codebase before writing
- Document what exists, not what should exist
- Use clear, concise engineering language
- Include runnable examples where possible
- Link to related documentation
- Do not generate code or modify source files
- Flag inconsistencies found in existing docs as part of the output
- If the project has a CONTRIBUTING.md, follow the documented conventions
