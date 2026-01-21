# Claude Code Hooks

This directory contains enforcement hooks that run automatically during Claude Code operations.

## How Hooks Work

Hooks are Python scripts that execute at specific points in Claude's operation cycle. They can:
- **Allow** operations (exit code 0)
- **Warn** about issues (exit code 1, non-blocking)
- **Block** operations (exit code 2, operation prevented)

## Available Hooks

### PreToolUse Hooks

These run **before** a tool operation:

| Hook | Purpose |
|------|---------|
| `block-secrets.py` | Prevents editing `.env` and secret files |
| `block-dangerous.py` | Prevents dangerous shell commands |
| `quality-check.py` | Checks code for quality violations |

### PostToolUse Hooks

These run **after** a tool operation:

| Hook | Purpose |
|------|---------|
| `format-dart.py` | Auto-formats Dart files after editing |

### Stop Hooks

These run when a conversation ends:

| Hook | Purpose |
|------|---------|
| `session-end.py` | Records session marker for learning system |

## Hook Input Format

Hooks receive JSON on stdin:

```json
{
  "tool": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.dart",
    "old_string": "...",
    "new_string": "..."
  }
}
```

## Hook Output Format

Hooks should print JSON to stdout:

```json
{
  "block": true,
  "message": "Reason shown to Claude",
  "feedback": "Info message",
  "continue": true
}
```

## Exit Codes

| Code | Meaning | Effect |
|------|---------|--------|
| 0 | Success | Operation allowed |
| 1 | Warning | Operation allowed, message shown |
| 2 | Block | Operation prevented, message to Claude |

## Configuration

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "tool == 'Edit'",
        "command": ["python", ".claude/hooks/block-secrets.py"]
      }
    ]
  }
}
```

## Adding New Hooks

1. Create a Python script in this directory
2. Handle JSON input from stdin
3. Output JSON response to stdout
4. Use appropriate exit code
5. Add configuration to `settings.json`

## Testing Hooks

```bash
# Test a hook manually
echo '{"tool": "Edit", "tool_input": {"file_path": ".env"}}' | python block-secrets.py
echo $?  # Should be 2 (blocked)
```
