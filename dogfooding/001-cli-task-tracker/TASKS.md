# Tasks: CLI Task Tracker

## Phase 1: MVP

### T1.1: Project skeleton
- [ ] Create directory structure: `task_tracker/`, `tests/`
- [ ] Create `pyproject.toml` with build config
- [ ] Create `task_tracker/__init__.py` with version
- [ ] Create `task_tracker/__main__.py` entry point
- [ ] Verify `python -m task_tracker --help` works

### T1.2: Task data model
- [ ] Create `task_tracker/models.py`
- [ ] Define `Task` dataclass with all fields
- [ ] Add validation for status and priority enums
- [ ] Add `to_dict()` and `from_dict()` methods

### T1.3: Storage layer
- [ ] Create `task_tracker/storage.py`
- [ ] Implement `load_tasks()` — reads JSON, auto-creates file
- [ ] Implement `save_tasks()` — writes JSON
- [ ] Implement `generate_id()` — auto-increment from existing tasks
- [ ] Handle corrupt JSON with clear error

### T1.4: CLI — add and list
- [ ] Create `task_tracker/cli.py` with argparse
- [ ] Implement `add` command with title, optional description/priority
- [ ] Implement `list` command (all tasks)
- [ ] Create `task_tracker/formatter.py` with table output
- [ ] Wire CLI dispatch in `__main__.py`

### T1.5: CLI — delete
- [ ] Implement `delete` command in cli.py
- [ ] Handle non-existent ID error
- [ ] Confirm deletion output

## Phase 2: Rich Functionality

### T2.1: CLI — update
- [ ] Implement `update` command with --title, --description, --status, --priority
- [ ] Validate status/priority on update
- [ ] Handle non-existent ID

### T2.2: List filters
- [ ] Add --status filter to list command
- [ ] Add --priority filter to list command
- [ ] Support combined filters

### T2.3: Error handling polish
- [ ] Consistent error messages across all commands
- [ ] Exit codes: 0 success, 1 user error, 2 system error
- [ ] Color output for errors (optional)

## Phase 3: Testing & Polish

### T3.1: Unit tests
- [ ] `tests/test_models.py` — Task creation, validation, serialization
- [ ] `tests/test_storage.py` — load/save, auto-create, corrupt data
- [ ] `tests/test_cli.py` — arg parsing, command dispatch
- [ ] `tests/test_formatter.py` — table output, empty list

### T3.2: Edge cases
- [ ] Special characters in title (quotes, emoji, newlines)
- [ ] Empty tasks.json (valid JSON, empty array)
- [ ] Very long titles (truncation in display)
- [ ] Missing `~/.task-tracker/` directory
- [ ] Read-only file permissions

### T3.3: Documentation
- [ ] README with install/usage/example
- [ ] --help text for all commands
- [ ] Example output in documentation
