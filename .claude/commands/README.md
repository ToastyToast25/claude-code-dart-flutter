# Claude Code Commands

Custom slash commands available in this project.

## Available Commands

| Command | Description |
|---------|-------------|
| `/project-new` | Start a new project with guided setup |
| `/project-deploy` | Deploy to any environment |
| `/project-test` | Run tests with coverage |
| `/project-review` | Comprehensive code review |
| `/project-fix-issue` | Fix a GitHub issue |
| `/project-release` | Prepare and execute a release |
| `/project-validate` | Validate project configuration consistency |

## How Commands Work

Commands are Markdown files in this directory. When you type `/project-command-name`, Claude loads the corresponding `project-command-name.md` file and follows its instructions.

## Using Arguments

Commands can accept arguments via `$ARGUMENTS`:

```
/project-test unit           # $ARGUMENTS = "unit"
/project-fix-issue 42        # $ARGUMENTS = "42"
/project-deploy production   # $ARGUMENTS = "production"
```

## Creating New Commands

1. Create a new `.md` file in this directory
2. Name it `command-name.md`
3. Include:
   - Description of what it does
   - Usage examples
   - Workflow steps
   - Related agents/skills

## Command Template

```markdown
# Command Name

Brief description of what this command does.

## Usage
\`\`\`
/project-command-name [arguments]
\`\`\`

## Arguments

- `$ARGUMENTS` - Description of expected arguments

## Workflow

1. Step one
2. Step two
3. Step three

## Examples

\`\`\`
/project-command-name arg1
/project-command-name arg2
\`\`\`

## Related Agents

- Agent 1
- Agent 2
```

## Personal Commands

You can also create personal commands in `~/.claude/commands/` that will be available across all projects.
