# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.3.1] - 2026-07-08

### Added

- **BUILD_BRIEF.md generation**: Planner agent now produces a phase-specific implementation brief that distills PRD + ARCHITECTURE + ROADMAP + TASKS into a single actionable document
- **AC→Task traceability**: TASKS.md tasks now annotate which acceptance criteria they satisfy (e.g. `(AC-1, AC-5)`), enabling coverage verification
- **Explicit task dependencies**: TASKS.md now requires `depends_on` declarations for every task, enabling correct execution ordering
- **Cross-reference validation**: Planner validates PRD↔ROADMAP consistency, AC→task coverage, and dependency completeness before delivery
- **Plan Accuracy review dimension**: Review skill gains a 7th dimension checking implementation against PRD, ARCHITECTURE, and discovered plan gaps
- **Build-to-Plan feedback loop**: Implementation specialist documents plan gaps discovered during coding; tech lead updates artifacts and passes findings to review

### Changed

- **agent/planner.md**: Added BUILD_BRIEF.md to persistent artifacts, AC tagging in PRD, phase mapping in ROADMAP, AC references and dependencies in TASKS, post-generation validation step
- **skills/plan/SKILL.md**: Added BUILD_BRIEF.md to outputs, AC traceability and dependency requirements, cross-reference validation step, updated description
- **skills/review/SKILL.md**: Added Plan Accuracy dimension with 6 checkpoints
- **agent/implementation-specialist.md**: Added Plan Gap Reporting section with structured output format
- **agent/tech-lead.md**: Added Phase Brief Management section, Build-to-Plan Feedback Loop section, Plan Gap Processing in operational protocol
- **AGENTS.md**: Updated planner and implementation-specialist descriptions
- **VERSION**: 0.3.0 → 0.3.1

## [0.3.0] - 2026-07-08

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
