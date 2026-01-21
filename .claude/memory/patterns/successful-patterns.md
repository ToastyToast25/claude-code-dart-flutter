# Successful Patterns

Patterns that work well in Dart/Flutter projects. Use these as starting points.

---

## Pattern: Repository with Either Result

**Use Case:** Data layer error handling without exceptions

**Why It Works:**
- Explicit error handling at compile time
- No try-catch scattered throughout codebase
- Forces callers to handle both success and failure

**Implementation:**
```dart
// lib/core/result/result.dart
import 'package:fpdart/fpdart.dart';

typedef Result<T> = Either<Failure, T>;

// lib/features/user/domain/repositories/user_repository.dart
abstract class UserRepository {
  Future<Result<User>> getUser(String id);
  Future<Result<List<User>>> getAllUsers();
  Future<Result<User>> createUser(CreateUserDto dto);
}

// lib/features/user/data/repositories/user_repository_impl.dart
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource _remote;
  final NetworkInfo _networkInfo;

  @override
  Future<Result<User>> getUser(String id) async {
    if (!await _networkInfo.isConnected) {
      return Left(NetworkFailure('No internet connection'));
    }

    try {
      final model = await _remote.getUser(id);
      return Right(model.toEntity());
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    } on NotFoundException {
      return Left(NotFoundFailure('User not found'));
    }
  }
}

// Usage in BLoC/Provider
final result = await repository.getUser(id);
result.fold(
  (failure) => emit(UserError(failure.message)),
  (user) => emit(UserLoaded(user)),
);
```

**Files:** Repository interface, Repository impl, Failure classes

---

## Pattern: Feature-First Folder Structure

**Use Case:** Organizing code by feature rather than type

**Why It Works:**
- Related code stays together
- Easy to find files
- Features are self-contained and deletable
- Scales with app size

**Implementation:**
```
lib/
├── app/
│   ├── app.dart
│   └── router.dart
├── core/
│   ├── config/
│   ├── extensions/
│   ├── utils/
│   └── result/
├── shared/
│   ├── data/
│   │   └── api_client.dart
│   └── presentation/
│       ├── theme/
│       └── widgets/
└── features/
    ├── auth/
    │   ├── data/
    │   │   ├── datasources/
    │   │   ├── models/
    │   │   └── repositories/
    │   ├── domain/
    │   │   ├── entities/
    │   │   ├── repositories/
    │   │   └── usecases/
    │   └── presentation/
    │       ├── bloc/
    │       ├── pages/
    │       └── widgets/
    └── products/
        ├── data/
        ├── domain/
        └── presentation/
```

**Files:** All feature files

---

## Pattern: Sealed Classes for State

**Use Case:** Type-safe state representation with exhaustive pattern matching

**Why It Works:**
- Compiler enforces handling all states
- No invalid state combinations
- Clear, self-documenting code

**Implementation:**
```dart
// State definition
sealed class AuthState {
  const AuthState();
}

final class AuthInitial extends AuthState {
  const AuthInitial();
}

final class AuthLoading extends AuthState {
  const AuthLoading();
}

final class AuthAuthenticated extends AuthState {
  const AuthAuthenticated(this.user);
  final User user;
}

final class AuthUnauthenticated extends AuthState {
  const AuthUnauthenticated();
}

final class AuthError extends AuthState {
  const AuthError(this.message);
  final String message;
}

// Usage with pattern matching
Widget build(BuildContext context) {
  return BlocBuilder<AuthBloc, AuthState>(
    builder: (context, state) {
      return switch (state) {
        AuthInitial() => const SplashScreen(),
        AuthLoading() => const LoadingIndicator(),
        AuthAuthenticated(:final user) => HomeScreen(user: user),
        AuthUnauthenticated() => const LoginScreen(),
        AuthError(:final message) => ErrorScreen(message: message),
      };
    },
  );
}
```

**Files:** State files, UI builders

---

## Pattern: Dependency Injection with Riverpod

**Use Case:** Clean, testable dependency injection

**Why It Works:**
- Dependencies are explicit
- Easy to mock for testing
- No service locator anti-pattern
- Compile-time safe

**Implementation:**
```dart
// Providers for dependencies
final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient(baseUrl: Env.apiUrl);
});

final userRemoteDataSourceProvider = Provider<UserRemoteDataSource>((ref) {
  return UserRemoteDataSourceImpl(ref.watch(apiClientProvider));
});

final userRepositoryProvider = Provider<UserRepository>((ref) {
  return UserRepositoryImpl(
    remoteDataSource: ref.watch(userRemoteDataSourceProvider),
    networkInfo: ref.watch(networkInfoProvider),
  );
});

// Feature provider using dependencies
final userProvider = FutureProvider.family<User, String>((ref, userId) async {
  final repository = ref.watch(userRepositoryProvider);
  final result = await repository.getUser(userId);
  return result.fold(
    (failure) => throw failure,
    (user) => user,
  );
});

// Testing - easy to override
void main() {
  testWidgets('shows user name', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          userRepositoryProvider.overrideWithValue(MockUserRepository()),
        ],
        child: const MyApp(),
      ),
    );
  });
}
```

**Files:** Provider definitions, test setup

---

## Pattern: Extension Methods for Context

**Use Case:** Cleaner access to theme, text styles, navigation

**Why It Works:**
- Reduces boilerplate
- Consistent access patterns
- Easy to add project-specific helpers

**Implementation:**
```dart
// lib/core/extensions/context_extension.dart
extension BuildContextX on BuildContext {
  // Theme shortcuts
  ThemeData get theme => Theme.of(this);
  TextTheme get textTheme => theme.textTheme;
  ColorScheme get colorScheme => theme.colorScheme;

  // Size shortcuts
  Size get screenSize => MediaQuery.sizeOf(this);
  double get screenWidth => screenSize.width;
  double get screenHeight => screenSize.height;

  // Responsive helpers
  bool get isMobile => screenWidth < 600;
  bool get isTablet => screenWidth >= 600 && screenWidth < 1200;
  bool get isDesktop => screenWidth >= 1200;

  // Navigation (if not using GoRouter)
  void pop<T>([T? result]) => Navigator.of(this).pop(result);
  Future<T?> push<T>(Widget page) => Navigator.of(this).push<T>(
    MaterialPageRoute(builder: (_) => page),
  );

  // Snackbar helper
  void showSnackBar(String message, {bool isError = false}) {
    ScaffoldMessenger.of(this).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? colorScheme.error : null,
      ),
    );
  }
}

// Usage
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Text(
      'Hello',
      style: context.textTheme.headlineMedium,
    );
  }
}
```

**Files:** Extension file, usage throughout app

---

## Pattern: Async Value Handling

**Use Case:** Consistent handling of loading/error/data states

**Why It Works:**
- Single pattern for all async UI
- No forgotten loading states
- Clean switch expressions

**Implementation:**
```dart
// With Riverpod's AsyncValue
class UserProfileScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userProvider);

    return userAsync.when(
      loading: () => const Center(
        child: CircularProgressIndicator(),
      ),
      error: (error, stack) => Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Error: $error'),
            ElevatedButton(
              onPressed: () => ref.invalidate(userProvider),
              child: const Text('Retry'),
            ),
          ],
        ),
      ),
      data: (user) => UserProfileContent(user: user),
    );
  }
}

// Reusable wrapper widget
class AsyncValueWidget<T> extends StatelessWidget {
  const AsyncValueWidget({
    required this.value,
    required this.data,
    this.loading,
    this.error,
  });

  final AsyncValue<T> value;
  final Widget Function(T) data;
  final Widget Function()? loading;
  final Widget Function(Object, StackTrace)? error;

  @override
  Widget build(BuildContext context) {
    return value.when(
      loading: loading ?? () => const Center(child: CircularProgressIndicator()),
      error: error ?? (e, s) => Center(child: Text('Error: $e')),
      data: data,
    );
  }
}

// Usage
AsyncValueWidget<User>(
  value: ref.watch(userProvider),
  data: (user) => Text(user.name),
)
```

**Files:** Async widget, all screens using async data

---

## How to Add New Patterns

When a pattern proves successful:

1. Document the use case
2. Explain why it works
3. Provide complete code example
4. List affected files
5. Include testing approach if relevant

---

*Last updated: 2026-01-21*
