---
description: "Creates Dart extension methods for String, DateTime, List, BuildContext, etc."
globs: ["lib/**/extensions/*.dart", "lib/core/extensions/**/*.dart"]
alwaysApply: false
---

# Create Extension Skill

Create Dart extension methods to add functionality to existing types.

## Trigger Keywords
- create extension
- dart extension
- add extension
- extension methods

---

## Extension Template

```dart
/// Extension on [Type] for [description].
extension [Name]Extension on [Type] {
  /// [Method description].
  [ReturnType] [methodName]([params]) {
    // Implementation using 'this'
  }
}
```

---

## Common Extensions

### String Extensions

```dart
/// Extension methods for String manipulation.
extension StringExtension on String {
  /// Capitalizes the first letter of the string.
  String get capitalized {
    if (isEmpty) return this;
    return '${this[0].toUpperCase()}${substring(1)}';
  }

  /// Capitalizes the first letter of each word.
  String get titleCase {
    return split(' ').map((word) => word.capitalized).join(' ');
  }

  /// Returns true if string is a valid email.
  bool get isValidEmail {
    return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(this);
  }

  /// Returns true if string is a valid URL.
  bool get isValidUrl {
    return Uri.tryParse(this)?.hasAbsolutePath ?? false;
  }

  /// Returns true if string contains only digits.
  bool get isNumeric {
    return RegExp(r'^[0-9]+$').hasMatch(this);
  }

  /// Truncates string to [maxLength] with ellipsis.
  String truncate(int maxLength, {String suffix = '...'}) {
    if (length <= maxLength) return this;
    return '${substring(0, maxLength - suffix.length)}$suffix';
  }

  /// Removes all whitespace from string.
  String get removeWhitespace {
    return replaceAll(RegExp(r'\s+'), '');
  }

  /// Converts string to slug format.
  String get toSlug {
    return toLowerCase()
        .replaceAll(RegExp(r'[^a-z0-9\s-]'), '')
        .replaceAll(RegExp(r'\s+'), '-');
  }

  /// Returns null if string is empty, otherwise returns string.
  String? get nullIfEmpty => isEmpty ? null : this;
}
```

### Nullable String Extensions

```dart
/// Extension methods for nullable Strings.
extension NullableStringExtension on String? {
  /// Returns true if string is null or empty.
  bool get isNullOrEmpty => this == null || this!.isEmpty;

  /// Returns true if string is null, empty, or only whitespace.
  bool get isNullOrBlank => this == null || this!.trim().isEmpty;

  /// Returns the string or a default value if null/empty.
  String orDefault(String defaultValue) {
    return isNullOrEmpty ? defaultValue : this!;
  }
}
```

### DateTime Extensions

```dart
/// Extension methods for DateTime.
extension DateTimeExtension on DateTime {
  /// Returns true if date is today.
  bool get isToday {
    final now = DateTime.now();
    return year == now.year && month == now.month && day == now.day;
  }

  /// Returns true if date is yesterday.
  bool get isYesterday {
    final yesterday = DateTime.now().subtract(const Duration(days: 1));
    return year == yesterday.year &&
        month == yesterday.month &&
        day == yesterday.day;
  }

  /// Returns true if date is tomorrow.
  bool get isTomorrow {
    final tomorrow = DateTime.now().add(const Duration(days: 1));
    return year == tomorrow.year &&
        month == tomorrow.month &&
        day == tomorrow.day;
  }

  /// Returns start of day (00:00:00).
  DateTime get startOfDay => DateTime(year, month, day);

  /// Returns end of day (23:59:59.999).
  DateTime get endOfDay => DateTime(year, month, day, 23, 59, 59, 999);

  /// Returns start of month.
  DateTime get startOfMonth => DateTime(year, month);

  /// Returns end of month.
  DateTime get endOfMonth => DateTime(year, month + 1, 0, 23, 59, 59, 999);

  /// Returns formatted string (uses intl if available).
  String format(String pattern) {
    // Simple implementation without intl
    return '$year-${month.toString().padLeft(2, '0')}-${day.toString().padLeft(2, '0')}';
  }

  /// Returns relative time string (e.g., "2 hours ago").
  String get timeAgo {
    final now = DateTime.now();
    final difference = now.difference(this);

    if (difference.inDays > 365) {
      return '${(difference.inDays / 365).floor()} year(s) ago';
    } else if (difference.inDays > 30) {
      return '${(difference.inDays / 30).floor()} month(s) ago';
    } else if (difference.inDays > 0) {
      return '${difference.inDays} day(s) ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours} hour(s) ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes} minute(s) ago';
    } else {
      return 'Just now';
    }
  }

  /// Adds business days (skipping weekends).
  DateTime addBusinessDays(int days) {
    var result = this;
    var remaining = days;
    while (remaining > 0) {
      result = result.add(const Duration(days: 1));
      if (result.weekday != DateTime.saturday &&
          result.weekday != DateTime.sunday) {
        remaining--;
      }
    }
    return result;
  }
}
```

### List Extensions

```dart
/// Extension methods for List.
extension ListExtension<T> on List<T> {
  /// Returns first element or null if empty.
  T? get firstOrNull => isEmpty ? null : first;

  /// Returns last element or null if empty.
  T? get lastOrNull => isEmpty ? null : last;

  /// Returns element at index or null if out of bounds.
  T? elementAtOrNull(int index) {
    if (index < 0 || index >= length) return null;
    return this[index];
  }

  /// Returns a new list with duplicates removed.
  List<T> get unique => toSet().toList();

  /// Returns a new list with duplicates removed based on key.
  List<T> uniqueBy<K>(K Function(T) key) {
    final seen = <K>{};
    return where((element) => seen.add(key(element))).toList();
  }

  /// Splits list into chunks of [size].
  List<List<T>> chunked(int size) {
    return [
      for (var i = 0; i < length; i += size)
        sublist(i, (i + size > length) ? length : i + size),
    ];
  }

  /// Returns random element.
  T get random => this[DateTime.now().millisecondsSinceEpoch % length];

  /// Inserts separator between elements.
  List<T> separated(T separator) {
    if (length <= 1) return toList();
    return [
      for (var i = 0; i < length; i++) ...[
        if (i > 0) separator,
        this[i],
      ],
    ];
  }
}
```

### Map Extensions

```dart
/// Extension methods for Map.
extension MapExtension<K, V> on Map<K, V> {
  /// Returns value for key or null, with null-safe access.
  V? getOrNull(K key) => containsKey(key) ? this[key] : null;

  /// Returns value for key or default value.
  V getOrDefault(K key, V defaultValue) {
    return containsKey(key) ? this[key] as V : defaultValue;
  }

  /// Returns new map with null values removed.
  Map<K, V> get withoutNulls {
    return Map.fromEntries(
      entries.where((e) => e.value != null),
    );
  }

  /// Transforms map values using provided function.
  Map<K, R> mapValues<R>(R Function(V) transform) {
    return map((key, value) => MapEntry(key, transform(value)));
  }
}
```

### Iterable Extensions

```dart
/// Extension methods for Iterable.
extension IterableExtension<T> on Iterable<T> {
  /// Returns first element matching predicate or null.
  T? firstWhereOrNull(bool Function(T) test) {
    for (final element in this) {
      if (test(element)) return element;
    }
    return null;
  }

  /// Returns last element matching predicate or null.
  T? lastWhereOrNull(bool Function(T) test) {
    T? result;
    for (final element in this) {
      if (test(element)) result = element;
    }
    return result;
  }

  /// Groups elements by key.
  Map<K, List<T>> groupBy<K>(K Function(T) keySelector) {
    final map = <K, List<T>>{};
    for (final element in this) {
      final key = keySelector(element);
      (map[key] ??= []).add(element);
    }
    return map;
  }

  /// Returns sum of elements (requires num type).
  T sum() {
    if (T != int && T != double && T != num) {
      throw UnsupportedError('sum() only works with numeric types');
    }
    return fold(
      (T == int ? 0 : 0.0) as T,
      (prev, curr) => ((prev as num) + (curr as num)) as T,
    );
  }
}
```

### BuildContext Extensions

```dart
/// Extension methods for BuildContext.
extension BuildContextExtension on BuildContext {
  /// Returns current theme.
  ThemeData get theme => Theme.of(this);

  /// Returns current text theme.
  TextTheme get textTheme => Theme.of(this).textTheme;

  /// Returns current color scheme.
  ColorScheme get colorScheme => Theme.of(this).colorScheme;

  /// Returns screen size.
  Size get screenSize => MediaQuery.sizeOf(this);

  /// Returns screen width.
  double get screenWidth => MediaQuery.sizeOf(this).width;

  /// Returns screen height.
  double get screenHeight => MediaQuery.sizeOf(this).height;

  /// Returns true if screen is narrow (mobile).
  bool get isMobile => screenWidth < 600;

  /// Returns true if screen is medium (tablet).
  bool get isTablet => screenWidth >= 600 && screenWidth < 1200;

  /// Returns true if screen is wide (desktop).
  bool get isDesktop => screenWidth >= 1200;

  /// Returns padding (safe area).
  EdgeInsets get padding => MediaQuery.paddingOf(this);

  /// Returns view insets (keyboard).
  EdgeInsets get viewInsets => MediaQuery.viewInsetsOf(this);

  /// Shows snackbar.
  void showSnackBar(String message, {bool isError = false}) {
    ScaffoldMessenger.of(this).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? colorScheme.error : null,
      ),
    );
  }

  /// Navigates to route.
  Future<T?> push<T>(Widget page) {
    return Navigator.of(this).push<T>(
      MaterialPageRoute(builder: (_) => page),
    );
  }

  /// Pops current route.
  void pop<T>([T? result]) => Navigator.of(this).pop(result);
}
```

### Num Extensions

```dart
/// Extension methods for num (int and double).
extension NumExtension on num {
  /// Clamps value between min and max.
  num clampBetween(num min, num max) => this < min ? min : (this > max ? max : this);

  /// Returns Duration in milliseconds.
  Duration get milliseconds => Duration(milliseconds: toInt());

  /// Returns Duration in seconds.
  Duration get seconds => Duration(seconds: toInt());

  /// Returns Duration in minutes.
  Duration get minutes => Duration(minutes: toInt());

  /// Returns Duration in hours.
  Duration get hours => Duration(hours: toInt());

  /// Returns Duration in days.
  Duration get days => Duration(days: toInt());

  /// Returns formatted file size string.
  String get fileSize {
    if (this < 1024) return '$this B';
    if (this < 1024 * 1024) return '${(this / 1024).toStringAsFixed(1)} KB';
    if (this < 1024 * 1024 * 1024) {
      return '${(this / (1024 * 1024)).toStringAsFixed(1)} MB';
    }
    return '${(this / (1024 * 1024 * 1024)).toStringAsFixed(1)} GB';
  }
}
```

---

## File Location

```
lib/
└── core/
    └── extensions/
        ├── string_extension.dart
        ├── datetime_extension.dart
        ├── list_extension.dart
        ├── map_extension.dart
        ├── context_extension.dart
        └── num_extension.dart
```

Or single file:
```
lib/
└── core/
    └── extensions.dart
```

---

## Export Barrel

```dart
// lib/core/extensions/extensions.dart
export 'string_extension.dart';
export 'datetime_extension.dart';
export 'list_extension.dart';
export 'map_extension.dart';
export 'context_extension.dart';
export 'num_extension.dart';
```

---

## Usage

```dart
import 'package:my_app/core/extensions/extensions.dart';

void example() {
  // String
  'hello world'.capitalized; // 'Hello world'
  'hello world'.titleCase; // 'Hello World'
  'test@example.com'.isValidEmail; // true

  // DateTime
  DateTime.now().isToday; // true
  DateTime.now().timeAgo; // 'Just now'

  // List
  [1, 2, 3].firstOrNull; // 1
  [1, 2, 2, 3].unique; // [1, 2, 3]
  [1, 2, 3, 4, 5].chunked(2); // [[1, 2], [3, 4], [5]]

  // Num
  5.seconds; // Duration(seconds: 5)
  1024.fileSize; // '1.0 KB'

  // Context
  context.screenWidth;
  context.theme;
  context.showSnackBar('Hello');
}
```

---

## Checklist

- [ ] Extension has descriptive name (`[Type]Extension`)
- [ ] Methods are well-documented
- [ ] Null-safe implementations
- [ ] No side effects (pure functions)
- [ ] Handles edge cases (empty lists, null values)
- [ ] Consistent with Dart conventions
- [ ] Exported via barrel file
