# Effective Dart Quick Reference

A condensed reference of Effective Dart guidelines.

## Style

### Naming

| Type | Convention | Example |
|------|------------|---------|
| Classes, enums, typedefs, type params | `UpperCamelCase` | `HttpRequest`, `Color` |
| Extensions | `UpperCamelCase` | `StringExtension` |
| Packages, directories, files | `lowercase_with_underscores` | `my_package`, `user_model.dart` |
| Import prefixes | `lowercase_with_underscores` | `import 'dart:math' as math;` |
| Variables, parameters, functions | `lowerCamelCase` | `userName`, `fetchData()` |
| Constants | `lowerCamelCase` | `defaultTimeout` |
| Private members | Prefix with `_` | `_privateField` |

### Acronyms

- Treat acronyms like regular words
- **DO**: `HttpClient`, `IOStream`, `Id`
- **DON'T**: `HTTPClient`, `iostream`, `ID`

### Formatting

```dart
// Line length: 80 characters
// Indentation: 2 spaces
// Use dart format

// Trailing commas for better formatting
Widget build(BuildContext context) {
  return Container(
    padding: const EdgeInsets.all(8),
    child: const Text('Hello'),  // trailing comma
  );
}
```

### Imports Order

```dart
// 1. dart: imports
import 'dart:async';
import 'dart:io';

// 2. package: imports
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

// 3. Relative imports
import '../models/user.dart';
import 'utils.dart';
```

## Usage

### Libraries

```dart
// DO use strings in part of directives
part of 'my_library.dart';

// DON'T use library names
// part of my_library; // Avoid
```

### Null Safety

```dart
// DO use ?? for default values
final name = input ?? 'default';

// DO use ?. for null-conditional access
final length = text?.length;

// DON'T use ! without good reason
// print(name!.length); // Avoid if possible

// DO use flow analysis
if (name != null) {
  print(name.length); // Safe, no ! needed
}
```

### Collections

```dart
// DO use collection literals
final points = <Point>[];
final addresses = <String, Address>{};
final counts = <int>{};

// DON'T use constructors
// final points = List<Point>(); // Avoid
// final addresses = Map<String, Address>(); // Avoid

// DO use spread
final merged = [...list1, ...list2];

// DO use if/for in collections
final widgets = [
  if (showHeader) const Header(),
  for (var item in items) ItemWidget(item),
];
```

### Functions

```dart
// DO use => for simple functions
String get name => _name;
bool get isEmpty => length == 0;

// DON'T use => for complex logic
// Use block body instead

// DO use named parameters for clarity
void resize({required int width, required int height}) {}

// DO provide default values
void greet({String name = 'World'}) {}
```

### Variables

```dart
// DO use final for local variables
final name = 'John';

// DO use const for compile-time constants
const maxRetries = 3;

// DON'T use var for typed API
// var names = <String>[]; // Prefer type annotation

// DO use type inference for locals
final items = <String>[];  // Type is clear from literal
```

## Design

### Classes

```dart
// DO use class modifiers appropriately
final class ImmutablePoint {  // Cannot be extended
  const ImmutablePoint(this.x, this.y);
  final double x, y;
}

sealed class Result<T> {  // Exhaustive pattern matching
  const Result();
}

// DO use const constructors
class Point {
  const Point(this.x, this.y);
  final double x, y;
}
```

### Members

```dart
// DO make fields final when possible
class User {
  User(this.name);
  final String name;  // Immutable
}

// DON'T use getters that do work
// Use methods instead
class Database {
  // Bad: get that does I/O
  // List<User> get users => _fetchUsers();

  // Good: method that does I/O
  Future<List<User>> fetchUsers() async => ...;
}

// DO use setters for side effects
class User {
  String _name = '';

  set name(String value) {
    _name = value;
    _notifyListeners();
  }
}
```

### Types

```dart
// DO annotate public APIs
String greet(String name) => 'Hello, $name!';

// DO use dynamic for truly dynamic types
void logAny(dynamic value) {
  print(value);
}

// DON'T use dynamic to silence analyzer
// Use Object? for unknown types
void process(Object? value) {
  if (value is String) {
    print(value.toUpperCase());
  }
}

// DO use Future<void> not Future
Future<void> save() async {
  await _storage.save();
}
```

### Parameters

```dart
// DO use required for required named params
void createUser({
  required String email,
  required String name,
  String? phone,  // Optional
}) {}

// DO put positional params first
void move(int x, int y, {bool animated = false}) {}

// DON'T use positional booleans
// void save(bool overwrite) {}  // Avoid

// DO use named boolean params
void save({bool overwrite = false}) {}
```

### Equality

```dart
// DO implement == and hashCode together
class Point {
  const Point(this.x, this.y);
  final int x, y;

  @override
  bool operator ==(Object other) {
    return other is Point && other.x == x && other.y == y;
  }

  @override
  int get hashCode => Object.hash(x, y);
}
```

## Documentation

### Format

```dart
/// Returns the user with the given [id].
///
/// Throws [NotFoundException] if no user exists with that ID.
///
/// Example:
/// ```dart
/// final user = await repository.getUser('123');
/// print(user.name);
/// ```
Future<User> getUser(String id) async { ... }
```

### Rules

- Start with a single-sentence summary
- Use third person for methods: "Returns...", "Fetches..."
- Use noun phrases for properties: "The current user"
- Prefix booleans with "Whether": "Whether the connection is active"
- Document parameters with `[paramName]` syntax
- Include examples for complex APIs
- Don't repeat what the code says

### What to Document

```dart
/// YES: Document public APIs
class UserRepository {
  /// Fetches the user with the given [id].
  Future<User> getUser(String id);
}

// NO: Don't document obvious getters
class User {
  final String name;  // No doc needed
  final String email;  // No doc needed
}

// NO: Don't document private members (usually)
String _cachedValue;  // No doc needed
```

## Error Handling

```dart
// DO throw specific exceptions
throw ArgumentError.value(id, 'id', 'must not be empty');
throw StateError('Cannot modify a closed connection');

// DO use on for specific types
try {
  await fetchUser();
} on NotFoundException {
  return null;
} on NetworkException catch (e) {
  log.error('Network failed', e);
  rethrow;
}

// DON'T catch Error types
// Errors indicate bugs, let them crash

// DO document exceptions
/// Throws [ArgumentError] if [id] is empty.
User getUser(String id) { ... }
```
