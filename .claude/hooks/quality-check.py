#!/usr/bin/env python3
"""
Hook: Check code quality rules before edits
Can be used as PreToolUse hook for stricter enforcement

Exit codes:
  0 = Allow operation
  1 = Warning (non-blocking)
  2 = Block operation
"""

import json
import sys
import re

def check_content_for_violations(content: str) -> list:
    """Check content for code quality violations."""
    violations = []

    # Patterns that indicate violations
    checks = [
        # Backward compatibility patterns
        (r'//\s*(?:TODO|FIXME):\s*remove\s+(?:after|when|in)',
         "Backward compatibility TODO found"),
        (r'//\s*backward\s*compat',
         "Backward compatibility comment found"),
        (r'//\s*legacy',
         "Legacy code comment found"),
        (r'@deprecated.*temporary',
         "Temporary deprecated code found"),

        # Unresolved TODOs
        (r'//\s*TODO:',
         "Unresolved TODO comment"),
        (r'//\s*FIXME:',
         "Unresolved FIXME comment"),
        (r'//\s*HACK:',
         "HACK comment found"),
        (r'//\s*XXX:',
         "XXX comment found"),

        # Dead code indicators
        (r'if\s*\(\s*false\s*\)',
         "Dead code: if (false)"),
        (r'while\s*\(\s*false\s*\)',
         "Dead code: while (false)"),

        # Debug artifacts
        (r'\bprint\s*\(\s*[\'"]DEBUG',
         "Debug print statement"),
        (r'console\.log\s*\(',
         "Console.log found (use proper logging)"),
    ]

    for pattern, message in checks:
        if re.search(pattern, content, re.IGNORECASE):
            violations.append(message)

    return violations

def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except:
        hook_input = {}

    tool_input = hook_input.get('tool_input', {})

    # Get content being written/edited
    new_content = tool_input.get('new_string', '') or tool_input.get('content', '')

    if not new_content:
        sys.exit(0)

    # Check for violations
    violations = check_content_for_violations(new_content)

    if violations:
        # For now, warn but don't block (change to exit(2) for strict mode)
        response = {
            "feedback": f"Quality warnings: {', '.join(violations[:3])}",
            "block": False  # Set to True for strict enforcement
        }
        print(json.dumps(response))
        sys.exit(1)  # Warning

    sys.exit(0)

if __name__ == "__main__":
    main()
