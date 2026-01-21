---
description: "Generates mock classes and test fixtures using mocktail"
globs: ["test/**/mocks/*.dart", "test/**/fixtures/*.dart"]
alwaysApply: false
---

# Generate Mocks Skill

Generate mock classes for testing using mocktail.

## Trigger
- "generate mocks"
- "create mocks"
- "mock classes"
- "test mocks"

## Parameters
- **classes**: List of classes to mock
- **output**: Output file path (default: test/mocks/mocks.dart)

## Dependencies Required

```yaml
dev_dependencies:
  mocktail: ^1.0.3
  bloc_test: ^9.1.5  # For BLoC mocks
```

## Generated Code

### Basic Mocks File

```dart
// test/mocks/mocks.dart
import 'package:mocktail/mocktail.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:bloc_test/bloc_test.dart';

// ============================================================
// Repository Mocks
// ============================================================

class MockAuthRepository extends Mock implements AuthRepository {}

class MockUserRepository extends Mock implements UserRepository {}

class MockProductRepository extends Mock implements ProductRepository {}

class MockOrderRepository extends Mock implements OrderRepository {}

// ============================================================
// Service Mocks
// ============================================================

class MockApiClient extends Mock implements ApiClient {}

class MockStorageService extends Mock implements StorageService {}

class MockAnalyticsService extends Mock implements AnalyticsService {}

class MockNotificationService extends Mock implements NotificationService {}

// ============================================================
// Data Source Mocks
// ============================================================

class MockAuthRemoteDataSource extends Mock implements AuthRemoteDataSource {}

class MockAuthLocalDataSource extends Mock implements AuthLocalDataSource {}

class MockUserRemoteDataSource extends Mock implements UserRemoteDataSource {}

// ============================================================
// BLoC/Cubit Mocks
// ============================================================

class MockAuthBloc extends MockBloc<AuthEvent, AuthState> implements AuthBloc {}

class MockAuthCubit extends MockCubit<AuthState> implements AuthCubit {}

class MockUserBloc extends MockBloc<UserEvent, UserState> implements UserBloc {}

// ============================================================
// Use Case Mocks
// ============================================================

class MockSignIn extends Mock implements SignIn {}

class MockSignOut extends Mock implements SignOut {}

class MockGetUser extends Mock implements GetUser {}

class MockGetAllProducts extends Mock implements GetAllProducts {}

// ============================================================
// External Service Mocks
// ============================================================

class MockNavigatorObserver extends Mock implements NavigatorObserver {}

class MockBuildContext extends Mock implements BuildContext {}

// ============================================================
// Fake Classes (for registerFallbackValue)
// ============================================================

class FakeUser extends Fake implements User {}

class FakeProduct extends Fake implements Product {}

class FakeOrder extends Fake implements Order {}

class FakeRoute extends Fake implements Route<dynamic> {}

class FakeAuthEvent extends Fake implements AuthEvent {}

class FakeAuthState extends Fake implements AuthState {}

// ============================================================
// Setup Function
// ============================================================

/// Call this in setUpAll() to register all fake values
void registerAllFallbackValues() {
  registerFallbackValue(FakeUser());
  registerFallbackValue(FakeProduct());
  registerFallbackValue(FakeOrder());
  registerFallbackValue(FakeRoute());
  registerFallbackValue(FakeAuthEvent());
  registerFallbackValue(FakeAuthState());
}
```

### Mock Extensions

```dart
// test/mocks/mock_extensions.dart
import 'package:mocktail/mocktail.dart';
import 'mocks.dart';

// ============================================================
// AuthRepository Mock Extensions
// ============================================================

extension MockAuthRepositoryX on MockAuthRepository {
  void stubSignInSuccess(User user) {
    when(() => signIn(any(), any())).thenAnswer((_) async => Right(user));
  }

  void stubSignInFailure(Failure failure) {
    when(() => signIn(any(), any())).thenAnswer((_) async => Left(failure));
  }

  void stubSignInException(Exception exception) {
    when(() => signIn(any(), any())).thenThrow(exception);
  }

  void stubSignOutSuccess() {
    when(() => signOut()).thenAnswer((_) async => const Right(null));
  }

  void stubGetCurrentUserSuccess(User? user) {
    when(() => getCurrentUser()).thenAnswer((_) async => Right(user));
  }

  void stubGetCurrentUserFailure(Failure failure) {
    when(() => getCurrentUser()).thenAnswer((_) async => Left(failure));
  }
}

// ============================================================
// UserRepository Mock Extensions
// ============================================================

extension MockUserRepositoryX on MockUserRepository {
  void stubGetUserSuccess(User user) {
    when(() => getUser(any())).thenAnswer((_) async => Right(user));
  }

  void stubGetUserFailure(Failure failure) {
    when(() => getUser(any())).thenAnswer((_) async => Left(failure));
  }

  void stubGetAllUsersSuccess(List<User> users) {
    when(() => getAllUsers()).thenAnswer((_) async => Right(users));
  }

  void stubUpdateUserSuccess(User user) {
    when(() => updateUser(any())).thenAnswer((_) async => Right(user));
  }

  void stubDeleteUserSuccess() {
    when(() => deleteUser(any())).thenAnswer((_) async => const Right(null));
  }
}

// ============================================================
// ProductRepository Mock Extensions
// ============================================================

extension MockProductRepositoryX on MockProductRepository {
  void stubGetProductSuccess(Product product) {
    when(() => getProduct(any())).thenAnswer((_) async => Right(product));
  }

  void stubGetAllProductsSuccess(List<Product> products) {
    when(() => getAllProducts()).thenAnswer((_) async => Right(products));
  }

  void stubSearchProductsSuccess(List<Product> products) {
    when(() => searchProducts(any())).thenAnswer((_) async => Right(products));
  }
}

// ============================================================
// ApiClient Mock Extensions
// ============================================================

extension MockApiClientX on MockApiClient {
  void stubGetSuccess(String path, Map<String, dynamic> response) {
    when(() => get(path)).thenAnswer((_) async => response);
  }

  void stubPostSuccess(String path, Map<String, dynamic> response) {
    when(() => post(path, body: any(named: 'body')))
        .thenAnswer((_) async => response);
  }

  void stubPutSuccess(String path, Map<String, dynamic> response) {
    when(() => put(path, body: any(named: 'body')))
        .thenAnswer((_) async => response);
  }

  void stubDeleteSuccess(String path) {
    when(() => delete(path)).thenAnswer((_) async => {});
  }

  void stubGetFailure(String path, Exception exception) {
    when(() => get(path)).thenThrow(exception);
  }

  void stubNetworkError() {
    when(() => get(any())).thenThrow(const NetworkException('No connection'));
    when(() => post(any(), body: any(named: 'body')))
        .thenThrow(const NetworkException('No connection'));
  }
}

// ============================================================
// StorageService Mock Extensions
// ============================================================

extension MockStorageServiceX on MockStorageService {
  void stubReadSuccess(String key, String? value) {
    when(() => read(key)).thenAnswer((_) async => value);
  }

  void stubWriteSuccess(String key) {
    when(() => write(key, any())).thenAnswer((_) async {});
  }

  void stubDeleteSuccess(String key) {
    when(() => delete(key)).thenAnswer((_) async {});
  }

  void stubClearSuccess() {
    when(() => clear()).thenAnswer((_) async {});
  }
}
```

### Mock Helpers

```dart
// test/mocks/mock_helpers.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

/// Creates a mock navigator key with stubbed methods
GlobalKey<NavigatorState> createMockNavigatorKey() {
  final key = GlobalKey<NavigatorState>();
  return key;
}

/// Stub any matcher for common types
void stubAnyMatchers() {
  // Useful when you need to match any argument of a specific type
}

/// Create a mock callback that can be verified
class MockCallback<T> extends Mock {
  void call(T value);
}

/// Create a mock void callback
class MockVoidCallback extends Mock {
  void call();
}

/// Verify a callback was called with specific value
void verifyCallbackCalled<T>(MockCallback<T> callback, T value) {
  verify(() => callback(value)).called(1);
}

/// Create a captured argument matcher
T captureArgument<T>(void Function() verification) {
  verification();
  return verify(() => verification()).captured.first as T;
}
```

### Test Fixtures

```dart
// test/fixtures/test_fixtures.dart

/// Factory methods for creating test data
class TestFixtures {
  TestFixtures._();

  // ============================================================
  // User Fixtures
  // ============================================================

  static User user({
    String? id,
    String? email,
    String? name,
    List<String>? roles,
    DateTime? createdAt,
  }) {
    return User(
      id: id ?? 'test-user-id',
      email: email ?? 'test@example.com',
      name: name ?? 'Test User',
      roles: roles ?? ['user'],
      createdAt: createdAt ?? DateTime(2024, 1, 1),
    );
  }

  static User adminUser({String? id}) {
    return user(
      id: id ?? 'admin-user-id',
      email: 'admin@example.com',
      name: 'Admin User',
      roles: ['admin', 'user'],
    );
  }

  static List<User> users(int count) {
    return List.generate(
      count,
      (i) => user(
        id: 'user-$i',
        email: 'user$i@example.com',
        name: 'User $i',
      ),
    );
  }

  // ============================================================
  // Product Fixtures
  // ============================================================

  static Product product({
    String? id,
    String? name,
    String? description,
    double? price,
    int? stock,
  }) {
    return Product(
      id: id ?? 'test-product-id',
      name: name ?? 'Test Product',
      description: description ?? 'A test product description',
      price: price ?? 9.99,
      stock: stock ?? 100,
    );
  }

  static List<Product> products(int count) {
    return List.generate(
      count,
      (i) => product(
        id: 'product-$i',
        name: 'Product $i',
        price: 9.99 + i,
      ),
    );
  }

  // ============================================================
  // Order Fixtures
  // ============================================================

  static Order order({
    String? id,
    String? userId,
    List<OrderItem>? items,
    OrderStatus? status,
    double? total,
  }) {
    return Order(
      id: id ?? 'test-order-id',
      userId: userId ?? 'test-user-id',
      items: items ?? [orderItem()],
      status: status ?? OrderStatus.pending,
      total: total ?? 99.99,
      createdAt: DateTime(2024, 1, 1),
    );
  }

  static OrderItem orderItem({
    String? productId,
    int? quantity,
    double? price,
  }) {
    return OrderItem(
      productId: productId ?? 'test-product-id',
      quantity: quantity ?? 1,
      price: price ?? 9.99,
    );
  }

  // ============================================================
  // API Response Fixtures
  // ============================================================

  static Map<String, dynamic> userJson({
    String? id,
    String? email,
    String? name,
  }) {
    return {
      'id': id ?? 'test-user-id',
      'email': email ?? 'test@example.com',
      'name': name ?? 'Test User',
      'roles': ['user'],
      'created_at': '2024-01-01T00:00:00.000Z',
    };
  }

  static Map<String, dynamic> productJson({String? id}) {
    return {
      'id': id ?? 'test-product-id',
      'name': 'Test Product',
      'description': 'A test product',
      'price': 9.99,
      'stock': 100,
    };
  }

  static Map<String, dynamic> paginatedResponse<T>(
    List<Map<String, dynamic>> items, {
    int page = 1,
    int perPage = 10,
    int total = 100,
  }) {
    return {
      'data': items,
      'meta': {
        'current_page': page,
        'per_page': perPage,
        'total_items': total,
        'total_pages': (total / perPage).ceil(),
        'has_next': page * perPage < total,
        'has_previous': page > 1,
      },
    };
  }

  static Map<String, dynamic> errorResponse({
    String message = 'An error occurred',
    String? code,
    List<Map<String, dynamic>>? fieldErrors,
  }) {
    return {
      'error': message,
      if (code != null) 'code': code,
      if (fieldErrors != null) 'errors': fieldErrors,
    };
  }

  // ============================================================
  // Failure Fixtures
  // ============================================================

  static ServerFailure serverFailure([String? message]) {
    return ServerFailure(message ?? 'Server error');
  }

  static NetworkFailure networkFailure([String? message]) {
    return NetworkFailure(message ?? 'No internet connection');
  }

  static CacheFailure cacheFailure([String? message]) {
    return CacheFailure(message ?? 'Cache error');
  }

  static ValidationFailure validationFailure([String? message]) {
    return ValidationFailure(message ?? 'Validation failed');
  }
}
```

### Usage in Tests

```dart
// test/features/auth/domain/usecases/sign_in_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';

import '../../../../mocks/mocks.dart';
import '../../../../mocks/mock_extensions.dart';
import '../../../../fixtures/test_fixtures.dart';

void main() {
  late SignIn signIn;
  late MockAuthRepository mockRepository;

  setUpAll(() {
    registerAllFallbackValues();
  });

  setUp(() {
    mockRepository = MockAuthRepository();
    signIn = SignIn(mockRepository);
  });

  group('SignIn', () {
    const email = 'test@example.com';
    const password = 'password123';
    final user = TestFixtures.user();

    test('should return user when credentials are valid', () async {
      // Arrange
      mockRepository.stubSignInSuccess(user);

      // Act
      final result = await signIn(SignInParams(
        email: email,
        password: password,
      ));

      // Assert
      expect(result, Right(user));
      verify(() => mockRepository.signIn(email, password)).called(1);
    });

    test('should return failure when credentials are invalid', () async {
      // Arrange
      final failure = TestFixtures.serverFailure('Invalid credentials');
      mockRepository.stubSignInFailure(failure);

      // Act
      final result = await signIn(SignInParams(
        email: email,
        password: password,
      ));

      // Assert
      expect(result, Left(failure));
    });
  });
}
```

### BLoC Test Example

```dart
// test/features/auth/presentation/bloc/auth_bloc_test.dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import '../../../../mocks/mocks.dart';
import '../../../../fixtures/test_fixtures.dart';

void main() {
  late AuthBloc bloc;
  late MockSignIn mockSignIn;
  late MockSignOut mockSignOut;

  setUpAll(() {
    registerAllFallbackValues();
  });

  setUp(() {
    mockSignIn = MockSignIn();
    mockSignOut = MockSignOut();
    bloc = AuthBloc(signIn: mockSignIn, signOut: mockSignOut);
  });

  tearDown(() {
    bloc.close();
  });

  group('AuthBloc', () {
    final user = TestFixtures.user();

    test('initial state is AuthInitial', () {
      expect(bloc.state, const AuthInitial());
    });

    blocTest<AuthBloc, AuthState>(
      'emits [AuthLoading, AuthAuthenticated] when sign in succeeds',
      build: () {
        when(() => mockSignIn(any())).thenAnswer((_) async => Right(user));
        return bloc;
      },
      act: (bloc) => bloc.add(AuthSignInRequested(
        email: 'test@example.com',
        password: 'password',
      )),
      expect: () => [
        const AuthLoading(),
        AuthAuthenticated(user),
      ],
      verify: (_) {
        verify(() => mockSignIn(any())).called(1);
      },
    );

    blocTest<AuthBloc, AuthState>(
      'emits [AuthLoading, AuthError] when sign in fails',
      build: () {
        when(() => mockSignIn(any())).thenAnswer(
          (_) async => Left(TestFixtures.serverFailure()),
        );
        return bloc;
      },
      act: (bloc) => bloc.add(AuthSignInRequested(
        email: 'test@example.com',
        password: 'password',
      )),
      expect: () => [
        const AuthLoading(),
        const AuthError('Server error'),
      ],
    );
  });
}
```

## Generate Command

To auto-generate mock file based on project structure:

```bash
# Run mock generator script
dart run tool/generate_mocks.dart
```

## Usage Examples

```
User: generate mocks for AuthRepository, UserRepository
User: create mocks for all repositories and services
User: generate test fixtures for User, Product entities
```
