#!/usr/bin/env python3
"""
Hook: Validate pubspec.yaml changes
Checks version format, detects potential dependency conflicts

Exit codes:
  0 = Valid
  1 = Warning (non-blocking)
  2 = Error (blocking)
"""

import json
import sys
import re

# Known conflicting package pairs
CONFLICTING_PACKAGES = [
    (['provider', 'riverpod'], 'Both provider and riverpod detected - choose one state management'),
    (['get', 'riverpod'], 'Both GetX and Riverpod detected - may conflict'),
    (['get', 'provider'], 'Both GetX and Provider detected - may conflict'),
    (['bloc', 'mobx'], 'Both BLoC and MobX detected - choose one state management'),
    (['hive', 'shared_preferences'], 'Consider using only Hive if storing complex data'),
    (['dio', 'http'], 'Both dio and http packages - consider standardizing on one'),
    (['freezed', 'built_value'], 'Both freezed and built_value - choose one code generation'),
]

# Deprecated packages with recommended replacements
DEPRECATED_PACKAGES = {
    'flutter_webview_plugin': 'Use webview_flutter instead',
    'url_launcher_web': 'Included in url_launcher 6.0+',
    'shared_preferences_web': 'Included in shared_preferences 2.0+',
    'path_provider_linux': 'Included in path_provider 2.0+',
    'sqflite_ffi': 'Use sqflite_common_ffi instead',
    'pedantic': 'Use flutter_lints or very_good_analysis',
    'effective_dart': 'Use flutter_lints or lints package',
}

# Version format regex
VERSION_REGEX = r'^version:\s*(\d+\.\d+\.\d+)(\+\d+)?$'
SEMVER_REGEX = r'^\d+\.\d+\.\d+$'


def extract_packages(content: str) -> set:
    """Extract package names from pubspec content."""
    packages = set()
    in_dependencies = False

    for line in content.split('\n'):
        if re.match(r'^(dependencies|dev_dependencies):', line):
            in_dependencies = True
            continue
        if in_dependencies:
            if re.match(r'^\S', line) and not line.startswith(' ') and not line.startswith('\t'):
                in_dependencies = False
                continue
            match = re.match(r'^\s+(\w+):', line)
            if match:
                packages.add(match.group(1))

    return packages


def check_version_format(content: str) -> list:
    """Check if version follows semver format."""
    issues = []

    for line in content.split('\n'):
        if line.startswith('version:'):
            if not re.match(VERSION_REGEX, line.strip()):
                issues.append('Version should follow format: X.Y.Z or X.Y.Z+build')
            break

    return issues


def check_conflicts(packages: set) -> list:
    """Check for known package conflicts."""
    warnings = []

    for conflict_set, message in CONFLICTING_PACKAGES:
        found = [p for p in conflict_set if p in packages]
        if len(found) > 1:
            warnings.append(message)

    return warnings


def check_deprecated(packages: set) -> list:
    """Check for deprecated packages."""
    warnings = []

    for package, replacement in DEPRECATED_PACKAGES.items():
        if package in packages:
            warnings.append(f'{package} is deprecated: {replacement}')

    return warnings


def check_sdk_constraints(content: str) -> list:
    """Check SDK constraints."""
    issues = []

    # Check for very old SDK constraints
    sdk_match = re.search(r'sdk:\s*["\']>=?(\d+\.\d+)', content)
    if sdk_match:
        min_version = sdk_match.group(1)
        major, minor = map(int, min_version.split('.'))
        if major < 3:
            issues.append(f'SDK constraint {min_version} is outdated - consider updating to 3.0+')

    # Check for flutter constraint
    flutter_match = re.search(r'flutter:\s*["\']>=?(\d+\.\d+)', content)
    if flutter_match:
        min_version = flutter_match.group(1)
        major, minor = map(int, min_version.split('.'))
        if major < 3:
            issues.append(f'Flutter constraint {min_version} is outdated - consider updating to 3.0+')

    return issues


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

    errors = []
    warnings = []

    # Check version format
    errors.extend(check_version_format(new_content))

    # Extract packages
    packages = extract_packages(new_content)

    # Check for conflicts
    warnings.extend(check_conflicts(packages))

    # Check for deprecated packages
    warnings.extend(check_deprecated(packages))

    # Check SDK constraints
    warnings.extend(check_sdk_constraints(new_content))

    if errors:
        response = {
            "feedback": f"pubspec.yaml errors: {', '.join(errors[:2])}",
            "block": True
        }
        print(json.dumps(response))
        sys.exit(2)

    if warnings:
        response = {
            "feedback": f"pubspec.yaml warnings: {', '.join(warnings[:2])}"
        }
        print(json.dumps(response))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
