#!/usr/bin/env python3
"""
Hook: Auto-format Dart files after editing
Exit codes:
  0 = Success
  1 = Error (non-blocking, shown to user)
"""

import json
import sys
import subprocess
import os

def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except:
        hook_input = {}

    tool_input = hook_input.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    # Only format .dart files
    if not file_path.endswith('.dart'):
        sys.exit(0)

    # Check if file exists
    if not os.path.exists(file_path):
        sys.exit(0)

    # Try to format the file
    try:
        result = subprocess.run(
            ['dart', 'format', file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            response = {
                "feedback": f"Auto-formatted: {os.path.basename(file_path)}"
            }
            print(json.dumps(response))
            sys.exit(0)
        else:
            # Non-blocking error
            response = {
                "feedback": f"Format warning: {result.stderr[:200]}"
            }
            print(json.dumps(response))
            sys.exit(1)

    except FileNotFoundError:
        # Dart not in PATH - non-blocking
        response = {
            "feedback": "Note: dart format not available in PATH"
        }
        print(json.dumps(response))
        sys.exit(0)

    except subprocess.TimeoutExpired:
        response = {
            "feedback": "Format timeout - file may be too large"
        }
        print(json.dumps(response))
        sys.exit(1)

    except Exception as e:
        response = {
            "feedback": f"Format error: {str(e)[:100]}"
        }
        print(json.dumps(response))
        sys.exit(1)

if __name__ == "__main__":
    main()
