#!/usr/bin/env python3
"""
Hook: Record session learnings when conversation ends
Exit codes:
  0 = Success (continue allowed)
"""

import json
import sys
import os
from datetime import datetime

def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except:
        hook_input = {}

    # Get the stop reason if available
    stop_reason = hook_input.get('stop_reason', 'unknown')

    # Path to sessions directory
    sessions_dir = os.path.join(os.path.dirname(__file__), '..', 'memory', 'sessions')

    # Ensure directory exists
    os.makedirs(sessions_dir, exist_ok=True)

    # Create session marker file
    today = datetime.now().strftime('%Y-%m-%d')
    marker_file = os.path.join(sessions_dir, f'.session-{today}.marker')

    try:
        # Just create/touch the marker file to indicate a session occurred
        with open(marker_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - Session ended: {stop_reason}\n")

        response = {
            "feedback": "Session recorded",
            "continue": True
        }
        print(json.dumps(response))

    except Exception as e:
        # Don't block on errors
        response = {
            "feedback": f"Could not record session: {str(e)[:50]}",
            "continue": True
        }
        print(json.dumps(response))

    sys.exit(0)

if __name__ == "__main__":
    main()
