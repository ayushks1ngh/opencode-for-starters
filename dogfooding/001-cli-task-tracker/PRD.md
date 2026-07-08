# PRD: CLI Task Tracker

## Problem Statement
Developers and power users need a simple, zero-dependency CLI tool to track tasks from the terminal. Existing solutions (Todoist, Notion, Jira) are heavy, require GUIs, or have complex APIs.

## Target Audience
- Developers who work in the terminal
- Power users who want lightweight task tracking
- Anyone who prefers markdown/data files over SaaS

## User Stories

### MVP (Must Have)
1. As a user, I can add a task with a title so I can capture tasks quickly
2. As a user, I can list all tasks so I can see what's pending
3. As a user, I can filter tasks by status so I can focus on todo/done items
4. As a user, I can update a task's status so I can track progress
5. As a user, I can delete a task so I can remove completed or unwanted items
6. As a user, my tasks persist between sessions so I don't lose data

### Enhancement (Should Have)
7. As a user, I can set task priority so I can triage work
8. As a user, I can edit task fields (title, description, priority) after creation
9. As a user, I can view tasks in a formatted table so they're easy to read

### Future (Could Have)
10. As a user, I can use tags/categories so I can organize tasks by project
11. As a user, I can set due dates so I can track deadlines
12. As a user, I can search tasks by keyword so I can find specific items

## Acceptance Criteria

### AC-1: Add Task
- Command: `task-tracker add "Buy groceries"`
- Creates task with id (incrementing), title="Buy groceries", status="todo", priority="medium", created_at and updated_at timestamps
- Outputs confirmation with task ID

### AC-2: List Tasks
- Command: `task-tracker list`
- Shows all tasks in a table: ID, Title, Status, Priority, Created
- `task-tracker list --status todo` filters by status
- `task-tracker list --priority high` filters by priority
- Empty list shows "No tasks found" message

### AC-3: Update Task
- Command: `task-tracker update 1 --status done`
- Updates the specified field(s)
- Returns error if task ID doesn't exist
- Outputs confirmation with updated fields

### AC-4: Delete Task
- Command: `task-tracker delete 1`
- Removes task from storage
- Returns error if task ID doesn't exist
- Outputs confirmation of deletion

### AC-5: Persistence
- Tasks stored in ~/.task-tracker/tasks.json
- Data survives across terminal sessions
- File created on first use with empty array

## Non-Requirements
- No daemon/server mode
- No sync/collaboration
- No GUI
- No cloud backups
- No natural language parsing
