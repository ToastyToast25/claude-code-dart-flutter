---
description: "Scaffolds Flutter pages/screens with routing and state management"
globs: ["lib/**/pages/*.dart", "lib/**/screens/*.dart", "lib/**/presentation/**/*_page.dart"]
alwaysApply: false
---

# Create Page Skill

Scaffold a new Flutter page/screen with proper structure and patterns.

## Trigger Keywords
- create page
- new page
- new screen
- add page
- scaffold page

## Page Template

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// [PageName] - Brief description of what this page does.
class [PageName]Page extends ConsumerStatefulWidget {
  const [PageName]Page({super.key});

  static const routeName = '/[route-name]';

  @override
  ConsumerState<[PageName]Page> createState() => _[PageName]PageState();
}

class _[PageName]PageState extends ConsumerState<[PageName]Page> {
  @override
  void initState() {
    super.initState();
    // Initialize page state
  }

  @override
  void dispose() {
    // Clean up controllers, subscriptions
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('[Page Title]'),
      ),
      body: SafeArea(
        child: _buildBody(),
      ),
    );
  }

  Widget _buildBody() {
    return const Center(
      child: Text('[PageName] Page'),
    );
  }
}
```

## Stateless Page Template

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// [PageName] - Brief description.
class [PageName]Page extends ConsumerWidget {
  const [PageName]Page({super.key});

  static const routeName = '/[route-name]';

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('[Page Title]'),
      ),
      body: const SafeArea(
        child: Center(
          child: Text('[PageName] Page'),
        ),
      ),
    );
  }
}
```

## Page with Parameters

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class [PageName]Page extends ConsumerWidget {
  const [PageName]Page({
    super.key,
    required this.id,
  });

  final String id;

  static const routeName = '/[route-name]/:id';

  /// Navigate to this page
  static void go(BuildContext context, String id) {
    context.push('$routeName'.replaceFirst(':id', id));
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final asyncData = ref.watch([dataProvider](id));

    return Scaffold(
      appBar: AppBar(
        title: const Text('[Page Title]'),
      ),
      body: asyncData.when(
        data: (data) => _buildContent(data),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => _buildError(error),
      ),
    );
  }

  Widget _buildContent(Data data) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // Content here
      ],
    );
  }

  Widget _buildError(Object error) {
    return Center(
      child: Text('Error: $error'),
    );
  }
}
```

## File Location

```
lib/
└── features/
    └── [feature_name]/
        └── presentation/
            └── pages/
                └── [page_name]_page.dart
```

## go_router Integration

```dart
// In router configuration
GoRoute(
  path: [PageName]Page.routeName,
  name: '[page-name]',
  builder: (context, state) => const [PageName]Page(),
),

// With parameters
GoRoute(
  path: [PageName]Page.routeName,
  name: '[page-name]',
  builder: (context, state) {
    final id = state.pathParameters['id']!;
    return [PageName]Page(id: id);
  },
),
```

## Checklist

- [ ] Page extends ConsumerWidget or ConsumerStatefulWidget
- [ ] Has static routeName constant
- [ ] Located in correct feature folder
- [ ] Added to router configuration
- [ ] Uses SafeArea for content
- [ ] Handles loading and error states
- [ ] Disposes resources in StatefulWidget
