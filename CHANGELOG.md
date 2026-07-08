# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- (placeholder for future entries)

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
