# Flutter Patterns Quick Reference

Common Flutter patterns and best practices.

## Widget Patterns

### Const Widgets

```dart
// Always use const when possible
class MyScreen extends StatelessWidget {
  const MyScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        Text('Title'),
        SizedBox(height: 16),
        Text('Content'),
      ],
    );
  }
}
```

### Builder Pattern for Complex Widgets

```dart
class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _buildAppBar(context),
      body: _buildBody(context),
    );
  }

  PreferredSizeWidget _buildAppBar(BuildContext context) {
    return AppBar(title: const Text('Profile'));
  }

  Widget _buildBody(BuildContext context) {
    return ListView(
      children: [
        _buildHeader(),
        _buildStats(),
        _buildActions(),
      ],
    );
  }

  Widget _buildHeader() => const ProfileHeader();
  Widget _buildStats() => const ProfileStats();
  Widget _buildActions() => const ProfileActions();
}
```

### Conditional Rendering

```dart
Widget build(BuildContext context) {
  return Column(
    children: [
      // Single condition
      if (showHeader) const Header(),

      // Spread multiple widgets
      if (showDetails) ...[
        const Divider(),
        const DetailsSection(),
        const Divider(),
      ],

      // Map items
      for (final item in items)
        ListTile(title: Text(item.name)),
    ],
  );
}
```

### Extract Widgets vs Methods

```dart
// Prefer extracting to widgets for:
// - Reusable components
// - Widgets that need their own state
// - Better rebuild optimization

// Good: Extract to widget
class UserAvatar extends StatelessWidget {
  const UserAvatar({super.key, required this.user});
  final User user;

  @override
  Widget build(BuildContext context) {
    return CircleAvatar(
      backgroundImage: NetworkImage(user.avatarUrl),
      child: Text(user.initials),
    );
  }
}

// Use methods for:
// - Non-reusable UI sections
// - When you need BuildContext access
// - Simple, local decomposition

Widget _buildTitle(BuildContext context) {
  final theme = Theme.of(context);
  return Text('Title', style: theme.textTheme.headlineLarge);
}
```

## State Management Patterns

### Lifting State Up

```dart
// Parent owns state, passes down to children
class CounterPage extends StatefulWidget {
  const CounterPage({super.key});

  @override
  State<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends State<CounterPage> {
  int _count = 0;

  void _increment() => setState(() => _count++);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        CounterDisplay(count: _count),
        CounterButton(onPressed: _increment),
      ],
    );
  }
}

// Stateless children
class CounterDisplay extends StatelessWidget {
  const CounterDisplay({super.key, required this.count});
  final int count;

  @override
  Widget build(BuildContext context) => Text('$count');
}

class CounterButton extends StatelessWidget {
  const CounterButton({super.key, required this.onPressed});
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      child: const Text('Increment'),
    );
  }
}
```

### Riverpod State Pattern

```dart
// State class (immutable)
@freezed
class AuthState with _$AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  const factory AuthState.authenticated(User user) = _Authenticated;
  const factory AuthState.error(String message) = _Error;
}

// Notifier
class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier(this._repository) : super(const AuthState.initial());

  final AuthRepository _repository;

  Future<void> login(String email, String password) async {
    state = const AuthState.loading();
    final result = await _repository.login(email, password);
    state = result.when(
      ok: (user) => AuthState.authenticated(user),
      error: (e) => AuthState.error(e.message),
    );
  }
}

// Provider
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.watch(authRepositoryProvider));
});

// Widget
class LoginPage extends ConsumerWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(authProvider);

    return state.when(
      initial: () => const LoginForm(),
      loading: () => const LoadingIndicator(),
      authenticated: (user) => HomeRedirect(user: user),
      error: (message) => LoginForm(error: message),
    );
  }
}
```

## Navigation Patterns

### go_router Setup

```dart
final routerProvider = Provider((ref) {
  final authState = ref.watch(authProvider);

  return GoRouter(
    initialLocation: '/',
    refreshListenable: authState,
    redirect: (context, state) {
      final isLoggedIn = authState.isAuthenticated;
      final isAuthRoute = state.matchedLocation.startsWith('/auth');

      if (!isLoggedIn && !isAuthRoute) return '/auth/login';
      if (isLoggedIn && isAuthRoute) return '/';
      return null;
    },
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const HomePage(),
        routes: [
          GoRoute(
            path: 'users/:id',
            builder: (context, state) {
              final id = state.pathParameters['id']!;
              return UserPage(userId: id);
            },
          ),
        ],
      ),
      GoRoute(
        path: '/auth/login',
        builder: (context, state) => const LoginPage(),
      ),
    ],
  );
});
```

### Deep Linking

```dart
GoRoute(
  path: '/products/:productId',
  builder: (context, state) {
    final productId = state.pathParameters['productId']!;
    final tab = state.uri.queryParameters['tab'];
    return ProductPage(productId: productId, initialTab: tab);
  },
),
```

## Form Patterns

### Form with Validation

```dart
class LoginForm extends StatefulWidget {
  const LoginForm({super.key});

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _submit() {
    if (_formKey.currentState!.validate()) {
      // Process form
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            controller: _emailController,
            decoration: const InputDecoration(labelText: 'Email'),
            keyboardType: TextInputType.emailAddress,
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Email is required';
              }
              if (!value.contains('@')) {
                return 'Enter a valid email';
              }
              return null;
            },
          ),
          TextFormField(
            controller: _passwordController,
            decoration: const InputDecoration(labelText: 'Password'),
            obscureText: true,
            validator: (value) {
              if (value == null || value.length < 8) {
                return 'Password must be at least 8 characters';
              }
              return null;
            },
          ),
          ElevatedButton(
            onPressed: _submit,
            child: const Text('Login'),
          ),
        ],
      ),
    );
  }
}
```

## Async Patterns

### FutureBuilder

```dart
Widget build(BuildContext context) {
  return FutureBuilder<User>(
    future: _fetchUser(),
    builder: (context, snapshot) {
      if (snapshot.connectionState == ConnectionState.waiting) {
        return const CircularProgressIndicator();
      }
      if (snapshot.hasError) {
        return Text('Error: ${snapshot.error}');
      }
      if (!snapshot.hasData) {
        return const Text('No data');
      }
      return UserWidget(user: snapshot.data!);
    },
  );
}
```

### StreamBuilder

```dart
Widget build(BuildContext context) {
  return StreamBuilder<List<Message>>(
    stream: _messagesStream,
    builder: (context, snapshot) {
      if (snapshot.hasError) {
        return ErrorWidget(snapshot.error!);
      }
      final messages = snapshot.data ?? [];
      return ListView.builder(
        itemCount: messages.length,
        itemBuilder: (context, index) => MessageTile(messages[index]),
      );
    },
  );
}
```

### Async in Callbacks

```dart
// Safe pattern for async in callbacks
ElevatedButton(
  onPressed: () async {
    // Capture values before async gap
    final navigator = Navigator.of(context);
    final scaffoldMessenger = ScaffoldMessenger.of(context);

    try {
      await performAsyncOperation();
      if (!mounted) return;  // Check if widget still mounted
      navigator.pop();
    } catch (e) {
      if (!mounted) return;
      scaffoldMessenger.showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  },
  child: const Text('Submit'),
)
```

## Performance Patterns

### Const Constructors

```dart
// Extract constants
class AppConstants {
  static const padding = EdgeInsets.all(16);
  static const borderRadius = BorderRadius.all(Radius.circular(8));
}

// Use const widgets
return const Padding(
  padding: AppConstants.padding,
  child: Text('Hello'),
);
```

### Selective Rebuilds

```dart
// Use Consumer/select to minimize rebuilds
Consumer(
  builder: (context, ref, child) {
    // Only rebuilds when name changes
    final name = ref.watch(userProvider.select((u) => u.name));
    return Text(name);
  },
)

// Or with Selector
Selector<UserModel, String>(
  selector: (context, user) => user.name,
  builder: (context, name, child) => Text(name),
)
```

### ListView Optimization

```dart
// Use builder for large lists
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(
    key: ValueKey(items[index].id),
    item: items[index],
  ),
)

// Separate items to avoid unnecessary rebuilds
ListView.separated(
  itemCount: items.length,
  separatorBuilder: (context, index) => const Divider(),
  itemBuilder: (context, index) => ItemWidget(items[index]),
)
```

## Error Handling Patterns

### Error Boundaries

```dart
class ErrorBoundary extends StatefulWidget {
  const ErrorBoundary({super.key, required this.child});
  final Widget child;

  @override
  State<ErrorBoundary> createState() => _ErrorBoundaryState();
}

class _ErrorBoundaryState extends State<ErrorBoundary> {
  Object? _error;

  @override
  Widget build(BuildContext context) {
    if (_error != null) {
      return ErrorDisplay(error: _error!);
    }
    return widget.child;
  }
}
```

### Async Error Handling

```dart
// With Result pattern
final result = await userRepository.getUser(id);
switch (result) {
  case Ok(:final value):
    return UserLoaded(value);
  case Error(:final error):
    return UserError(error.message);
}

// With Riverpod AsyncValue
ref.watch(userProvider).when(
  data: (user) => UserWidget(user),
  loading: () => const LoadingWidget(),
  error: (error, stack) => ErrorWidget(error),
);
```
