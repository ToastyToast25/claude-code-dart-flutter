#!/usr/bin/env python3
"""
Hook: Block dangerous commands
Exit codes:
  0 = Allow operation
  2 = Block operation (passes message to Claude)
"""

import json
import sys
import re

def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except:
        hook_input = {}

    tool_input = hook_input.get('tool_input', {})
    command = tool_input.get('command', '')

    # Dangerous patterns to block
    dangerous_patterns = [
        (r'rm\s+-rf\s+/', "Recursive delete from root"),
        (r'rm\s+-rf\s+~', "Recursive delete from home"),
        (r'rm\s+-rf\s+\*', "Recursive delete wildcard"),
        (r'git\s+push.*--force.*main', "Force push to main"),
        (r'git\s+push.*--force.*master', "Force push to master"),
        (r'git\s+push\s+-f.*main', "Force push to main"),
        (r'git\s+push\s+-f.*master', "Force push to master"),
        (r'DROP\s+DATABASE', "Drop database"),
        (r'DROP\s+TABLE', "Drop table"),
        (r'TRUNCATE\s+TABLE', "Truncate table"),
        (r'DELETE\s+FROM\s+\w+\s*;?\s*$', "Delete all rows without WHERE"),
        (r'chmod\s+-R\s+777', "Recursive chmod 777"),
        (r':(){ :|:& };:', "Fork bomb"),
        (r'mkfs\.', "Format filesystem"),
        (r'dd\s+if=.*of=/dev/', "Direct disk write"),
    ]

    # Check command against patterns
    for pattern, description in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            response = {
                "block": True,
                "message": f"BLOCKED: Dangerous command detected - {description}. "
                          f"Command: '{command[:100]}...' "
                          f"This operation could cause irreversible damage and must be run manually if needed."
            }
            print(json.dumps(response))
            sys.exit(2)

    # Allow operation
    sys.exit(0)

if __name__ == "__main__":
    main()
