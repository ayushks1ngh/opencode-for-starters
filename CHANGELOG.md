# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.5.0] - 2026-07-08

### Added

- **Adaptive Planning**: Planner classifies projects into 5 types (CLI Tool, Application/SaaS, Library/SDK, AI System, Infrastructure Platform) before generating artifacts — different project types receive different planning depth based on measurable triggers
- **Artifact Depth Heuristics**: Each artifact (PRD, ARCHITECTURE, TASKS, BUILD_BRIEF) has 3-5 depth levels with explicit required-when conditions (e.g. interface contracts required when ≥3 modules or public API surface; behavioral edge cases required when stateful or concurrent components). Quick-reference depth map for each project type.
- **Behavioral Edge Case Specifications**: Interface contracts extended with behavioral expectations — duplicate calls, invalid inputs, concurrency, idempotency, retry behavior, lifecycle state transitions, resource limits. Required for ARCHITECTURE L3+.
- **Plan validation extended**: 3 new post-generation checks — behavioral edge cases present (L3+), depth justification recorded, classification recorded (14 total checks).

### Changed

- **agent/planner.md**: Added Project Classification section (mandatory first step), Artifact Depth Heuristics (4 tables with L1-L5 depth definitions), Behavioral Edge Cases (7 dimensions per component), Classification→Depth quick-reference mapping. Post-generation validation expanded from 11 to 14 checks.
- **skills/plan/SKILL.md**: Step 1 now classifies project type and collects depth triggers before requirements analysis. Step 2 passes classification context to planner. Step 3 generates artifacts at determined depth with per-type reference table. Step 4 validates depth-appropriate content. Step 5 reports classification and depth rationale.
- **AGENTS.md**: Updated planner description to mention adaptive depth, behavioral edge cases, and measurable heuristics.
- **README.md**: Updated planner description, version badge, feature tables, roadmap section for v0.5.0.
- **dogfooding/FRAMEWORK_LEARNINGS.md**: Updated Planned Improvements and Evidence Status tables with v0.5.0 features.
- **VERSION**: 0.4.0 → 0.5.0

### Infrastructure

- No new agents, skills, or commands — zero scope creep (all changes extend existing planner-driven workflow)

## [0.4.0] - 2026-07-08

### Added

- **Planning Maturity framework**: Planner now generates security constraints, operational constraints, interface contracts, and module dependency graphs — all validated prior to implementation
- **Security constraints in PRD**: Explicit documentation of input validation rules, allowed protocols/schemes, auth requirements, trust boundaries, and security assumptions
- **Operational constraints in PRD**: Explicit documentation of runtime assumptions, storage locations, database config, host binding, environment requirements, and deployment assumptions
- **Interface contracts in ARCHITECTURE**: Component-level specifications with function signatures, return types, error conventions, status code conventions, and header requirements
- **Module dependency graphs in ARCHITECTURE**: Explicit import/call dependency diagrams showing initialization order and preventing circular dependencies
- **BUILD_BRIEF v2 — Verification section**: Every acceptance criterion now includes verification steps, validation commands, expected outcomes, and definition of done — enabling verification without re-reading other artifacts
- **Traceability matrix in TASKS**: Reverse mapping of AC→tasks for impact analysis (e.g. "if AC-5 changes, which tasks are affected?")
- **Planning Completeness review dimension**: Review now evaluates whether security constraints, operational assumptions, interface contracts, dependency graphs, and verification steps were documented and implemented correctly
- **Dogfooding archive system**: `dogfooding/` directory with PROJECT_INDEX.md (project tracker), FRAMEWORK_LEARNINGS.md (confirmed/invalid assumptions, bottlenecks, open questions, evidence rules), and per-project artifact archives for 001-cli-task-tracker and 002-url-shortener
- **Evidence Rule**: Framework governance — improvements validated by two or more dogfooding projects OR blocking completion; single-observations recorded but not automatically implemented

### Changed

- **agent/planner.md**: Complete rewrite of Persistent Artifacts section — added Security Constraints, Operational Constraints, Interface Contracts, Module Dependency Graph, Traceability Matrix, BUILD_BRIEF v2 Verification section, expanded Post-Generation Validation from 5 to 11 checks
- **skills/plan/SKILL.md**: Updated all artifact generation steps to include security, operational, interface, and dependency documentation; BUILD_BRIEF now requires verification section; validation step expanded to 9 checks
- **skills/review/SKILL.md**: Added Planning Completeness as an 8th review dimension with 7 checkpoints covering security, operational, interface, dependency, and verification completeness
- **AGENTS.md**: Added Framework Governance section with Evidence Rule reference; updated planner description
- **README.md**: Updated for Planning Maturity release; added Planning Completeness to review description; updated roadmap
- **dogfooding/**: Created archive system with PROJECT_INDEX.md, FRAMEWORK_LEARNINGS.md, and per-project directories
- **VERSION**: 0.3.1 → 0.4.0

## [0.3.1] - 2026-07-08

### Added

- **Planner agent**: New `@planner` primary agent — requirements analysis, scope definition, milestone planning, risk identification. Generates persistent project artifacts (PRD.md, ARCHITECTURE.md, ROADMAP.md, TASKS.md)
- **Plan skill**: Structured workflow for converting raw ideas into executable engineering plans with file-based outputs
- **Investigate skill**: Systematic debugging workflow — reproduce, gather evidence, analyze, hypothesize, fix, verify. No fixes before root cause
- **Review skill**: Pre-merge code review across 6 dimensions (architecture, security, testing, performance, maintainability, DX) with severity-ranked findings
- **Docs skill**: Documentation generation for README, architecture, API, setup guides, and onboarding
- **Slash commands**: `/plan`, `/investigate`, `/review` — thin wrappers that invoke the corresponding skill
- **Pipeline enforcement**: Tech lead agent updated with soft pipeline gating — recommends Plan → Build → Review → Ship order but does not block

### Changed

- **AGENTS.md**: Restructured with primary vs specialist agent categories, new workflow rules, new commands table
- **README.md**: New workflow philosophy (Idea → Plan → Architecture → Implementation → Testing → Review → Ship), updated agent/command/skill tables, new usage examples, updated repository structure map
- **VERSION**: 0.2.0 → 0.3.0

### Infrastructure

- 4 new skill directories (plan, investigate, review, docs)
- 3 new command definitions (plan, investigate, review)
- 1 new agent definition (planner)

[0.4.0]: https://github.com/ayushks1ngh/opencode-for-starters/releases/tag/v0.4.0
[0.3.1]: https://github.com/ayushks1ngh/opencode-for-starters/releases/tag/v0.3.1
[0.3.0]: https://github.com/ayushks1ngh/opencode-for-starters/releases/tag/v0.3.0

## [0.2.0] - 2026-07-08

### Added

- **Agent system**: 7 specialized agents (tech-lead, requirements-clarifier, architect-designer, implementation-specialist, test-automation-engineer, scan, big-pickle-simple-tasks)
- **Default agent orchestration**: Build agent overridden with pipeline-aware prompt that routes work through specialists automatically
- **Slash commands**: `/build` (auto-detects project type), `/scan` (security auditing)
- **Ship skill**: One-command commit, push, PR, and review trigger workflow
- **AGENTS.md orchestration**: Pipeline instructions loaded as session instructions
- **Global installation**: Clone to `~/.config/opencode/` for system-wide use
- **Local installation**: Clone to `.opencode/` for per-project use
- **Remote paste-link**: Instructions loaded from GitHub raw URL (no clone needed)
- **Agent definitions**: YAML frontmatter with mode, tools, permissions, and descriptions
- **MIT license**: Open source licensing

### Infrastructure

- `VERSION` file at 0.2.0
- `CHANGELOG.md` with Keep a Changelog format
- `CONTRIBUTING.md` contributor guide
- GitHub issue templates (bug report, feature request)
- GitHub pull request template
- `setup.sh` bootstrap script with global, local, and auto modes

[0.2.0]: https://github.com/ayushks1ngh/opencode-for-starters/releases/tag/v0.2.0
