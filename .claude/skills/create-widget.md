---
description: "Creates Flutter widgets (Stateless/Stateful) following project patterns"
globs: ["lib/**/*_widget.dart", "lib/**/widgets/*.dart"]
alwaysApply: false
---

# Skill: Create Flutter Widget

Create well-structured Flutter widgets following best practices.

## Usage

When asked to create a widget, follow these guidelines:

## StatelessWidget Template

```dart
import 'package:flutter/material.dart';

/// Brief description of what this widget does.
class MyWidget extends StatelessWidget {
  /// Creates a [MyWidget].
  const MyWidget({
    super.key,
    required this.title,
    this.onTap,
  });

  /// The title displayed in the widget.
  final String title;

  /// Called when the widget is tapped.
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Text(title),
    );
  }
}
```

## StatefulWidget Template

```dart
import 'package:flutter/material.dart';

/// Brief description of what this widget does.
class MyStatefulWidget extends StatefulWidget {
  /// Creates a [MyStatefulWidget].
  const MyStatefulWidget({
    super.key,
    required this.initialValue,
    this.onChanged,
  });

  /// The initial value.
  final int initialValue;

  /// Called when the value changes.
  final ValueChanged<int>? onChanged;

  @override
  State<MyStatefulWidget> createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget> {
  late int _value;

  @override
  void initState() {
    super.initState();
    _value = widget.initialValue;
  }

  @override
  void didUpdateWidget(MyStatefulWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.initialValue != widget.initialValue) {
      _value = widget.initialValue;
    }
  }

  void _increment() {
    setState(() => _value++);
    widget.onChanged?.call(_value);
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _increment,
      child: Text('$_value'),
    );
  }
}
```

## ConsumerWidget Template (Riverpod)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Brief description of what this widget does.
class MyConsumerWidget extends ConsumerWidget {
  /// Creates a [MyConsumerWidget].
  const MyConsumerWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(myProvider);

    return switch (state) {
      AsyncLoading() => const CircularProgressIndicator(),
      AsyncError(:final error) => Text('Error: $error'),
      AsyncData(:final value) => Text('Value: $value'),
    };
  }
}
```

## Widget Checklist

- [ ] Use `const` constructor if possible
- [ ] Use `super.key` parameter
- [ ] Mark required parameters with `required`
- [ ] Use `final` for all fields
- [ ] Add doc comments for class and public members
- [ ] Use trailing commas for better formatting
- [ ] Extract complex build logic to private methods
- [ ] Use `const` for child widgets when possible
- [ ] Add `Key` parameter for widgets in lists

## Naming Conventions

- Widget class: `UpperCamelCase` (e.g., `UserProfileCard`)
- File name: `lowercase_with_underscores` (e.g., `user_profile_card.dart`)
- Private state class: `_WidgetNameState`
- Callbacks: `on` prefix (e.g., `onTap`, `onChanged`)

## Common Patterns

### Conditional Rendering

```dart
@override
Widget build(BuildContext context) {
  return Column(
    children: [
      if (showHeader) const Header(),
      Content(data: data),
      if (showFooter) ...[
        const Divider(),
        const Footer(),
      ],
    ],
  );
}
```

### Builder Pattern for Complex Widgets

```dart
Widget build(BuildContext context) {
  return Column(
    children: [
      _buildHeader(),
      _buildContent(),
      _buildFooter(),
    ],
  );
}

Widget _buildHeader() => const Text('Header');
Widget _buildContent() => const Text('Content');
Widget _buildFooter() => const Text('Footer');
```

### Responsive Design

```dart
@override
Widget build(BuildContext context) {
  final screenWidth = MediaQuery.sizeOf(context).width;

  return screenWidth > 600
      ? _buildWideLayout()
      : _buildNarrowLayout();
}
```
