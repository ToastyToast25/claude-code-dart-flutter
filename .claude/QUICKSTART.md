# Quick Start Guide

Get started with the Claude Code Dart development environment in 5 minutes.

## Overview

This project includes a comprehensive agent/skill system for Dart/Flutter development:

- **34 Agents** - Specialized assistants for different tasks
- **27 Skills** - Reusable code patterns and templates
- **5 Slash Commands** - Quick workflows
- **Enforcement Hooks** - Automated code quality checks

## First Steps

### 1. Start a New Project

```
/project:new
```

Or ask: "Create a new Flutter app with authentication"

### 2. Create Features

Ask Claude to create components:

- "Create a user authentication feature"
- "Create a product listing page"
- "Create a BLoC for cart management"
- "Create an API endpoint for orders"

### 3. Run Tests

```
/project:test
```

Or ask: "Run tests with coverage"

### 4. Deploy

```
/project:deploy production
```

## Key Agents

| Ask for... | Agent Used |
|------------|------------|
| "Set up a new project" | Project Setup Agent |
| "Review my code" | Code Review Agent |
| "Write tests for..." | Test Writer Agent |
| "Debug this error" | Debugging Agent |
| "Optimize performance" | Performance Agent |
| "Deploy to..." | Deployment Agent |

## Key Skills

Skills are auto-activated when you work on matching files:

| Working on... | Skill Activated |
|---------------|-----------------|
| `lib/**/models/*.dart` | create-model |
| `lib/**/bloc/*.dart` | create-bloc |
| `lib/**/pages/*.dart` | create-page |
| `test/**/*.dart` | create-test |
| `pubspec.yaml` | add-package |

## Slash Commands

| Command | Description |
|---------|-------------|
| `/project:new` | Start new project with guided setup |
| `/project:test` | Run tests with coverage |
| `/project:review` | Comprehensive code review |
| `/project:deploy` | Deploy to any environment |
| `/project:fix-issue 123` | Fix a GitHub issue |

## Rules Enforcement

These rules are automatically enforced by hooks:

- **Blocked**: Editing `.env` or secrets files
- **Blocked**: `rm -rf /`, force push to main, DROP DATABASE
- **Auto-format**: Dart files formatted after edits
- **Quality check**: No TODO comments, dead code, or deprecated APIs

## Directory Structure

```
.claude/
├── registry.md          # START HERE - Agent/skill index
├── context.md           # Project context and notes
├── settings.json        # Hooks and permissions
├── QUICKSTART.md        # This file
├── agents/              # 34 specialized agents
├── skills/              # 27 reusable skills
├── commands/            # Slash commands
├── hooks/               # Enforcement scripts
├── rules/               # Code quality rules
├── memory/              # Persistent learnings
└── learnings/           # Knowledge base
```

## Tips

### Be Specific
Instead of: "Create a form"
Say: "Create a login form with email/password validation using Riverpod"

### Use Trigger Keywords
Agents activate on keywords like:
- "create", "add", "new" → Creation agents
- "review", "check", "audit" → Review agents
- "test", "coverage" → Testing agents
- "debug", "fix", "error" → Debugging agents
- "deploy", "build", "release" → Deployment agents

### Chain Tasks
Claude will hand off between agents as needed:
1. "Create a user feature" → Feature creation
2. Automatically → Test writer for the feature
3. Automatically → Code review

### Ask for Help
- "What agents are available?"
- "How do I create a BLoC?"
- "What's the project architecture?"

## Common Workflows

### Add a New Feature
1. "Create a [feature_name] feature with [requirements]"
2. Claude creates data/domain/presentation layers
3. Tests are auto-generated
4. Code is auto-formatted

### Fix a Bug
1. "Debug this error: [error message]"
2. Claude analyzes and identifies root cause
3. Proposes fix with explanation
4. Tests updated if needed

### Deploy
1. `/project:deploy staging`
2. Claude runs tests, builds, and deploys
3. Provides deployment URL and status

## Need Help?

- Read the full registry: `.claude/registry.md`
- Check agent docs: `.claude/agents/[agent-name].md`
- Check skill docs: `.claude/skills/[skill-name].md`
- Ask Claude: "Explain how [feature] works"
