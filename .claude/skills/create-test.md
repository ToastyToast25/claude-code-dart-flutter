---
description: "Creates unit tests, widget tests, and integration tests for Dart/Flutter"
globs: ["test/**/*_test.dart", "integration_test/**/*.dart"]
alwaysApply: false
---

# Skill: Create Dart Test

Create comprehensive tests following Dart and Flutter testing best practices.

## Usage

When asked to create tests, follow these guidelines:

## Unit Test Template

```dart
import 'package:test/test.dart';

import 'package:my_app/src/calculator.dart';

void main() {
  group('Calculator', () {
    late Calculator calculator;

    setUp(() {
      calculator = Calculator();
    });

    group('add', () {
      test('should return sum of two positive numbers', () {
        // Arrange
        const a = 2;
        const b = 3;

        // Act
        final result = calculator.add(a, b);

        // Assert
        expect(result, equals(5));
      });

      test('should handle negative numbers', () {
        expect(calculator.add(-1, 1), equals(0));
        expect(calculator.add(-1, -1), equals(-2));
      });

      test('should handle zero', () {
        expect(calculator.add(0, 5), equals(5));
        expect(calculator.add(5, 0), equals(5));
      });
    });

    group('divide', () {
      test('should return quotient of two numbers', () {
        expect(calculator.divide(10, 2), equals(5));
      });

      test('should throw ArgumentError when dividing by zero', () {
        expect(
          () => calculator.divide(10, 0),
          throwsA(isA<ArgumentError>()),
        );
      });
    });
  });
}
```

## Widget Test Template

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:my_app/src/widgets/counter_widget.dart';

void main() {
  group('CounterWidget', () {
    testWidgets('should display initial count of 0', (tester) async {
      // Arrange & Act
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CounterWidget(),
          ),
        ),
      );

      // Assert
      expect(find.text('0'), findsOneWidget);
      expect(find.text('1'), findsNothing);
    });

    testWidgets('should increment count when add button is pressed',
        (tester) async {
      // Arrange
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CounterWidget(),
          ),
        ),
      );

      // Act
      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();

      // Assert
      expect(find.text('1'), findsOneWidget);
    });

    testWidgets('should decrement count when subtract button is pressed',
        (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CounterWidget(initialValue: 5),
          ),
        ),
      );

      await tester.tap(find.byIcon(Icons.remove));
      await tester.pump();

      expect(find.text('4'), findsOneWidget);
    });

    testWidgets('should call onChanged callback when count changes',
        (tester) async {
      int? changedValue;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CounterWidget(
              onChanged: (value) => changedValue = value,
            ),
          ),
        ),
      );

      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();

      expect(changedValue, equals(1));
    });
  });
}
```

## Async Test Template

```dart
import 'package:test/test.dart';

import 'package:my_app/src/services/user_service.dart';

void main() {
  group('UserService', () {
    late UserService userService;
    late MockUserRepository mockRepository;

    setUp(() {
      mockRepository = MockUserRepository();
      userService = UserService(mockRepository);
    });

    group('getUser', () {
      test('should return user when repository succeeds', () async {
        // Arrange
        final expectedUser = User(id: '1', name: 'John');
        when(() => mockRepository.getUser('1'))
            .thenAnswer((_) async => expectedUser);

        // Act
        final result = await userService.getUser('1');

        // Assert
        expect(result, equals(expectedUser));
        verify(() => mockRepository.getUser('1')).called(1);
      });

      test('should throw NotFoundException when user does not exist', () async {
        when(() => mockRepository.getUser('unknown'))
            .thenThrow(NotFoundException('User not found'));

        expect(
          () => userService.getUser('unknown'),
          throwsA(isA<NotFoundException>()),
        );
      });
    });

    group('fetchUsers', () {
      test('should return empty list when no users exist', () async {
        when(() => mockRepository.getUsers())
            .thenAnswer((_) async => <User>[]);

        final result = await userService.fetchUsers();

        expect(result, isEmpty);
      });
    });
  });
}
```

## Stream Test Template

```dart
import 'package:test/test.dart';

void main() {
  group('MessageStream', () {
    test('should emit messages in order', () async {
      final stream = Stream.fromIterable(['a', 'b', 'c']);

      await expectLater(
        stream,
        emitsInOrder(['a', 'b', 'c']),
      );
    });

    test('should emit error', () async {
      final stream = Stream<int>.error(Exception('Failed'));

      await expectLater(
        stream,
        emitsError(isA<Exception>()),
      );
    });

    test('should complete after emitting values', () async {
      final stream = Stream.fromIterable([1, 2, 3]);

      await expectLater(
        stream,
        emitsInOrder([1, 2, 3, emitsDone]),
      );
    });

    test('should emit multiple values then error', () async {
      final controller = StreamController<int>();
      controller.add(1);
      controller.add(2);
      controller.addError(Exception('Error'));
      controller.close();

      await expectLater(
        controller.stream,
        emitsInOrder([
          1,
          2,
          emitsError(isA<Exception>()),
        ]),
      );
    });
  });
}
```

## Riverpod Provider Test Template

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockUserRepository extends Mock implements UserRepository {}

void main() {
  group('UserNotifier', () {
    late ProviderContainer container;
    late MockUserRepository mockRepository;

    setUp(() {
      mockRepository = MockUserRepository();
      container = ProviderContainer(
        overrides: [
          userRepositoryProvider.overrideWithValue(mockRepository),
        ],
      );
    });

    tearDown(() {
      container.dispose();
    });

    test('should start with initial state', () {
      final state = container.read(userProvider);
      expect(state, isA<UserInitial>());
    });

    test('should load user successfully', () async {
      final expectedUser = User(id: '1', name: 'John');
      when(() => mockRepository.getUser('1'))
          .thenAnswer((_) async => expectedUser);

      await container.read(userProvider.notifier).loadUser('1');

      final state = container.read(userProvider);
      expect(state, isA<UserLoaded>());
      expect((state as UserLoaded).user, equals(expectedUser));
    });

    test('should handle error when loading user fails', () async {
      when(() => mockRepository.getUser('1'))
          .thenThrow(Exception('Network error'));

      await container.read(userProvider.notifier).loadUser('1');

      final state = container.read(userProvider);
      expect(state, isA<UserError>());
    });
  });
}
```

## Widget Test with Riverpod

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('UserScreen', () {
    testWidgets('should display loading indicator initially', (tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: UserScreen(),
          ),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('should display user name when loaded', (tester) async {
      final mockUser = User(id: '1', name: 'John Doe');

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            userProvider.overrideWith((ref) => UserLoaded(mockUser)),
          ],
          child: const MaterialApp(
            home: UserScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();

      expect(find.text('John Doe'), findsOneWidget);
    });

    testWidgets('should display error message on failure', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            userProvider.overrideWith(
              (ref) => const UserError('Failed to load user'),
            ),
          ],
          child: const MaterialApp(
            home: UserScreen(),
          ),
        ),
      );

      expect(find.text('Failed to load user'), findsOneWidget);
    });
  });
}
```

## Common Matchers Reference

```dart
// Equality
expect(actual, equals(expected));
expect(actual, isNot(equals(other)));
expect(actual, same(identical)); // Same object reference

// Type checking
expect(actual, isA<String>());
expect(actual, isNull);
expect(actual, isNotNull);
expect(actual, isTrue);
expect(actual, isFalse);

// Collections
expect(list, contains(element));
expect(list, containsAll([a, b]));
expect(list, containsAllInOrder([a, b, c]));
expect(list, hasLength(3));
expect(list, isEmpty);
expect(list, isNotEmpty);
expect(map, containsPair('key', 'value'));

// Numeric
expect(num, greaterThan(5));
expect(num, greaterThanOrEqualTo(5));
expect(num, lessThan(10));
expect(num, lessThanOrEqualTo(10));
expect(num, inInclusiveRange(1, 10));
expect(num, inExclusiveRange(1, 10));
expect(double, closeTo(3.14, 0.01));

// Strings
expect(str, startsWith('Hello'));
expect(str, endsWith('World'));
expect(str, contains('middle'));
expect(str, matches(RegExp(r'\d+')));
expect(str, equalsIgnoringCase('HELLO'));

// Exceptions
expect(() => fn(), throwsException);
expect(() => fn(), throwsA(isA<CustomError>()));
expect(() => fn(), throwsArgumentError);
expect(() => fn(), throwsStateError);
expect(() => fn(), returnsNormally);

// Widget finders
expect(find.text('Hello'), findsOneWidget);
expect(find.byType(Button), findsNothing);
expect(find.byKey(Key('key')), findsNWidgets(2));
expect(find.byIcon(Icons.add), findsWidgets);
expect(find.byType(TextField), findsAtLeast(1));
```

## Test File Checklist

- [ ] Import test package (`test` or `flutter_test`)
- [ ] Use descriptive `group` and `test` names
- [ ] Follow Arrange-Act-Assert pattern
- [ ] Use `setUp` and `tearDown` for shared setup
- [ ] Mock external dependencies
- [ ] Test edge cases and error conditions
- [ ] Keep tests independent
- [ ] Use meaningful variable names
- [ ] Clean up resources in `tearDown`
