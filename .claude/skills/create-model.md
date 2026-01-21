---
description: "Creates Dart data models with JSON serialization, Freezed, or sealed classes"
globs: ["lib/**/models/*.dart", "lib/**/entities/*.dart", "lib/**/domain/**/*.dart"]
alwaysApply: false
---

# Skill: Create Dart Model

Create well-structured data models following Dart best practices.

## Usage

When asked to create a model or data class, follow these guidelines:

## Simple Immutable Model

```dart
/// Represents a user in the system.
class User {
  /// Creates a [User].
  const User({
    required this.id,
    required this.email,
    required this.name,
    this.avatarUrl,
    this.createdAt,
  });

  /// The unique identifier.
  final String id;

  /// The user's email address.
  final String email;

  /// The user's display name.
  final String name;

  /// The user's avatar URL, if available.
  final String? avatarUrl;

  /// When the user was created.
  final DateTime? createdAt;

  /// Creates a copy with the given fields replaced.
  User copyWith({
    String? id,
    String? email,
    String? name,
    String? avatarUrl,
    DateTime? createdAt,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      name: name ?? this.name,
      avatarUrl: avatarUrl ?? this.avatarUrl,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is User &&
        other.id == id &&
        other.email == email &&
        other.name == name &&
        other.avatarUrl == avatarUrl &&
        other.createdAt == createdAt;
  }

  @override
  int get hashCode {
    return Object.hash(id, email, name, avatarUrl, createdAt);
  }

  @override
  String toString() {
    return 'User(id: $id, email: $email, name: $name)';
  }
}
```

## Model with JSON Serialization (Manual)

```dart
/// Represents a user in the system.
class User {
  const User({
    required this.id,
    required this.email,
    required this.name,
    this.avatarUrl,
  });

  final String id;
  final String email;
  final String name;
  final String? avatarUrl;

  /// Creates a [User] from JSON.
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      email: json['email'] as String,
      name: json['name'] as String,
      avatarUrl: json['avatar_url'] as String?,
    );
  }

  /// Converts this [User] to JSON.
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
      'avatar_url': avatarUrl,
    };
  }
}
```

## Model with Freezed (Recommended for Complex Models)

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

/// Represents a user in the system.
@freezed
class User with _$User {
  /// Creates a [User].
  const factory User({
    required String id,
    required String email,
    required String name,
    @JsonKey(name: 'avatar_url') String? avatarUrl,
    @Default(false) bool isVerified,
  }) = _User;

  /// Private constructor for adding methods.
  const User._();

  /// Creates a [User] from JSON.
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);

  /// Returns the user's initials.
  String get initials {
    final parts = name.split(' ');
    if (parts.length >= 2) {
      return '${parts[0][0]}${parts[1][0]}'.toUpperCase();
    }
    return name.isNotEmpty ? name[0].toUpperCase() : '';
  }
}
```

## Enum Models

```dart
/// The status of an order.
enum OrderStatus {
  /// Order is pending payment.
  pending('Pending'),

  /// Order is being processed.
  processing('Processing'),

  /// Order has been shipped.
  shipped('Shipped'),

  /// Order has been delivered.
  delivered('Delivered'),

  /// Order was cancelled.
  cancelled('Cancelled');

  const OrderStatus(this.displayName);

  /// Human-readable name for display.
  final String displayName;

  /// Whether the order is in a final state.
  bool get isFinal => this == delivered || this == cancelled;
}
```

## Sealed Class for Union Types

```dart
/// Represents the result of an operation.
sealed class Result<T> {
  const Result();
}

/// A successful result containing a value.
final class Ok<T> extends Result<T> {
  const Ok(this.value);
  final T value;
}

/// A failed result containing an error.
final class Error<T> extends Result<T> {
  const Error(this.error);
  final Exception error;
}

// Usage with pattern matching
void handleResult(Result<User> result) {
  switch (result) {
    case Ok(:final value):
      print('Got user: ${value.name}');
    case Error(:final error):
      print('Error: $error');
  }
}
```

## State Models with Sealed Classes

```dart
/// The authentication state.
sealed class AuthState {
  const AuthState();
}

/// Initial state before any auth check.
final class AuthInitial extends AuthState {
  const AuthInitial();
}

/// Currently checking authentication.
final class AuthLoading extends AuthState {
  const AuthLoading();
}

/// User is authenticated.
final class AuthAuthenticated extends AuthState {
  const AuthAuthenticated(this.user);
  final User user;
}

/// User is not authenticated.
final class AuthUnauthenticated extends AuthState {
  const AuthUnauthenticated();
}

/// Authentication error occurred.
final class AuthError extends AuthState {
  const AuthError(this.message);
  final String message;
}
```

## Model Checklist

- [ ] Use `const` constructor
- [ ] All fields are `final` (immutable)
- [ ] Add doc comments for class and fields
- [ ] Implement `copyWith` for models that need updates
- [ ] Implement `==` and `hashCode` for value equality
- [ ] Implement `toString` for debugging
- [ ] Use `@JsonKey` for JSON field name mapping
- [ ] Handle nullable fields appropriately
- [ ] Use `@Default` for default values (with Freezed)

## Naming Conventions

- Model class: `UpperCamelCase` (e.g., `UserProfile`)
- File name: `lowercase_with_underscores` (e.g., `user_profile.dart`)
- JSON factory: `fromJson`
- Serialization method: `toJson`

## File Organization

```
lib/
├── features/
│   └── auth/
│       ├── data/
│       │   └── models/
│       │       └── user_model.dart    # DTO with JSON
│       └── domain/
│           └── entities/
│               └── user.dart          # Pure domain entity
```
