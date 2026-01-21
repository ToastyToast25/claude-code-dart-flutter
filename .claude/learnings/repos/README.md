# Repository Learnings

This directory stores analysis and learnings from imported/analyzed GitHub repositories.

## Naming Convention

Files should be named after the repository: `{repo-name}.md`

Example: `jellyflix.md`, `flutter-samples.md`

## Repository Analysis Format

```markdown
# Learnings from {repo-name}

**Source**: https://github.com/{owner}/{repo}
**Analyzed**: YYYY-MM-DD
**Purpose**: [why we analyzed this repo]

## Project Overview
- Type: [Flutter App / Dart Backend / etc]
- Platforms: [Android, iOS, Web, etc]
- Architecture: [Clean Architecture / MVVM / etc]

## Technologies Used
| Category | Choice |
|----------|--------|
| State Management | [riverpod/bloc/etc] |
| Navigation | [go_router/auto_route/etc] |
| API Client | [dio/http/etc] |
| Database | [drift/sqflite/etc] |

## What They Did Well
- [specific implementation detail]
- [architectural decision]

## What Could Be Better
- [improvement opportunity]
- [technical debt observed]

## Code Patterns to Adopt
```dart
// Example pattern from their codebase
[code snippet]
```

## Code Patterns to Avoid
```dart
// Anti-pattern observed
[code snippet]

// Better approach
[improved code]
```

## Feature Ideas
- [feature from repo we want]
- [feature we'll do differently]

## Questions/Unknowns
- [technical question]
- [architectural decision needed]
```

## Usage

When Repository Import Agent analyzes a repo, save findings here for future reference.
