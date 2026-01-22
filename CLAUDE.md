# CLAUDE.md - Dart Development Guide

## Critical Rules (ENFORCED)

> **These rules are enforced by hooks. Violations will be blocked.**

1. **NEVER** edit `.env`, `.env.*`, `secrets.*`, or `credentials.*` files
2. **NEVER** commit code with unresolved `TODO`, `FIXME`, `HACK`, or `XXX` comments
3. **NEVER** leave backward compatibility hacks or legacy code
4. **NEVER** leave dead code, commented-out code, or unreachable code
5. **NEVER** use deprecated APIs - use current alternatives
6. **ALWAYS** run `flutter analyze` before marking code complete - zero warnings required
7. **ALWAYS** ensure code compiles before suggesting it's done

See `.claude/rules/code-quality.md` for full details.

---

## Project Overview

This is a Dart/Flutter project with a comprehensive agent/skill system. Claude should follow Dart best practices, Effective Dart guidelines, and Flutter conventions when working with this codebase.

## Quick Reference

### Commands

```bash
# Run the app
flutter run

# Run tests
flutter test
dart test

# Analyze code
dart analyze
flutter analyze

# Format code
dart format .
flutter format .

# Build
flutter build apk
flutter build ios
flutter build web

# Code generation (freezed, json_serializable, etc.)
dart run build_runner build --delete-conflicting-outputs
dart run build_runner watch --delete-conflicting-outputs

# Get dependencies
flutter pub get
dart pub get

# Upgrade dependencies
flutter pub upgrade
dart pub upgrade
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes, Enums, Typedefs | `UpperCamelCase` | `UserProfile`, `AuthState` |
| Files, Packages, Directories | `lowercase_with_underscores` | `user_profile.dart` |
| Variables, Methods, Parameters | `lowerCamelCase` | `userName`, `fetchData()` |
| Constants | `lowerCamelCase` | `defaultTimeout` (not SCREAMING_CAPS) |
| Private members | Prefix with `_` | `_privateMethod()` |

### Import Order

1. `dart:` imports (core libraries)
2. `package:` imports (external packages)
3. Relative imports (project files)
4. Alphabetical within each group

```dart
import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:riverpod/riverpod.dart';

import '../models/user.dart';
import 'utils.dart';
```

## Code Style Guidelines

### Formatting

- **Line length**: 80 characters maximum
- **Indentation**: 2 spaces
- **Always use curly braces** for control flow (except single-line `if` without `else`)
- **Use `dart format`** - it represents official Dart standards

### Best Practices

```dart
// DO: Use final for single-assignment variables
final name = 'John';

// DO: Use const for compile-time constants
const maxRetries = 3;

// DO: Prefer explicit types for public APIs
String getUserName(int userId) => '';

// DON'T: Use var for public API return types
// var getUserName(int userId) => ''; // Bad

// DO: Use trailing commas for better formatting
Widget build(BuildContext context) {
  return Column(
    children: [
      Text('Hello'),
      Text('World'),
    ],
  );
}
```

### Null Safety

```dart
// Non-nullable by default
String name = 'John';

// Nullable when needed
String? nickname;

// Use flow analysis instead of bang operator
if (nickname != null) {
  print(nickname.length); // Safe - no ! needed
}

// Null-coalescing
final displayName = nickname ?? name;

// Late initialization (use sparingly)
late final String computedValue;
```

## Architecture

This project follows **Feature-First Architecture** with clean separation:

```
lib/
├── features/
│   └── [feature_name]/
│       ├── data/           # Data sources, repositories impl, models
│       ├── domain/         # Entities, repository interfaces, use cases
│       └── presentation/   # Pages, widgets, controllers/viewmodels
├── shared/
│   ├── services/           # App-wide services
│   ├── utils/              # Utility functions
│   ├── widgets/            # Reusable widgets
│   └── theme/              # App theming
└── main.dart
```

## State Management

**Primary**: Riverpod (recommended for most cases)

```dart
// Simple state
final counterProvider = StateProvider((ref) => 0);

// Async data
final userProvider = FutureProvider((ref) => fetchUser());

// Complex state with StateNotifier
class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);
  void increment() => state++;
}
final counterProvider = StateNotifierProvider((ref) => CounterNotifier());
```

## Error Handling

Use the **Result pattern** for explicit error handling:

```dart
sealed class Result<T> {
  const Result();
}

final class Ok<T> extends Result<T> {
  const Ok(this.value);
  final T value;
}

final class Error<T> extends Result<T> {
  const Error(this.error);
  final Exception error;
}

// Usage with pattern matching
switch (result) {
  case Ok(:final value): handleSuccess(value);
  case Error(:final error): handleError(error);
}
```

## Testing

- **Unit tests**: `test/` directory, `*_test.dart` naming
- **Widget tests**: Use `testWidgets()` and `WidgetTester`
- **Integration tests**: `integration_test/` directory

```dart
// Unit test
test('should return user', () {
  // Arrange, Act, Assert
});

// Widget test
testWidgets('should display title', (tester) async {
  await tester.pumpWidget(const MyWidget());
  expect(find.text('Title'), findsOneWidget);
});
```

## Claude Configuration

**Registry**: `.claude/registry.md` - Contains all agent/skill definitions and auto-invoke rules

On each request, consult `.claude/registry.md` to determine which agent(s) to load based on trigger keywords.

### Directory Structure

```
.claude/
├── registry.md          # Agent/skill index (START HERE)
├── context.md           # Project context and session notes
├── settings.json        # Hooks and permissions
├── agents/              # 34 specialized agents
├── skills/              # 27 reusable skills
├── commands/            # Slash commands
├── hooks/               # Enforcement scripts
├── rules/               # Code quality rules
├── memory/              # Persistent learnings
└── learnings/           # Knowledge base
```

### Key Agents

| Agent | File | Use For |
|-------|------|---------|
| Project Setup | `agents/project-setup.md` | New projects |
| Repository Import | `agents/repo-import.md` | Analyze GitHub repos |
| Platform Installer | `agents/platform-installer.md` | Deploy anywhere |
| Agent Testing | `agents/agent-testing.md` | Verify code |
| Learning System | `agents/learning-system.md` | Record patterns |

### Slash Commands

- `/project-new` - Start new project workflow
- `/project-deploy` - Deploy to server
- `/project-test` - Run full test suite
- `/project-review` - Code review workflow
- `/project-fix-issue` - Fix a GitHub issue
- `/project-release` - Create a new release
- `/project-validate` - Validate configuration

## Key Principles

1. **KISS** - Keep implementations simple and focused
2. **DRY** - Don't repeat yourself, but don't over-abstract prematurely
3. **Explicit over implicit** - Be clear about types and intentions
4. **Test-driven** - Write tests alongside features
5. **Immutability** - Prefer immutable data structures
6. **Dependency Injection** - Avoid global mutable state
