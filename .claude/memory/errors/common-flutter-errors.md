# Common Flutter/Dart Errors

Error patterns encountered and their solutions. Reference this before debugging similar issues.

---

## Null Safety Errors

### ERR-001: Null check operator used on a null value

**Error:**
```
Null check operator used on a null value
```

**Common Causes:**
1. Using `!` on a nullable value that's actually null
2. Accessing widget properties before initState completes
3. Race condition in async operations

**Solutions:**
```dart
// BAD
final user = ref.read(userProvider).value!;

// GOOD - Check first
final user = ref.read(userProvider).value;
if (user == null) return;

// GOOD - Use pattern matching
if (ref.read(userProvider) case AsyncData(:final value)) {
  // use value safely
}

// GOOD - Provide default
final user = ref.read(userProvider).value ?? User.empty();
```

**Prevention:**
- Avoid `!` operator; use null-aware operators
- Use `late` only when you're certain of initialization order
- Prefer `AsyncValue` pattern with Riverpod

---

### ERR-002: LateInitializationError

**Error:**
```
LateInitializationError: Field 'controller' has not been initialized.
```

**Common Causes:**
1. Accessing `late` field before assignment
2. Using `late` in wrong lifecycle method
3. Conditional initialization that didn't execute

**Solutions:**
```dart
// BAD
late TextEditingController controller;

@override
void initState() {
  super.initState();
  if (someCondition) {
    controller = TextEditingController(); // Might not run!
  }
}

// GOOD - Always initialize or use nullable
TextEditingController? _controller;
TextEditingController get controller => _controller ??= TextEditingController();

// GOOD - Initialize unconditionally
late final TextEditingController controller = TextEditingController();
```

---

## Widget Lifecycle Errors

### ERR-003: setState() called after dispose()

**Error:**
```
setState() called after dispose(): _MyWidgetState#xxxxx
```

**Common Causes:**
1. Async operation completing after widget unmounts
2. Timer/Stream callback after dispose
3. Not cancelling subscriptions

**Solutions:**
```dart
// BAD
Future<void> _loadData() async {
  final data = await api.fetchData();
  setState(() => _data = data); // Widget might be disposed!
}

// GOOD - Check mounted
Future<void> _loadData() async {
  final data = await api.fetchData();
  if (mounted) {
    setState(() => _data = data);
  }
}

// GOOD - Cancel in dispose
StreamSubscription? _subscription;

@override
void initState() {
  super.initState();
  _subscription = stream.listen((data) {
    if (mounted) setState(() => _data = data);
  });
}

@override
void dispose() {
  _subscription?.cancel();
  super.dispose();
}
```

---

### ERR-004: Looking up deactivated widget's ancestor

**Error:**
```
Looking up a deactivated widget's ancestor is unsafe.
```

**Common Causes:**
1. Using BuildContext after async gap
2. Navigator operations after widget disposal

**Solutions:**
```dart
// BAD
onPressed: () async {
  await someAsyncOperation();
  Navigator.of(context).pop(); // Context might be invalid!
}

// GOOD - Capture navigator before async
onPressed: () async {
  final navigator = Navigator.of(context);
  await someAsyncOperation();
  if (mounted) {
    navigator.pop();
  }
}

// GOOD - Use GoRouter with ref
onPressed: () async {
  await someAsyncOperation();
  if (mounted) {
    ref.read(routerProvider).pop();
  }
}
```

---

## Build Errors

### ERR-005: RenderBox was not laid out

**Error:**
```
RenderBox was not laid out: RenderFlex#xxxxx
```

**Common Causes:**
1. Unbounded constraints (Column in Column, ListView in Column)
2. Missing Expanded/Flexible wrapper
3. Infinite height/width

**Solutions:**
```dart
// BAD - ListView in Column without bounds
Column(
  children: [
    ListView(...), // Unbounded height!
  ],
)

// GOOD - Constrain the ListView
Column(
  children: [
    Expanded(
      child: ListView(...),
    ),
  ],
)

// GOOD - Use shrinkWrap (for small lists only)
Column(
  children: [
    ListView(
      shrinkWrap: true,
      physics: NeverScrollableScrollPhysics(),
      ...
    ),
  ],
)
```

---

### ERR-006: Vertical viewport was given unbounded height

**Error:**
```
Vertical viewport was given unbounded height.
```

**Common Causes:**
1. ListView/GridView without height constraint
2. Nested scrollable widgets

**Solutions:**
```dart
// BAD
Column(
  children: [
    ListView.builder(...), // No height constraint!
  ],
)

// GOOD - Wrap in Expanded
Column(
  children: [
    Expanded(
      child: ListView.builder(...),
    ),
  ],
)

// GOOD - Give explicit height
SizedBox(
  height: 300,
  child: ListView.builder(...),
)
```

---

## State Management Errors

### ERR-007: ProviderNotFoundException

**Error:**
```
ProviderNotFoundException: Could not find provider XxxProvider
```

**Common Causes:**
1. Missing ProviderScope at root
2. Provider not in widget tree
3. Wrong ref type used

**Solutions:**
```dart
// Ensure ProviderScope at root
void main() {
  runApp(
    ProviderScope(  // Must wrap entire app
      child: MyApp(),
    ),
  );
}

// Check provider is accessible
// Use ConsumerWidget or Consumer for widgets
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.watch(myProvider);
    // ...
  }
}
```

---

### ERR-008: Bad state: Future already completed

**Error:**
```
Bad state: Future already completed
```

**Common Causes:**
1. Completing a Completer twice
2. Race condition in async code

**Solutions:**
```dart
// BAD
final completer = Completer<void>();
try {
  await doSomething();
  completer.complete();
} catch (e) {
  completer.complete(); // Might complete twice!
}

// GOOD - Check first
final completer = Completer<void>();
try {
  await doSomething();
  if (!completer.isCompleted) completer.complete();
} catch (e) {
  if (!completer.isCompleted) completer.completeError(e);
}
```

---

## Navigation Errors

### ERR-009: Navigator operation requested with a context that does not include a Navigator

**Error:**
```
Navigator operation requested with a context that does not include a Navigator.
```

**Common Causes:**
1. Using context before Navigator is available
2. Wrong context (from builder, not from Navigator)

**Solutions:**
```dart
// BAD - Using MaterialApp's context
MaterialApp(
  home: Builder(
    builder: (context) {
      Navigator.of(context).push(...); // No Navigator yet!
    },
  ),
)

// GOOD - Navigate from inside home widget
MaterialApp(
  home: HomeScreen(), // Navigate from within HomeScreen
)

// GOOD - Use GlobalKey
final navigatorKey = GlobalKey<NavigatorState>();

MaterialApp(
  navigatorKey: navigatorKey,
  home: ...,
)

// Then use:
navigatorKey.currentState?.push(...);
```

---

## How to Add New Errors

When you encounter and solve a new error:

1. Add entry with unique ID (ERR-XXX)
2. Include exact error message
3. List common causes
4. Provide BAD and GOOD code examples
5. Add prevention tips

---

*Last updated: 2026-01-21*
