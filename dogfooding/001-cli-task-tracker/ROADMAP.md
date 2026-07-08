# Roadmap: CLI Task Tracker

## Phase 1: MVP (Day 1)
- [ ] Core data model (Task dataclass)
- [ ] JSON storage layer (read/write, auto-create)
- [ ] CLI: add, list, delete commands
- [ ] Formatter: basic table output
- [ ] Entry point: `python -m task_tracker` and installable CLI

## Phase 2: Rich Functionality (Day 2)
- [ ] Update command (all fields)
- [ ] List filters (--status, --priority)
- [ ] Description field support
- [ ] Priority field support
- [ ] Error handling polish

## Phase 3: Testing & Polish (Day 3)
- [ ] Unit tests for all modules
- [ ] Edge case handling (empty file, corrupt data, special chars in title)
- [ ] man page or --help documentation
- [ ] CI pipeline (GitHub Actions)

## Phase 4: Release (Day 4)
- [ ] PyPI packaging
- [ ] Homebrew formula (optional)
- [ ] Changelog
