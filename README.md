# Claude Code Dart/Flutter Development Environment

A comprehensive agent and skill system for Dart/Flutter development with Claude Code.

## Quick Start

```bash
# Clone this repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Start Claude Code
claude

# Run a slash command
/project:new
```

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| **Agents** | 34 | Specialized assistants for different tasks |
| **Skills** | 27 | Reusable code patterns with auto-activation |
| **Templates** | 6 | Boilerplate for features, BLoCs, pages, etc. |
| **Commands** | 5 | Slash commands for common workflows |
| **Hooks** | 5 | Enforcement scripts for code quality |

## Slash Commands

| Command | Description |
|---------|-------------|
| `/project:new` | Start a new project with guided setup |
| `/project:test` | Run tests with coverage reporting |
| `/project:review` | Comprehensive code review |
| `/project:deploy [env]` | Deploy to staging/production |
| `/project:fix-issue [#]` | Fix a GitHub issue by number |

## Key Agents

| Agent | Trigger Keywords |
|-------|------------------|
| Project Setup | "new project", "init project", "setup project" |
| Code Review | "review", "PR review", "check code" |
| Test Writer | "write tests", "add tests", "unit test" |
| Debugging | "error", "bug", "debug", "fix error" |
| Deployment | "deploy", "production", "server setup" |
| Architecture | "architecture", "structure", "layers" |
| Security Audit | "security", "vulnerabilities", "audit" |
| Performance | "slow", "performance", "optimize" |

See [.claude/registry.md](.claude/registry.md) for the complete list.

## Skills (Auto-Activated)

Skills automatically activate when you work on matching files:

| File Pattern | Skill |
|--------------|-------|
| `lib/**/bloc/*.dart` | BLoC creation patterns |
| `lib/**/models/*.dart` | Model/entity patterns |
| `lib/**/pages/*.dart` | Page scaffolding |
| `lib/**/widgets/*.dart` | Widget patterns |
| `lib/**/repositories/*.dart` | Repository pattern |
| `test/**/*.dart` | Test patterns |
| `pubspec.yaml` | Package management |

## Directory Structure

```
.claude/
├── registry.md          # Central index - START HERE
├── QUICKSTART.md        # 5-minute getting started guide
├── settings.json        # Hooks, auto-context, permissions
├── agents/              # 34 specialized agents
│   ├── project-setup.md
│   ├── code-review.md
│   ├── debugging.md
│   └── ...
├── skills/              # 27 reusable skills
│   ├── create-bloc.md
│   ├── create-widget.md
│   ├── create-test.md
│   └── ...
├── commands/            # Slash commands
│   ├── new.md
│   ├── test.md
│   ├── deploy.md
│   └── ...
├── templates/           # Code templates
│   ├── feature.dart.template
│   ├── bloc.dart.template
│   ├── page.dart.template
│   └── ...
├── hooks/               # Enforcement scripts
│   ├── block-secrets.py
│   ├── quality-check.py
│   └── ...
├── memory/              # Persistent learnings
└── docs/                # Reference documentation
```

## Enforcement Rules

These rules are automatically enforced by hooks:

- **Blocked**: Editing `.env`, `secrets.*`, `credentials.*` files
- **Blocked**: `rm -rf /`, `git push --force main`, `DROP DATABASE`
- **Auto-format**: Dart files are formatted after edits
- **Quality check**: No TODO comments, dead code, or deprecated APIs allowed

## Usage Examples

### Create a New Feature

```
Create a user authentication feature with:
- Email/password login
- OAuth (Google, Apple)
- Session management with Riverpod
```

### Fix a Bug

```
Debug this error: "Null check operator used on a null value"
at lib/features/auth/presentation/bloc/auth_bloc.dart:42
```

### Deploy to Production

```
/project:deploy production
```

### Code Review

```
Review the changes in the auth feature before merging
```

## Configuration

### MCP Servers

Edit `.mcp.json` to enable additional integrations:

```json
{
  "mcpServers": {
    "github": { "enabled": true },
    "filesystem": { "enabled": true },
    "postgres": { "enabled": false },
    "redis": { "enabled": false }
  }
}
```

### Auto-Context

Edit `.claude/settings.json` to customize which files are auto-loaded:

```json
{
  "context": {
    "autoLoad": [
      ".claude/registry.md",
      "CLAUDE.md"
    ],
    "onFileMatch": {
      "lib/**/bloc/*.dart": [".claude/skills/create-bloc.md"]
    }
  }
}
```

## Templates

Use templates for rapid scaffolding:

| Template | Use Case |
|----------|----------|
| `feature.dart.template` | Complete clean architecture feature |
| `bloc.dart.template` | BLoC with events and states |
| `repository.dart.template` | Repository with data sources |
| `page.dart.template` | Page with BLoC integration |
| `widget.dart.template` | Stateless/Stateful widgets |
| `test.dart.template` | Unit, widget, and BLoC tests |

Ask Claude: "Create a products feature using the feature template"

## Best Practices

### Be Specific
```
❌ "Create a form"
✅ "Create a login form with email/password validation using Riverpod"
```

### Use Trigger Keywords
- **Create**: "create", "add", "new", "scaffold"
- **Review**: "review", "check", "audit"
- **Test**: "test", "coverage", "verify"
- **Debug**: "debug", "fix", "error"
- **Deploy**: "deploy", "build", "release"

### Let Agents Chain
Claude automatically hands off between agents:
1. Create feature → Test writer → Code review

## Requirements

- [Claude Code CLI](https://github.com/anthropics/claude-code)
- Dart SDK 3.0+
- Flutter SDK 3.0+ (for Flutter projects)
- Python 3.8+ (for hooks)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your agent/skill to the appropriate directory
4. Update `.claude/registry.md`
5. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) for details.

---

Built with [Claude Code](https://github.com/anthropics/claude-code)
