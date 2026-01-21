---
description: "Creates domain layer use cases following clean architecture patterns"
globs: ["lib/**/usecases/*.dart", "lib/**/domain/**/*_usecase.dart"]
alwaysApply: false
---

# Create Use Case Skill

Create a domain layer use case following clean architecture patterns.

## Trigger Keywords
- create usecase
- create use case
- new usecase
- domain usecase
- add usecase

## Use Case Template

```dart
import 'package:fpdart/fpdart.dart';

/// Use case for [describing what this use case does].
///
/// Example:
/// ```dart
/// final result = await useCase(GetUserParams(id: 'user-123'));
/// result.fold(
///   (failure) => print('Error: $failure'),
///   (user) => print('User: ${user.name}'),
/// );
/// ```
class [UseCaseName]UseCase {
  const [UseCaseName]UseCase(this._repository);

  final [Repository]Repository _repository;

  /// Executes the use case.
  ///
  /// Parameters:
  /// - [params]: The parameters required for this operation.
  ///
  /// Returns either a [Failure] or [ReturnType].
  Future<Either<Failure, [ReturnType]>> call([Params] params) async {
    return _repository.[method](params.[field]);
  }
}

/// Parameters for [UseCaseName].
class [Params] {
  const [Params]({
    required this.[field],
  });

  final [Type] [field];
}
```

## Simple Use Case (No Params)

```dart
/// Use case for fetching current user.
class GetCurrentUserUseCase {
  const GetCurrentUserUseCase(this._repository);

  final AuthRepository _repository;

  Future<Either<Failure, User>> call() async {
    return _repository.getCurrentUser();
  }
}
```

## Use Case with Multiple Dependencies

```dart
/// Use case for creating an order with payment processing.
class CreateOrderUseCase {
  const CreateOrderUseCase(
    this._orderRepository,
    this._paymentService,
    this._inventoryService,
  );

  final OrderRepository _orderRepository;
  final PaymentService _paymentService;
  final InventoryService _inventoryService;

  Future<Either<Failure, Order>> call(CreateOrderParams params) async {
    // Validate inventory
    final inventoryCheck = await _inventoryService.checkAvailability(
      params.items,
    );

    if (inventoryCheck.isLeft()) {
      return inventoryCheck.map((_) => throw UnimplementedError());
    }

    // Process payment
    final paymentResult = await _paymentService.processPayment(
      amount: params.totalAmount,
      method: params.paymentMethod,
    );

    return paymentResult.flatMap((payment) async {
      // Create order
      return _orderRepository.createOrder(
        items: params.items,
        paymentId: payment.id,
      );
    });
  }
}

class CreateOrderParams {
  const CreateOrderParams({
    required this.items,
    required this.totalAmount,
    required this.paymentMethod,
  });

  final List<OrderItem> items;
  final double totalAmount;
  final PaymentMethod paymentMethod;
}
```

## Stream Use Case

```dart
/// Use case for watching user notifications in real-time.
class WatchNotificationsUseCase {
  const WatchNotificationsUseCase(this._repository);

  final NotificationRepository _repository;

  Stream<Either<Failure, List<Notification>>> call(String userId) {
    return _repository.watchNotifications(userId);
  }
}
```

## Use Case with Validation

```dart
/// Use case for user registration with validation.
class RegisterUserUseCase {
  const RegisterUserUseCase(this._repository);

  final AuthRepository _repository;

  Future<Either<Failure, User>> call(RegisterParams params) async {
    // Validate input
    final validationResult = _validate(params);
    if (validationResult != null) {
      return Left(ValidationFailure(validationResult));
    }

    return _repository.register(
      email: params.email,
      password: params.password,
      name: params.name,
    );
  }

  String? _validate(RegisterParams params) {
    if (!_isValidEmail(params.email)) {
      return 'Invalid email format';
    }
    if (params.password.length < 8) {
      return 'Password must be at least 8 characters';
    }
    if (params.name.isEmpty) {
      return 'Name is required';
    }
    return null;
  }

  bool _isValidEmail(String email) {
    return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(email);
  }
}

class RegisterParams {
  const RegisterParams({
    required this.email,
    required this.password,
    required this.name,
  });

  final String email;
  final String password;
  final String name;
}
```

## File Location

```
lib/
└── features/
    └── [feature_name]/
        └── domain/
            └── usecases/
                └── [usecase_name]_usecase.dart
```

## Provider Integration

```dart
// Use case provider
final [useCaseName]UseCaseProvider = Provider<[UseCaseName]UseCase>((ref) {
  final repository = ref.watch([repository]Provider);
  return [UseCaseName]UseCase(repository);
});

// Usage in presentation layer
final result = await ref.read([useCaseName]UseCaseProvider).call(params);
```

## Testing Template

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';

class MockRepository extends Mock implements [Repository]Repository {}

void main() {
  late [UseCaseName]UseCase useCase;
  late MockRepository mockRepository;

  setUp(() {
    mockRepository = MockRepository();
    useCase = [UseCaseName]UseCase(mockRepository);
  });

  group('[UseCaseName]UseCase', () {
    test('should return [ReturnType] on success', () async {
      // Arrange
      when(() => mockRepository.[method](any()))
          .thenAnswer((_) async => Right([expectedResult]));

      // Act
      final result = await useCase([Params]([testParams]));

      // Assert
      expect(result, Right([expectedResult]));
      verify(() => mockRepository.[method]([testParams])).called(1);
    });

    test('should return Failure on error', () async {
      // Arrange
      final failure = ServerFailure('Error');
      when(() => mockRepository.[method](any()))
          .thenAnswer((_) async => Left(failure));

      // Act
      final result = await useCase([Params]([testParams]));

      // Assert
      expect(result, Left(failure));
    });
  });
}
```

## Checklist

- [ ] Single responsibility (one use case per operation)
- [ ] Depends on repository abstractions, not implementations
- [ ] Has dedicated Params class for multiple parameters
- [ ] Includes validation where appropriate
- [ ] Returns Either<Failure, Success> for error handling
- [ ] Has corresponding provider
- [ ] Includes unit tests
