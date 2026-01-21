# Claude Code Dart/Flutter Development Environment

A comprehensive agent and skill system for Dart/Flutter development with Claude Code.

## Quick Start

```bash
# Clone this repository
git clone https://github.com/ToastyToast25/claude-code-dart-flutter.git
cd claude-code-dart-flutter

# Start Claude Code
claude

# Run a slash command
/project:new
```

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| **Agents** | 34 | Specialized assistants for different tasks |
| **Skills** | 31 | Reusable code patterns with auto-activation |
| **Templates** | 10 | Boilerplate for features, BLoCs, pages, etc. |
| **Commands** | 7 | Slash commands for common workflows |
| **Hooks** | 10 | Enforcement scripts for code quality |

## Slash Commands

| Command | Description |
|---------|-------------|
| `/project:new` | Start a new project with guided setup |
| `/project:test` | Run tests with coverage reporting |
| `/project:review` | Comprehensive code review |
| `/project:deploy [env]` | Deploy to staging/production |
| `/project:fix-issue [#]` | Fix a GitHub issue by number |
| `/project:release` | Create a new release with versioning |
| `/project:validate` | Validate project configuration consistency |

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
| `lib/**/validators/*.dart` | Input validation patterns |
| `test/**/*.dart` | Test patterns |
| `pubspec.yaml` | Package management |
| `CHANGELOG.md` | Versioning patterns |
| `backend/**/*.dart` | API endpoint & security patterns |
| `routes/**/*.dart` | API endpoint & security patterns |

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
│   ├── security-audit.md
│   └── ... (30 more)
├── skills/              # 30 reusable skills
│   ├── create-bloc.md
│   ├── create-widget.md
│   ├── create-test.md
│   ├── input-security.md
│   ├── project-maintenance.md
│   └── ... (25 more)
├── commands/            # 7 slash commands
│   ├── new.md
│   ├── test.md
│   ├── deploy.md
│   ├── validate.md
│   └── ... (3 more)
├── templates/           # 6 code templates
│   ├── feature.dart.template
│   ├── bloc.dart.template
│   ├── page.dart.template
│   └── ... (3 more)
├── hooks/               # 10 enforcement scripts
│   ├── block-secrets.py
│   ├── security-scan.py
│   ├── quality-check.py
│   ├── auto-gitignore.py
│   └── ... (6 more)
├── rules/               # Mandatory code quality rules
├── memory/              # Persistent learnings
└── docs/                # Reference documentation
```

## Enforcement Rules

These rules are automatically enforced by hooks:

**PreToolUse (before execution):**
- **Blocked**: Editing `.env`, `secrets.*`, `credentials.*` files
- **Blocked**: `rm -rf /`, `git push --force main`, `DROP DATABASE`
- **Security scan**: Blocks hardcoded API keys, detects injection patterns
- **Pubspec validation**: Checks version format, warns about conflicting packages

**PostToolUse (after execution):**
- **Auto-format**: Dart files are formatted after edits
- **Quality check**: No TODO comments, dead code, or deprecated APIs
- **Auto-gitignore**: Updates .gitignore when new packages are added
- **Registry sync**: Reminds to update registry when new config files are created

**Stop (on session end):**
- **Session recording**: Captures learnings for future sessions

## Security Features

Built-in protection against common vulnerabilities:

- **XSS Prevention**: HTML sanitization, Content Security Policy patterns
- **SSRF Prevention**: URL validation, blocked private IP ranges, DNS rebinding protection
- **SQL/NoSQL Injection**: Parameterized queries, input sanitization
- **Command Injection**: Shell character filtering, safe process execution
- **Path Traversal**: Path validation, sandboxed file access
- **Input Validation**: Comprehensive validators for all user inputs

See [input-security.md](.claude/skills/input-security.md) for implementation details.

## Project Maintenance

Keep configuration files synchronized with `/project:validate`:

```bash
# Check for configuration issues
/project:validate

# Output:
# === Project Validation Report ===
# [OK] Agents: 34 (registry: 34)
# [OK] Skills: 31 (registry: 31)
# [OK] Commands: 7 (registry: 7)
# [OK] Templates: 10 (registry: 10)
# [OK] Hooks: 10 (registry: 10)
```

The validation checks:
- File counts match registry.md
- All referenced files exist
- Skills have valid frontmatter
- Hooks are properly wired in settings.json

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
