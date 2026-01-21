---
description: "Analyzes Dart code for issues and applies fixes following best practices"
globs: ["**/*.dart", "analysis_options.yaml"]
alwaysApply: false
---

# Skill: Analyze and Fix Dart Code

Analyze Dart code for issues and apply fixes following best practices.

## Usage

When asked to analyze or fix code, follow these guidelines:

## Running Analysis

```bash
# Run Dart analyzer
dart analyze

# Run Flutter analyzer
flutter analyze

# Fix auto-fixable issues
dart fix --apply
flutter fix --apply

# Preview fixes without applying
dart fix --dry-run
```

## Common Issues and Fixes

### 1. Null Safety Issues

**Issue: Unnecessary null check**
```dart
// Bad
String? name;
if (name != null) {
  print(name!); // Unnecessary !
}

// Good
String? name;
if (name != null) {
  print(name); // Flow analysis handles this
}
```

**Issue: Missing null check**
```dart
// Bad
String? name;
print(name.length); // Error: null check needed

// Good
String? name;
print(name?.length ?? 0);
// or
if (name != null) {
  print(name.length);
}
```

**Issue: Late initialization risks**
```dart
// Bad - runtime error if accessed before init
late String name;

void printName() {
  print(name); // StateError if not initialized
}

// Good - use nullable or provide default
String? name;
String name = '';

void printName() {
  print(name ?? 'Unknown');
}
```

### 2. Async/Await Issues

**Issue: Unawaited futures**
```dart
// Bad - fire and forget
void save() {
  saveToDatabase(); // Warning: unawaited_futures
}

// Good - await or explicitly ignore
Future<void> save() async {
  await saveToDatabase();
}

// Or if intentionally fire-and-forget
void save() {
  unawaited(saveToDatabase());
}
```

**Issue: Missing async**
```dart
// Bad
Future<String> getName() {
  return fetchName(); // Should use async/await
}

// Good
Future<String> getName() async {
  return await fetchName();
}

// Or for simple delegation
Future<String> getName() => fetchName();
```

**Issue: Unnecessary await in return**
```dart
// Bad
Future<String> getName() async {
  return await fetchName(); // Unnecessary await
}

// Good
Future<String> getName() async {
  return fetchName();
}
```

### 3. Widget Issues (Flutter)

**Issue: Missing const constructor**
```dart
// Bad
class MyWidget extends StatelessWidget {
  MyWidget({Key? key}) : super(key: key); // Missing const

  @override
  Widget build(BuildContext context) => const Text('Hello');
}

// Good
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) => const Text('Hello');
}
```

**Issue: BuildContext used after async gap**
```dart
// Bad
onPressed: () async {
  await someAsyncOperation();
  Navigator.of(context).pop(); // Context may be invalid
}

// Good
onPressed: () async {
  final navigator = Navigator.of(context);
  await someAsyncOperation();
  if (mounted) {
    navigator.pop();
  }
}
```

**Issue: Missing key for list items**
```dart
// Bad
ListView(
  children: items.map((item) => ListTile(title: Text(item.name))).toList(),
)

// Good
ListView(
  children: items.map((item) => ListTile(
    key: ValueKey(item.id),
    title: Text(item.name),
  )).toList(),
)
```

### 4. Type Issues

**Issue: Implicit dynamic**
```dart
// Bad
var items = []; // List<dynamic>
final map = {}; // Map<dynamic, dynamic>

// Good
var items = <String>[];
final map = <String, int>{};
```

**Issue: Missing return type**
```dart
// Bad
fetchUser(String id) async {
  return await api.getUser(id);
}

// Good
Future<User> fetchUser(String id) async {
  return await api.getUser(id);
}
```

### 5. Import Issues

**Issue: Unused imports**
```dart
// Bad
import 'dart:io'; // Unused
import 'package:flutter/material.dart';

// Good
import 'package:flutter/material.dart';
```

**Issue: Wrong import order**
```dart
// Bad
import '../utils.dart';
import 'package:flutter/material.dart';
import 'dart:async';

// Good
import 'dart:async';

import 'package:flutter/material.dart';

import '../utils.dart';
```

**Issue: Relative imports in lib/**
```dart
// Bad (in lib/)
import '../../../models/user.dart';

// Good
import 'package:my_app/models/user.dart';
```

### 6. Code Style Issues

**Issue: Unnecessary this**
```dart
// Bad
class User {
  final String name;
  User(this.name);

  void print() {
    print(this.name); // Unnecessary this
  }
}

// Good
class User {
  final String name;
  User(this.name);

  void printName() {
    print(name);
  }
}
```

**Issue: Prefer interpolation**
```dart
// Bad
final message = 'Hello ' + name + '!';

// Good
final message = 'Hello $name!';
```

**Issue: Unnecessary braces in interpolation**
```dart
// Bad
final message = 'Hello ${name}!';

// Good
final message = 'Hello $name!';

// Needed for expressions
final message = 'Hello ${user.name}!';
```

### 7. Performance Issues

**Issue: Inefficient collection operations**
```dart
// Bad
final names = users.map((u) => u.name).toList();
final first = names.first;

// Good
final firstName = users.first.name;
```

**Issue: Unnecessary object creation in build**
```dart
// Bad
Widget build(BuildContext context) {
  return Text(
    'Hello',
    style: TextStyle(fontSize: 16), // Created every build
  );
}

// Good
static const _textStyle = TextStyle(fontSize: 16);

Widget build(BuildContext context) {
  return Text('Hello', style: _textStyle);
}
```

## Analysis Options Setup

```yaml
# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
  errors:
    missing_required_param: error
    missing_return: error
    invalid_annotation_target: ignore

linter:
  rules:
    # Error prevention
    - avoid_print
    - avoid_returning_null_for_future
    - cancel_subscriptions
    - close_sinks
    - unawaited_futures

    # Style
    - always_declare_return_types
    - prefer_const_constructors
    - prefer_const_declarations
    - prefer_final_fields
    - prefer_final_locals
    - prefer_single_quotes

    # Documentation
    - public_member_api_docs
```

## Fix Workflow

1. **Run analyzer**: `dart analyze` or `flutter analyze`
2. **Review issues**: Categorize by severity
3. **Auto-fix**: `dart fix --apply` for safe fixes
4. **Manual fixes**: Address remaining issues
5. **Re-run analyzer**: Verify all issues resolved
6. **Run tests**: Ensure fixes didn't break functionality

## Quick Reference: Common Fixes

| Issue | Fix |
|-------|-----|
| `unnecessary_null_comparison` | Remove redundant null checks |
| `prefer_const_constructors` | Add `const` keyword |
| `avoid_print` | Use logger or debugPrint |
| `unawaited_futures` | Add `await` or `unawaited()` |
| `use_key_in_widget_constructors` | Add `super.key` parameter |
| `prefer_final_locals` | Change `var` to `final` |
| `prefer_single_quotes` | Replace `"` with `'` |
| `unnecessary_this` | Remove `this.` prefix |
| `unused_import` | Remove import statement |
| `missing_return` | Add return statement |
