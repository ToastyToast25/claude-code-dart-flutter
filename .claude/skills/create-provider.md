---
description: "Creates Riverpod providers for state management (StateProvider, FutureProvider, Notifier)"
globs: ["lib/**/providers/*.dart", "lib/**/presentation/**/*_provider.dart"]
alwaysApply: false
---

# Skill: Create Riverpod Provider

Create well-structured Riverpod providers following best practices.

## Usage

When asked to create a provider or state management, follow these guidelines:

## Provider Types

### StateProvider (Simple Mutable State)

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Provides the current counter value.
final counterProvider = StateProvider<int>((ref) => 0);

// Usage in widget
class CounterWidget extends ConsumerWidget {
  const CounterWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);

    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () => ref.read(counterProvider.notifier).state++,
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

### Provider (Computed/Derived Values)

```dart
/// Provides the formatted display string for the counter.
final counterDisplayProvider = Provider<String>((ref) {
  final count = ref.watch(counterProvider);
  return 'Current count: $count';
});

/// Provides whether the counter is even.
final isEvenProvider = Provider<bool>((ref) {
  final count = ref.watch(counterProvider);
  return count.isEven;
});
```

### FutureProvider (Async Data)

```dart
/// Provides the current user fetched from the API.
final userProvider = FutureProvider<User>((ref) async {
  final apiClient = ref.watch(apiClientProvider);
  return apiClient.fetchCurrentUser();
});

/// Provides a user by ID.
final userByIdProvider = FutureProvider.family<User, String>((ref, userId) async {
  final apiClient = ref.watch(apiClientProvider);
  return apiClient.fetchUser(userId);
});

// Usage
class UserWidget extends ConsumerWidget {
  const UserWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userProvider);

    return userAsync.when(
      data: (user) => Text('Hello, ${user.name}'),
      loading: () => const CircularProgressIndicator(),
      error: (error, stack) => Text('Error: $error'),
    );
  }
}
```

### StreamProvider (Real-time Data)

```dart
/// Provides real-time messages.
final messagesProvider = StreamProvider<List<Message>>((ref) {
  final repository = ref.watch(messageRepositoryProvider);
  return repository.watchMessages();
});

/// Provides auth state changes.
final authStateProvider = StreamProvider<User?>((ref) {
  final authService = ref.watch(authServiceProvider);
  return authService.authStateChanges;
});
```

### StateNotifierProvider (Complex State)

```dart
/// The state for the todo list.
@immutable
class TodoState {
  const TodoState({
    this.todos = const [],
    this.filter = TodoFilter.all,
    this.isLoading = false,
    this.error,
  });

  final List<Todo> todos;
  final TodoFilter filter;
  final bool isLoading;
  final String? error;

  TodoState copyWith({
    List<Todo>? todos,
    TodoFilter? filter,
    bool? isLoading,
    String? error,
  }) {
    return TodoState(
      todos: todos ?? this.todos,
      filter: filter ?? this.filter,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

/// Manages the todo list state.
class TodoNotifier extends StateNotifier<TodoState> {
  TodoNotifier(this._repository) : super(const TodoState());

  final TodoRepository _repository;

  Future<void> loadTodos() async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final todos = await _repository.getTodos();
      state = state.copyWith(todos: todos, isLoading: false);
    } catch (e) {
      state = state.copyWith(error: e.toString(), isLoading: false);
    }
  }

  Future<void> addTodo(String title) async {
    final todo = Todo(id: _uuid.v4(), title: title);
    state = state.copyWith(todos: [...state.todos, todo]);

    try {
      await _repository.saveTodo(todo);
    } catch (e) {
      // Rollback on error
      state = state.copyWith(
        todos: state.todos.where((t) => t.id != todo.id).toList(),
        error: e.toString(),
      );
    }
  }

  void toggleTodo(String id) {
    state = state.copyWith(
      todos: state.todos.map((todo) {
        return todo.id == id
            ? todo.copyWith(isCompleted: !todo.isCompleted)
            : todo;
      }).toList(),
    );
  }

  void setFilter(TodoFilter filter) {
    state = state.copyWith(filter: filter);
  }
}

/// Provides the todo list state.
final todoProvider = StateNotifierProvider<TodoNotifier, TodoState>((ref) {
  return TodoNotifier(ref.watch(todoRepositoryProvider));
});

/// Provides the filtered todo list.
final filteredTodosProvider = Provider<List<Todo>>((ref) {
  final state = ref.watch(todoProvider);

  return switch (state.filter) {
    TodoFilter.all => state.todos,
    TodoFilter.active => state.todos.where((t) => !t.isCompleted).toList(),
    TodoFilter.completed => state.todos.where((t) => t.isCompleted).toList(),
  };
});
```

### NotifierProvider (Riverpod 2.0+ Style)

```dart
/// Manages authentication state.
class AuthNotifier extends Notifier<AuthState> {
  @override
  AuthState build() {
    return const AuthState.initial();
  }

  Future<void> login(String email, String password) async {
    state = const AuthState.loading();

    try {
      final user = await ref.read(authRepositoryProvider).login(email, password);
      state = AuthState.authenticated(user);
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }

  Future<void> logout() async {
    await ref.read(authRepositoryProvider).logout();
    state = const AuthState.unauthenticated();
  }
}

final authProvider = NotifierProvider<AuthNotifier, AuthState>(() {
  return AuthNotifier();
});
```

### AsyncNotifierProvider (Async Initialization)

```dart
/// Manages user profile with async initialization.
class UserProfileNotifier extends AsyncNotifier<UserProfile> {
  @override
  Future<UserProfile> build() async {
    return ref.read(userRepositoryProvider).getCurrentProfile();
  }

  Future<void> updateName(String name) async {
    state = const AsyncLoading();

    state = await AsyncValue.guard(() async {
      final profile = await ref.read(userRepositoryProvider).updateProfile(
        name: name,
      );
      return profile;
    });
  }
}

final userProfileProvider = AsyncNotifierProvider<UserProfileNotifier, UserProfile>(() {
  return UserProfileNotifier();
});
```

## Provider Modifiers

### autoDispose

```dart
/// Auto-disposes when no longer listened to.
final searchResultsProvider = FutureProvider.autoDispose
    .family<List<Product>, String>((ref, query) async {
  // Cancel if disposed before completing
  final cancelToken = CancelToken();
  ref.onDispose(cancelToken.cancel);

  return ref.watch(productApiProvider).search(query, cancelToken: cancelToken);
});
```

### family

```dart
/// Provides a user by ID.
final userProvider = FutureProvider.family<User, String>((ref, userId) async {
  return ref.watch(userRepositoryProvider).getUser(userId);
});

// Usage
final user = ref.watch(userProvider('user-123'));
```

## Dependency Injection Pattern

```dart
// Repository provider
final userRepositoryProvider = Provider<UserRepository>((ref) {
  return UserRepositoryImpl(
    ref.watch(apiClientProvider),
    ref.watch(localStorageProvider),
  );
});

// API client provider
final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient(baseUrl: 'https://api.example.com');
});

// Local storage provider
final localStorageProvider = Provider<LocalStorage>((ref) {
  return SharedPreferencesStorage();
});
```

## Provider Checklist

- [ ] Use `autoDispose` for providers tied to screen lifecycle
- [ ] Use `family` for parameterized providers
- [ ] Add doc comments describing the provider
- [ ] Keep state classes immutable
- [ ] Handle loading and error states
- [ ] Use `ref.watch` for reactive dependencies
- [ ] Use `ref.read` for one-time reads (in callbacks)
- [ ] Implement `copyWith` for state classes
- [ ] Use sealed classes for complex states

## File Organization

```
lib/
├── features/
│   └── auth/
│       └── presentation/
│           └── providers/
│               ├── auth_provider.dart
│               └── auth_state.dart
└── shared/
    └── providers/
        ├── api_client_provider.dart
        └── local_storage_provider.dart
```
