---
description: Guidelines for maintaining Claude Code project configuration files
globs:
  - ".claude/**/*.md"
  - ".claude/**/*.json"
  - ".claude/**/*.py"
alwaysApply: false
---

# Project Maintenance

Keep all Claude Code configuration files synchronized and up to date.

## When to Use

Apply these guidelines when:
- Adding new agents, skills, commands, or templates
- Modifying settings.json
- Creating or updating hooks
- Before committing configuration changes

## Maintenance Checklist

### After Adding a New Agent

1. Create file in `.claude/agents/` with proper naming (`agent-name.md`)
2. Add entry to `.claude/registry.md` under Agents section
3. Update agent count in registry Summary section
4. Run `/project:validate` to verify

### After Adding a New Skill

1. Create file in `.claude/skills/` with proper naming (`skill-name.md`)
2. Include YAML frontmatter:
   ```yaml
   ---
   description: Brief description of what this skill does
   globs:
     - "pattern/to/match/**/*.dart"
   alwaysApply: false
   ---
   ```
3. Add entry to `.claude/registry.md` under Skills section
4. Update skill count in registry Summary section
5. If skill should auto-load, add pattern to `.claude/settings.json` `onFileMatch`
6. Run `/project:validate` to verify

### After Adding a New Command

1. Create file in `.claude/commands/` with proper naming (`command-name.md`)
2. Add entry to `.claude/registry.md` under Commands section
3. Update command count in registry Summary section
4. Run `/project:validate` to verify

### After Adding a New Hook

1. Create Python file in `.claude/hooks/`
2. Add hook configuration to `.claude/settings.json` under appropriate section:
   - `PreToolUse` - runs before tool execution (can block)
   - `PostToolUse` - runs after tool execution
   - `Stop` - runs when session ends
3. Update hook count in registry Summary section
4. Run `/project:validate` to verify

### After Adding a New Template

1. Create file in `.claude/templates/`
2. Add entry to `.claude/registry.md` under Templates section
3. Update template count in registry Summary section
4. Run `/project:validate` to verify

## Registry Update Locations

When updating `.claude/registry.md`, modify these sections:

### 1. Summary Section (Top)
```markdown
## Summary

- **X** specialized agents
- **Y** skills
- **Z** commands
- **N** templates
- **M** hooks
```

### 2. Directory Structure
```markdown
## Directory Structure

.claude/
├── agents/          # X agent definitions
├── skills/          # Y skill guides
├── commands/        # Z slash commands
├── templates/       # N code templates
├── hooks/           # M automation hooks
```

### 3. Relevant Category Section
Add entry under appropriate heading (Agents, Skills, Commands, etc.)

## Settings.json Patterns

### Adding Auto-Load Skills

```json
{
  "context": {
    "onFileMatch": {
      "lib/**/new_pattern/*.dart": [".claude/skills/relevant-skill.md"]
    }
  }
}
```

### Adding New Hooks

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "tool == 'Edit' && tool_input.file_path matches '\\.dart$'",
        "command": ["python", ".claude/hooks/new-hook.py"],
        "description": "Description of what hook does"
      }
    ]
  }
}
```

## Validation

Always run validation after changes:

```
/project:validate
```

Or run the script directly:

```bash
python .claude/hooks/validate-project.py
```

## Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Count mismatch | Added file but didn't update registry | Update Summary section counts |
| Missing file | Registry references non-existent file | Create file or remove reference |
| Hook not running | Not wired in settings.json | Add to appropriate hooks section |
| Skill not loading | Missing from onFileMatch | Add glob pattern to settings.json |
| Invalid frontmatter | Missing required fields | Add description and globs/alwaysApply |

## Best Practices

1. **Commit validation**: Run `/project:validate` before every commit
2. **Atomic updates**: Update all related files in a single commit
3. **Descriptive names**: Use clear, consistent naming conventions
4. **Document changes**: Note significant changes in relevant README files
5. **Test hooks**: Verify hooks work by triggering their conditions
