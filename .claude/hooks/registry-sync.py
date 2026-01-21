#!/usr/bin/env python3
"""
Hook: Remind to update registry when new Claude config files are created
Triggers when files are written to .claude/agents/, .claude/skills/, etc.

Exit codes:
  0 = Success
  1 = Reminder (non-blocking)
"""

import json
import sys
import os
from pathlib import Path

# Directories that should be tracked in registry
TRACKED_DIRS = {
    'agents': 'agent',
    'skills': 'skill',
    'commands': 'command',
    'templates': 'template',
    'hooks': 'hook',
}


def get_project_root():
    """Find project root."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / '.claude').exists():
            return current
        if (current.parent / '.claude').exists():
            return current.parent
        current = current.parent
    return Path.cwd()


def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except:
        hook_input = {}

    tool_input = hook_input.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not file_path:
        sys.exit(0)

    # Normalize path
    file_path = file_path.replace('\\', '/')

    # Check if this is a new file in a tracked directory
    for dir_name, item_type in TRACKED_DIRS.items():
        pattern = f'.claude/{dir_name}/'
        if pattern in file_path:
            # Get filename
            filename = os.path.basename(file_path)

            # Skip README files
            if filename.lower() == 'readme.md':
                sys.exit(0)

            # Check file extension
            if dir_name == 'hooks' and not filename.endswith('.py'):
                sys.exit(0)
            if dir_name == 'templates' and not filename.endswith('.template'):
                sys.exit(0)
            if dir_name in ['agents', 'skills', 'commands'] and not filename.endswith('.md'):
                sys.exit(0)

            response = {
                "feedback": f"New {item_type} created: {filename}. Remember to update registry.md and run /project:validate"
            }
            print(json.dumps(response))
            sys.exit(1)  # Warning, non-blocking

    sys.exit(0)


if __name__ == "__main__":
    main()
