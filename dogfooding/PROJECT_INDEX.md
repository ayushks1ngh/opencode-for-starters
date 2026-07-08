# Dogfooding Project Index

Tracks every dogfooding project, its findings, severity, and resulting framework changes.

| # | Project | Status | Complexity | Key Findings | Severity | Changes Implemented |
|---|---------|--------|------------|--------------|----------|---------------------|
| 001 | CLI Task Tracker | Complete | Low | BUILD_BRIEF needed, AC→task traceability needed, task dependencies needed, build handoff missing | High | v0.3.1 — BUILD_BRIEF, AC traceability, dependencies, handoff feedback loop |
| 002 | URL Shortener SaaS | Complete | Medium | Security constraints missing, operational constraints missing, interface contracts missing, module deps missing, verification criteria missing | Critical | v0.4.0 — Planner upgrade, BUILD_BRIEF v2, Planning Completeness review, dogfooding archive |
| 003 | Research Agent SDK | Complete | Medium | Interface contracts validated, dependency graphs validated, BUILD_BRIEF verification caught bug, project type matters for artifact depth | Low | All v0.4.0 features validated via Evidence Rule. New: project type-aware planning needed |
| 004 | Memory-Enabled Agent Chatbot | Complete | Medium-High | AI System classification correct, depth heuristics triggered properly, behavioral edge cases caught bug (ConnectionError retry), contract drift discovered (KeyError vs ToolResult) | Low | All v0.5.0 features validated via Evidence Rule. No core framework changes needed. New: Contract Accuracy review (single observation) |

## Status Legend
- **Complete**: All pipeline stages executed, report written
- **In Progress**: Currently being executed
- **Planned**: Not yet started
- **Archived**: Completed, data used for framework changes

## Adding a New Project

When adding a new dogfooding project:
1. Create directory `NNN-project-name/`
2. Copy all planning artifacts (PRD.md, ARCHITECTURE.md, ROADMAP.md, TASKS.md, BUILD_BRIEF.md)
3. Copy review output (REVIEW.md)
4. Write DOGFOODING_REPORT_NN.md
5. Add entry to this index
6. Add findings to FRAMEWORK_LEARNINGS.md
