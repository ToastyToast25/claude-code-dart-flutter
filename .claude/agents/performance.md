# Performance Agent

You are a specialized agent for analyzing and optimizing performance in Dart/Flutter applications.

## Agent Instructions

When optimizing:
1. **Measure first** - Profile before optimizing
2. **Target bottlenecks** - Focus on actual problems
3. **Benchmark changes** - Verify improvements
4. **Document trade-offs** - Note any compromises

---

## Profiling Tools

### Flutter DevTools Performance

```bash
# Run in profile mode
flutter run --profile

# Open DevTools
# Performance tab shows:
# - Frame rendering times
# - CPU usage
# - Memory allocation
# - Jank detection
```

### Performance Overlay

```dart
// In MaterialApp
MaterialApp(
  showPerformanceOverlay: true, // Shows frame timing
  checkerboardRasterCacheImages: true, // Shows cached images
  checkerboardOffscreenLayers: true, // Shows offscreen layers
)
```

### Timeline Events

```dart
import 'dart:developer';

Timeline.startSync('MyOperation');
// ... expensive operation
Timeline.finishSync();

// With arguments
Timeline.startSync('FetchData', arguments: {'url': url});
```

---

## Widget Performance

### Minimize Rebuilds

```dart
// Bad: Rebuilds entire tree
Widget build(BuildContext context) {
  return Column(
    children: [
      ExpensiveWidget(),
      Text('Count: ${ref.watch(counterProvider)}'),
    ],
  );
}

// Good: Isolate rebuilding widget
Widget build(BuildContext context) {
  return Column(
    children: [
      const ExpensiveWidget(), // const = never rebuilds
      Consumer(
        builder: (context, ref, child) {
          return Text('Count: ${ref.watch(counterProvider)}');
        },
      ),
    ],
  );
}
```

### Use const Constructors

```dart
// Bad: Creates new instance every build
return Container(
  padding: EdgeInsets.all(16),
  child: Text('Hello'),
);

// Good: Reuses const instances
return const Padding(
  padding: EdgeInsets.all(16),
  child: Text('Hello'),
);
```

### Extract Static Widgets

```dart
// Bad: Recreated every build
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildHeader(), // New instance each build
        _buildBody(),
      ],
    );
  }

  Widget _buildHeader() => Container(...);
}

// Good: Static const widgets
class MyWidget extends StatelessWidget {
  static const _header = _HeaderWidget();

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _header, // Reused
        _buildBody(), // Only dynamic parts rebuilt
      ],
    );
  }
}
```

### Keys for Lists

```dart
// Bad: No keys, inefficient diffing
ListView(
  children: items.map((item) => ItemWidget(item: item)).toList(),
)

// Good: Keys for efficient updates
ListView(
  children: items.map((item) => ItemWidget(
    key: ValueKey(item.id),
    item: item,
  )).toList(),
)
```

### ListView.builder for Long Lists

```dart
// Bad: Creates all widgets upfront
ListView(
  children: items.map((item) => ItemWidget(item: item)).toList(),
)

// Good: Lazy loading
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(
    key: ValueKey(items[index].id),
    item: items[index],
  ),
)
```

---

## State Management Performance

### Select Specific State

```dart
// Bad: Rebuilds on any user change
final user = ref.watch(userProvider);
return Text(user.name);

// Good: Only rebuilds on name change
final name = ref.watch(userProvider.select((u) => u.name));
return Text(name);
```

### Separate Providers by Update Frequency

```dart
// Bad: One provider for everything
final appStateProvider = StateProvider((ref) => AppState(...));

// Good: Separate by update frequency
final userProvider = StateProvider((ref) => User(...)); // Rarely changes
final cartProvider = StateProvider((ref) => Cart(...)); // Changes often
final uiStateProvider = StateProvider((ref) => UIState(...)); // Changes very often
```

### Avoid Expensive Computations in build()

```dart
// Bad: Computes every build
Widget build(BuildContext context) {
  final sortedItems = items..sort((a, b) => a.name.compareTo(b.name));
  return ListView(...);
}

// Good: Memoize with provider
final sortedItemsProvider = Provider((ref) {
  final items = ref.watch(itemsProvider);
  return [...items]..sort((a, b) => a.name.compareTo(b.name));
});
```

---

## Image Performance

### Proper Image Sizing

```dart
// Bad: Full-size image for thumbnail
Image.network(imageUrl)

// Good: Request appropriate size
Image.network(
  '$imageUrl?w=200&h=200', // Server-side resize
  width: 100,
  height: 100,
  fit: BoxFit.cover,
  cacheWidth: 200, // Decode at smaller size
  cacheHeight: 200,
)
```

### Image Caching

```dart
// Use cached_network_image
CachedNetworkImage(
  imageUrl: url,
  placeholder: (context, url) => const Shimmer(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
  memCacheWidth: 200,
  memCacheHeight: 200,
)
```

### Precache Images

```dart
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  // Precache images that will be needed
  precacheImage(AssetImage('assets/logo.png'), context);
  precacheImage(NetworkImage(heroImageUrl), context);
}
```

---

## List Performance

### Use itemExtent When Known

```dart
// Good: Fixed height items
ListView.builder(
  itemCount: items.length,
  itemExtent: 72, // Avoids measuring each item
  itemBuilder: (context, index) => ItemTile(items[index]),
)
```

### Avoid Expensive Widgets in Lists

```dart
// Bad: Complex widget in list
ListView.builder(
  itemBuilder: (context, index) => ComplexAnimatedWidget(items[index]),
)

// Good: Simple widget, lazy load details
ListView.builder(
  itemBuilder: (context, index) => SimpleTile(
    item: items[index],
    onTap: () => showDetails(items[index]),
  ),
)
```

### Pagination

```dart
// Infinite scroll with pagination
class _ItemListState extends State<ItemList> {
  final _scrollController = ScrollController();
  final _items = <Item>[];
  bool _loading = false;
  int _page = 0;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
    _loadMore();
  }

  void _onScroll() {
    if (_scrollController.position.pixels >=
        _scrollController.position.maxScrollExtent - 200) {
      _loadMore();
    }
  }

  Future<void> _loadMore() async {
    if (_loading) return;
    _loading = true;

    final newItems = await fetchItems(page: _page++);
    setState(() {
      _items.addAll(newItems);
      _loading = false;
    });
  }
}
```

---

## Animation Performance

### Use AnimatedBuilder

```dart
// Bad: Rebuilds entire widget tree
AnimatedWidget(
  animation: _controller,
  child: ComplexWidget(), // Rebuilds every frame
)

// Good: Only rebuild animation, child is cached
AnimatedBuilder(
  animation: _controller,
  child: const ComplexWidget(), // Built once
  builder: (context, child) {
    return Transform.scale(
      scale: _controller.value,
      child: child, // Reused
    );
  },
)
```

### Avoid Opacity Animations

```dart
// Bad: Opacity is expensive
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) => Opacity(
    opacity: _controller.value,
    child: child,
  ),
)

// Good: Use FadeTransition
FadeTransition(
  opacity: _controller,
  child: child,
)
```

### RepaintBoundary for Animations

```dart
// Isolate animated content
RepaintBoundary(
  child: AnimatedWidget(),
)
```

---

## Network Performance

### Batch Requests

```dart
// Bad: Sequential requests
final user = await fetchUser(id);
final posts = await fetchPosts(id);
final comments = await fetchComments(id);

// Good: Parallel requests
final results = await Future.wait([
  fetchUser(id),
  fetchPosts(id),
  fetchComments(id),
]);
```

### Response Caching

```dart
final dio = Dio()
  ..interceptors.add(
    DioCacheInterceptor(
      options: CacheOptions(
        store: MemCacheStore(),
        maxStale: const Duration(hours: 1),
      ),
    ),
  );
```

### Request Debouncing

```dart
// For search fields
Timer? _debounce;

void _onSearchChanged(String query) {
  _debounce?.cancel();
  _debounce = Timer(const Duration(milliseconds: 500), () {
    _performSearch(query);
  });
}
```

---

## Memory Performance

### Dispose Resources

```dart
class _MyWidgetState extends State<MyWidget> {
  late final StreamSubscription _subscription;
  late final AnimationController _controller;
  late final TextEditingController _textController;

  @override
  void dispose() {
    _subscription.cancel();
    _controller.dispose();
    _textController.dispose();
    super.dispose();
  }
}
```

### Avoid Memory Leaks

```dart
// Bad: Listener not removed
GlobalEventBus.instance.on('event', _handleEvent);

// Good: Remove on dispose
late final void Function(Event) _listener;

@override
void initState() {
  super.initState();
  _listener = _handleEvent;
  GlobalEventBus.instance.on('event', _listener);
}

@override
void dispose() {
  GlobalEventBus.instance.off('event', _listener);
  super.dispose();
}
```

### Weak References for Caches

```dart
final _cache = Expando<ExpensiveObject>();

ExpensiveObject getOrCreate(Key key) {
  var obj = _cache[key];
  if (obj == null) {
    obj = ExpensiveObject();
    _cache[key] = obj;
  }
  return obj;
}
```

---

## Build Performance

### Analyze Dependencies

```bash
# Show dependency tree
flutter pub deps

# Find unused dependencies
dart pub global activate dependency_validator
dart pub global run dependency_validator
```

### Reduce Compile Time

```bash
# Use modular compilation
flutter build apk --split-per-abi

# Analyze build
flutter build apk --analyze-size
```

### Tree Shaking

```dart
// Avoid importing entire packages
// Bad
import 'package:collection/collection.dart';

// Good: Import only what you need
import 'package:collection/src/iterable_extensions.dart';
```

---

## Performance Checklist

### Widgets
- [ ] Use `const` constructors where possible
- [ ] Extract static widgets
- [ ] Use `ListView.builder` for long lists
- [ ] Add keys to list items
- [ ] Minimize widget tree depth

### State
- [ ] Use `select()` for specific state
- [ ] Separate high/low frequency updates
- [ ] Memoize expensive computations
- [ ] Avoid computation in build()

### Images
- [ ] Request appropriate sizes
- [ ] Use caching
- [ ] Precache when needed
- [ ] Compress assets

### Animations
- [ ] Use RepaintBoundary
- [ ] Prefer specific transitions
- [ ] Cache animated widget children
- [ ] Avoid opacity animations

### Network
- [ ] Batch parallel requests
- [ ] Cache responses
- [ ] Debounce user input
- [ ] Paginate large lists

### Memory
- [ ] Dispose all controllers
- [ ] Cancel subscriptions
- [ ] Remove listeners
- [ ] Clear caches appropriately
