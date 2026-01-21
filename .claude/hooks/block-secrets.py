#!/usr/bin/env python3
"""
Hook: Block access to secret files
Exit codes:
  0 = Allow operation
  2 = Block operation (passes message to Claude)
"""

import json
import sys
import os

def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except:
        hook_input = {}

    tool_input = hook_input.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    # Patterns to block
    blocked_patterns = [
        '.env',
        '.env.local',
        '.env.development',
        '.env.staging',
        '.env.production',
        'secrets.',
        'credentials.',
        '.secret',
        'api_key',
        'private_key',
    ]

    # Check if file matches blocked patterns
    file_lower = file_path.lower()
    file_name = os.path.basename(file_lower)

    for pattern in blocked_patterns:
        if pattern in file_name or file_name.startswith(pattern):
            # Output JSON response to block
            response = {
                "block": True,
                "message": f"BLOCKED: Cannot edit '{file_path}' - this file may contain secrets. "
                          f"Secret files must be edited manually by the user for security reasons."
            }
            print(json.dumps(response))
            sys.exit(2)  # Exit code 2 = block operation

    # Allow operation
    sys.exit(0)

if __name__ == "__main__":
    main()
