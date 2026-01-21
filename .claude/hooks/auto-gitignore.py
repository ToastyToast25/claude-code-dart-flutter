#!/usr/bin/env python3
"""
Hook: Auto-update .gitignore when pubspec.yaml changes
Triggers on pubspec.yaml edits to add relevant ignores for new packages

Exit codes:
  0 = Success
  1 = Warning (non-blocking)
"""

import json
import sys
import os
import re
from pathlib import Path

# Package to gitignore mappings
PACKAGE_IGNORES = {
    'firebase_core': [
        '# Firebase',
        'firebase_options.dart',
        'google-services.json',
        'GoogleService-Info.plist',
    ],
    'firebase_crashlytics': [
        '# Crashlytics',
        '**/firebase_crashlytics/',
    ],
    'hive': [
        '# Hive database',
        '*.hive',
        '*.lock',
        '.hive/',
    ],
    'sqflite': [
        '# SQLite',
        '*.db',
        '*.sqlite',
    ],
    'drift': [
        '# Drift database',
        '*.sqlite',
        '*.g.dart',
    ],
    'freezed': [
        '# Freezed generated',
        '*.freezed.dart',
    ],
    'json_serializable': [
        '# JSON serializable',
        '*.g.dart',
    ],
    'build_runner': [
        '# Build runner',
        '.dart_tool/build/',
    ],
    'flutter_native_splash': [
        '# Native splash generated',
        'android/app/src/main/res/drawable/background.png',
    ],
    'flutter_launcher_icons': [
        '# Launcher icons generated',
        # Usually committed, but backup originals ignored
    ],
    'envied': [
        '# Envied generated',
        '*.g.dart',
        '.env',
        '.env.*',
    ],
    'dotenv': [
        '# Environment files',
        '.env',
        '.env.*',
        '!.env.example',
    ],
    'sentry_flutter': [
        '# Sentry',
        'sentry.properties',
    ],
}

# Always ensure these are in gitignore
BASE_IGNORES = [
    '# Dependencies',
    '.packages',
    '.pub/',
    'pubspec.lock',
    '',
    '# Generated',
    '*.g.dart',
    '*.freezed.dart',
    '*.mocks.dart',
    '',
    '# IDE',
    '.idea/',
    '*.iml',
    '.vscode/',
    '',
    '# Build',
    'build/',
    '.dart_tool/',
    '',
    '# Environment',
    '.env',
    '.env.*',
    '!.env.example',
    '',
    '# OS',
    '.DS_Store',
    'Thumbs.db',
]


def get_project_root():
    """Find project root."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / 'pubspec.yaml').exists():
            return current
        if (current.parent / 'pubspec.yaml').exists():
            return current.parent
        current = current.parent
    return Path.cwd()


def extract_packages(pubspec_content: str) -> set:
    """Extract package names from pubspec.yaml content."""
    packages = set()

    # Simple regex to find package names in dependencies
    in_dependencies = False
    for line in pubspec_content.split('\n'):
        if re.match(r'^(dependencies|dev_dependencies):', line):
            in_dependencies = True
            continue
        if in_dependencies:
            if re.match(r'^\S', line) and not line.startswith(' '):
                in_dependencies = False
                continue
            match = re.match(r'^\s+(\w+):', line)
            if match:
                packages.add(match.group(1))

    return packages


def read_gitignore(gitignore_path: Path) -> list:
    """Read current gitignore entries."""
    if not gitignore_path.exists():
        return []
    return gitignore_path.read_text(encoding='utf-8').split('\n')


def update_gitignore(gitignore_path: Path, new_entries: list) -> bool:
    """Add new entries to gitignore if not already present."""
    current = read_gitignore(gitignore_path)
    current_set = set(line.strip() for line in current)

    added = []
    for entry in new_entries:
        if entry.strip() and entry.strip() not in current_set:
            if not entry.startswith('#'):
                added.append(entry)
            current.append(entry)
            current_set.add(entry.strip())

    if added:
        # Write back
        gitignore_path.write_text('\n'.join(current), encoding='utf-8')
        return True
    return False


def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except:
        hook_input = {}

    tool_input = hook_input.get('tool_input', {})
    file_path = tool_input.get('file_path', '')
    new_content = tool_input.get('new_string', '') or tool_input.get('content', '')

    # Only process pubspec.yaml
    if not file_path.endswith('pubspec.yaml'):
        sys.exit(0)

    if not new_content:
        sys.exit(0)

    project_root = get_project_root()
    gitignore_path = project_root / '.gitignore'

    # Extract packages from the new content
    packages = extract_packages(new_content)

    # Collect new ignores needed
    new_ignores = []

    # Ensure base ignores exist
    current_ignores = set(line.strip() for line in read_gitignore(gitignore_path))
    for entry in BASE_IGNORES:
        if entry.strip() and entry.strip() not in current_ignores:
            new_ignores.append(entry)

    # Add package-specific ignores
    for package in packages:
        if package in PACKAGE_IGNORES:
            for entry in PACKAGE_IGNORES[package]:
                if entry.strip() and entry.strip() not in current_ignores:
                    new_ignores.append(entry)

    if new_ignores:
        try:
            update_gitignore(gitignore_path, new_ignores)
            response = {
                "feedback": f"Auto-updated .gitignore with {len([e for e in new_ignores if not e.startswith('#')])} new entries"
            }
            print(json.dumps(response))
        except Exception as e:
            response = {
                "feedback": f"Could not update .gitignore: {str(e)[:50]}"
            }
            print(json.dumps(response))
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
