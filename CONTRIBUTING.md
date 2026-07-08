# Contributing to opencode-for-starters

Thanks for your interest in contributing! This document covers everything you need to know to get started.

## Project Overview

opencode-for-starters is a starter kit that turns [opencode](https://opencode.ai) into a full development team. When cloned into a project as `.opencode/`, it provides:

- **8 specialized agents** (tech-lead, planner, requirements-clarifier, architect-designer, implementation-specialist, test-automation-engineer, scan, big-pickle-simple-tasks)
- **Slash commands** (`/build`, `/scan`)
- **Skill packs** (e.g., `ship` for one-command PRs)
- **Pipeline orchestration** via AGENTS.md instructions

All files use plain markdown with YAML frontmatter. No build tools, no compilers, no dependencies.

## Repository Structure

```
opencode.json            # Main config: model, instructions, agent overrides
AGENTS.md                # Pipeline rules — loaded every session
VERSION                  # Current release version
CHANGELOG.md             # Release history
CONTRIBUTING.md          # This file
README.md                # Project documentation
setup.sh                 # Bootstrap script
LICENSE                  # MIT license
agent/                   # Agent definitions (8 agents)
  tech-lead.md           #   Orchestrator — routes work
  planner.md             #   Generates plans + 5 artifacts
  requirements-clarifier.md
  architect-designer.md
  implementation-specialist.md
  test-automation-engineer.md
  scan.md                #   Security vulnerability scanner
  big-pickle-simple-tasks.md
command/                 # Slash commands (5 commands)
  build.md
  scan.md
  plan.md
  investigate.md
  review.md
skills/                  # Skill packs (7 skills)
  plan/SKILL.md          #   Planning workflow
  investigate/SKILL.md   #   Debugging workflow
  review/SKILL.md        #   Code review workflow (8 dimensions)
  docs/SKILL.md          #   Documentation workflow
  ship/SKILL.md          #   One-command PR pipeline
  web-design-guidelines/ #   UI/accessibility review (100+ rules)
  writing-guidelines/    #   Documentation style review (80+ rules)
dogfooding/              # Dogfooding archive
  PROJECT_INDEX.md
  FRAMEWORK_LEARNINGS.md
  001-cli-task-tracker/
  002-url-shortener/
  003-research-agent-sdk/
  004-ai-chatbot/
```

## How Agents Work

Each agent is a markdown file in `agent/` with YAML frontmatter:

```yaml
---
description: What this agent does and when to use it.
mode: primary         # or "subagent"
tools:                # optional — tool restrictions
  bash: false
  edit: false
---
Instructions for the agent...
```

Agents are auto-discovered by opencode when placed in `agent/`. The `mode` field determines whether the agent appears as a primary agent (can be switched to) or a subagent (only invoked via @-mention or by other agents).

## How Commands Work

Commands are markdown files in `command/` that map to agents:

```yaml
---
description: What the command does.
agent: build          # which agent handles this command
---

Instructions for what the command should do.
```

Commands are invoked via `/command-name` in an opencode session.

## How Skills Work

Skills are `SKILL.md` files in `skills/` that provide structured, multi-step workflows. They use the [opencode SKILL.md format](https://opencode.ai/docs/concepts/skills) with YAML frontmatter (name, description, triggers) and step-by-step instructions.

Skills are triggered by natural language (e.g., saying "ship it" triggers the `ship` skill).

## How to Test Changes

1. **Clone this repo** into a test project as `.opencode/`:
   ```bash
   git clone https://github.com/ayushks1ngh/opencode-for-starters.git /tmp/test-project/.opencode
   ```

2. **Verify config loads**:
   ```bash
   opencode debug config
   ```
   Check that all agents, commands, and instructions are listed.

3. **Verify a specific agent**:
   ```bash
   opencode debug agent <name>
   ```

4. **Verify a specific skill**:
   ```bash
   opencode debug skill <name>
   ```

5. **Start a session** and test the changed behavior:
   ```bash
   opencode /tmp/test-project
   ```

## Pull Request Process

1. Create a branch from `main` with a descriptive name (`feat/skill-name`, `fix/issue-description`, `docs/section-name`)
2. Make your changes following the coding and documentation standards below
3. Test that the config loads correctly (see testing section above)
4. Update the VERSION file following semantic versioning:
   - **Patch** (x.x.N): Bug fixes, documentation updates, minor improvements
   - **Minor** (x.N.0): New features, new agents, new skills
   - **Major** (N.0.0): Stable release, breaking changes
5. Add a CHANGELOG entry for the new version
6. Open a PR against `main` with a clear description of what changed and why
7. Ensure the PR template checklist is complete

## Coding Standards

- **Keep it simple**: No build tools, no compilers, no package.json. All files are markdown.
- **One responsibility per file**: Each agent, command, or skill does one thing.
- **Consistent frontmatter**: All YAML frontmatter uses `description: >-` for multi-line descriptions.
- **No hardcoded models**: Agents should inherit the model from `opencode.json` unless there is a specific reason to override.
- **Clear scope boundaries**: Subagents that shouldn't write code or edit files must declare those restrictions in their frontmatter.

## Documentation Standards

- **Keep comments minimal**: Agent instructions should be self-documenting. Avoid inline comments.
- **Use consistent headings**: `##` for top-level sections, `###` for subsections.
- **Code blocks**: Use fenced code blocks with language tags (```bash, ```json, ```yaml, ```).
- **Active voice**: Write instructions as direct commands ("Run this command", not "This command should be run").
- **Lists**: Use `-` for unordered lists, `1.` for ordered steps.
