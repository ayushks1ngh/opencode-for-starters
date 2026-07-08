# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- (placeholder for future entries)

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
