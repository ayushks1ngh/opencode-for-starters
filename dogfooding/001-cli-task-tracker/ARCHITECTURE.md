# Architecture: CLI Task Tracker

## Tech Stack
- Language: Python 3.8+
- Dependencies: None (stdlib only)
- Testing: pytest
- Packaging: pip-installable via setup.py or pyproject.toml

## Data Model

```python
@dataclass
class Task:
    id: int              # auto-incrementing
    title: str           # required
    description: str     # optional, defaults to ""
    status: str          # "todo" | "in-progress" | "done"
    priority: str        # "low" | "medium" | "high"
    created_at: str      # ISO 8601 timestamp
    updated_at: str      # ISO 8601 timestamp
```

## Storage Layer

```
~/.task-tracker/tasks.json
```

Format: JSON array of task objects.
- Read on every command, write on mutations
- File auto-created on first use with `[]`
- Lock-free (single-user CLI, no concurrency)

## CLI Design

```
task-tracker add <title> [--description <text>] [--priority <low|medium|high>]
task-tracker list [--status <status>] [--priority <priority>]
task-tracker update <id> [--title <text>] [--description <text>] [--status <status>] [--priority <priority>]
task-tracker delete <id>
task-tracker --help
```

Exit codes: 0 = success, 1 = user error, 2 = system error.

## Project Structure

```
task_tracker/
  __init__.py      # package marker, version
  __main__.py      # entry point: `python -m task_tracker`
  cli.py           # argument parsing, command dispatch
  storage.py       # JSON file read/write
  models.py        # Task dataclass, validation
  formatter.py     # table formatting for output
tests/
  test_storage.py
  test_cli.py
  test_models.py
  test_formatter.py
pyproject.toml     # packaging config
```

## Data Flow

```
CLI args → cli.py (argparse) → storage.py (read JSON)
                              → models.py (validate/transform)
                              → storage.py (write JSON)
                              → formatter.py (format output) → stdout
```

## Error Handling
- File not found → auto-create
- Corrupt JSON → print clear error, exit 2
- Invalid task ID → print error, exit 1
- Invalid status/priority → print valid options, exit 1
