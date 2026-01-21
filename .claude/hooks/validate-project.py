#!/usr/bin/env python3
"""
Hook/Script: Validate project configuration consistency
Can be run standalone or as a hook

Exit codes:
  0 = All validations passed
  1 = Warnings found (non-blocking)
  2 = Errors found (blocking if used as PreToolUse)
"""

import json
import sys
import os
import re
from pathlib import Path

def get_project_root():
    """Find project root (where .claude directory is)."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / '.claude').exists():
            return current
        if (current.parent / '.claude').exists():
            return current.parent
        current = current.parent
    return Path.cwd()

def count_files(directory: Path, extension: str, exclude_readme: bool = True) -> list:
    """Count files with given extension in directory."""
    if not directory.exists():
        return []

    files = []
    for f in directory.glob(f'*{extension}'):
        if exclude_readme and f.name.lower() == 'readme.md':
            continue
        files.append(f)
    return files

def extract_registry_counts(registry_path: Path) -> dict:
    """Extract documented counts from registry.md."""
    counts = {}
    if not registry_path.exists():
        return counts

    content = registry_path.read_text(encoding='utf-8')

    # Look for patterns in the Summary Statistics table
    # Format: | Total Agents | 34 | or | Templates | 6 |
    patterns = [
        (r'\|\s*Total\s+Agents\s*\|\s*(\d+)\s*\|', 'agents'),
        (r'\|\s*Total\s+Skills\s*\|\s*(\d+)\s*\|', 'skills'),
        (r'\|\s*Commands\s*\|\s*(\d+)\s*\|', 'commands'),
        (r'\|\s*Templates\s*\|\s*(\d+)\s*\|', 'templates'),
        (r'\|\s*Hooks\s*\|\s*(\d+)\s*\|', 'hooks'),
    ]

    for pattern, key in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            counts[key] = int(match.group(1))

    return counts

def validate_settings(settings_path: Path, project_root: Path) -> list:
    """Validate settings.json references."""
    issues = []

    if not settings_path.exists():
        issues.append("settings.json not found")
        return issues

    try:
        settings = json.loads(settings_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        issues.append(f"settings.json is invalid JSON: {e}")
        return issues

    # Check autoLoad files
    context = settings.get('context', {})
    for auto_file in context.get('autoLoad', []):
        full_path = project_root / auto_file
        if not full_path.exists():
            issues.append(f"autoLoad file missing: {auto_file}")

    # Check onFileMatch skill references
    for pattern, skills in context.get('onFileMatch', {}).items():
        for skill in skills:
            skill_path = project_root / skill
            if not skill_path.exists():
                issues.append(f"onFileMatch skill missing: {skill} (pattern: {pattern})")

    # Check hook files
    hooks = settings.get('hooks', {})
    for hook_type in ['PreToolUse', 'PostToolUse', 'Stop']:
        for hook in hooks.get(hook_type, []):
            command = hook.get('command', [])
            if len(command) >= 2:
                hook_file = command[1]  # Usually the python file path
                hook_path = project_root / hook_file
                if not hook_path.exists():
                    issues.append(f"{hook_type} hook file missing: {hook_file}")

    return issues

def validate_skill_frontmatter(skills_dir: Path) -> list:
    """Validate that skills have proper frontmatter."""
    issues = []

    if not skills_dir.exists():
        return issues

    for skill_file in skills_dir.glob('*.md'):
        if skill_file.name.lower() == 'readme.md':
            continue

        content = skill_file.read_text(encoding='utf-8')

        # Check for YAML frontmatter
        if not content.startswith('---'):
            issues.append(f"Skill missing frontmatter: {skill_file.name}")
            continue

        # Extract frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            issues.append(f"Skill has invalid frontmatter: {skill_file.name}")
            continue

        frontmatter = parts[1]

        # Check required fields
        if 'description:' not in frontmatter:
            issues.append(f"Skill missing description: {skill_file.name}")

        if 'globs:' not in frontmatter and 'alwaysApply:' not in frontmatter:
            issues.append(f"Skill needs globs or alwaysApply: {skill_file.name}")

    return issues

def main():
    """Run all validations."""
    project_root = get_project_root()
    claude_dir = project_root / '.claude'

    report = {
        'counts': {},
        'registry_counts': {},
        'issues': [],
        'warnings': []
    }

    # Count actual files
    agents = count_files(claude_dir / 'agents', '.md')
    skills = count_files(claude_dir / 'skills', '.md')
    commands = count_files(claude_dir / 'commands', '.md')
    templates = count_files(claude_dir / 'templates', '.template')
    hooks = count_files(claude_dir / 'hooks', '.py', exclude_readme=False)

    report['counts'] = {
        'agents': len(agents),
        'skills': len(skills),
        'commands': len(commands),
        'templates': len(templates),
        'hooks': len(hooks)
    }

    # Get registry counts
    report['registry_counts'] = extract_registry_counts(claude_dir / 'registry.md')

    # Compare counts
    for key in ['agents', 'skills', 'commands', 'templates', 'hooks']:
        actual = report['counts'].get(key, 0)
        documented = report['registry_counts'].get(key)

        if documented is not None and actual != documented:
            report['issues'].append(
                f"{key.capitalize()} count mismatch: actual={actual}, registry={documented}"
            )

    # Validate settings
    settings_issues = validate_settings(claude_dir / 'settings.json', project_root)
    report['issues'].extend(settings_issues)

    # Validate skill frontmatter
    frontmatter_issues = validate_skill_frontmatter(claude_dir / 'skills')
    report['warnings'].extend(frontmatter_issues)

    # Output report (use ASCII-safe symbols for Windows compatibility)
    print("=== Project Validation Report ===\n")

    for key in ['agents', 'skills', 'commands', 'templates', 'hooks']:
        actual = report['counts'].get(key, 0)
        documented = report['registry_counts'].get(key, '?')
        status = '[OK]' if actual == documented else '[X]'
        print(f"{status} {key.capitalize()}: {actual} (registry: {documented})")

    print()

    if report['issues']:
        print("Issues Found:")
        for issue in report['issues']:
            print(f"  [X] {issue}")
        print()

    if report['warnings']:
        print("Warnings:")
        for warning in report['warnings']:
            print(f"  [!] {warning}")
        print()

    total_problems = len(report['issues']) + len(report['warnings'])
    print(f"Total: {len(report['issues'])} errors, {len(report['warnings'])} warnings")
    print("\n=== Validation Complete ===")

    # Return appropriate exit code
    if report['issues']:
        sys.exit(2)  # Errors
    elif report['warnings']:
        sys.exit(1)  # Warnings only
    else:
        sys.exit(0)  # All good

if __name__ == "__main__":
    main()
