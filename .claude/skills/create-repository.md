---
description: "Creates repository pattern implementation with data sources and caching"
globs: ["lib/**/repositories/*.dart", "lib/**/datasources/*.dart", "lib/**/data/**/*.dart"]
alwaysApply: false
---

# Skill: Create Repository

Create well-structured repository classes following the Repository Pattern.

## Usage

When asked to create a repository, follow these guidelines:

## Repository Interface (Domain Layer)

```dart
import '../entities/user.dart';
import '../../shared/domain/result.dart';

/// Repository interface for user data operations.
///
/// This defines the contract for accessing user data without
/// specifying how the data is retrieved or stored.
abstract class UserRepository {
  /// Retrieves a user by their unique identifier.
  ///
  /// Returns [Result.ok] with the user if found.
  /// Returns [Result.error] with [UserNotFoundException] if not found.
  Future<Result<User>> getUser(String id);

  /// Retrieves all users.
  ///
  /// Returns [Result.ok] with the list of users.
  /// Returns [Result.error] if the operation fails.
  Future<Result<List<User>>> getUsers();

  /// Creates a new user.
  ///
  /// Returns [Result.ok] with the created user.
  /// Returns [Result.error] if creation fails.
  Future<Result<User>> createUser(CreateUserRequest request);

  /// Updates an existing user.
  ///
  /// Returns [Result.ok] with the updated user.
  /// Returns [Result.error] if the user doesn't exist or update fails.
  Future<Result<User>> updateUser(String id, UpdateUserRequest request);

  /// Deletes a user by their identifier.
  ///
  /// Returns [Result.ok] with void on success.
  /// Returns [Result.error] if deletion fails.
  Future<Result<void>> deleteUser(String id);

  /// Watches a user for real-time updates.
  ///
  /// Emits the current user state and any subsequent changes.
  Stream<User?> watchUser(String id);

  /// Watches all users for real-time updates.
  Stream<List<User>> watchUsers();
}
```

## Repository Implementation (Data Layer)

```dart
import 'package:flutter/foundation.dart';

import '../../domain/entities/user.dart';
import '../../domain/repositories/user_repository.dart';
import '../../shared/domain/result.dart';
import '../datasources/user_local_datasource.dart';
import '../datasources/user_remote_datasource.dart';
import '../models/user_model.dart';

/// Implementation of [UserRepository] that handles data operations
/// with both remote API and local cache.
class UserRepositoryImpl implements UserRepository {
  /// Creates a [UserRepositoryImpl].
  UserRepositoryImpl({
    required UserRemoteDataSource remoteDataSource,
    required UserLocalDataSource localDataSource,
  })  : _remoteDataSource = remoteDataSource,
        _localDataSource = localDataSource;

  final UserRemoteDataSource _remoteDataSource;
  final UserLocalDataSource _localDataSource;

  @override
  Future<Result<User>> getUser(String id) async {
    try {
      // Try cache first
      final cachedUser = await _localDataSource.getUser(id);
      if (cachedUser != null) {
        // Return cached data but refresh in background
        _refreshUser(id);
        return Result.ok(cachedUser.toEntity());
      }

      // Fetch from remote
      final userModel = await _remoteDataSource.getUser(id);
      await _localDataSource.cacheUser(userModel);
      return Result.ok(userModel.toEntity());
    } on NotFoundException {
      return Result.error(UserNotFoundException(id));
    } on NetworkException catch (e) {
      // Try cache as fallback
      final cachedUser = await _localDataSource.getUser(id);
      if (cachedUser != null) {
        return Result.ok(cachedUser.toEntity());
      }
      return Result.error(e);
    } on Exception catch (e) {
      return Result.error(UnexpectedException(e.toString()));
    }
  }

  @override
  Future<Result<List<User>>> getUsers() async {
    try {
      final userModels = await _remoteDataSource.getUsers();
      await _localDataSource.cacheUsers(userModels);
      return Result.ok(userModels.map((m) => m.toEntity()).toList());
    } on NetworkException catch (e) {
      // Try cache as fallback
      final cachedUsers = await _localDataSource.getUsers();
      if (cachedUsers.isNotEmpty) {
        return Result.ok(cachedUsers.map((m) => m.toEntity()).toList());
      }
      return Result.error(e);
    } on Exception catch (e) {
      return Result.error(UnexpectedException(e.toString()));
    }
  }

  @override
  Future<Result<User>> createUser(CreateUserRequest request) async {
    try {
      final userModel = await _remoteDataSource.createUser(
        CreateUserDto.fromRequest(request),
      );
      await _localDataSource.cacheUser(userModel);
      return Result.ok(userModel.toEntity());
    } on ValidationException catch (e) {
      return Result.error(e);
    } on NetworkException catch (e) {
      return Result.error(e);
    } on Exception catch (e) {
      return Result.error(UnexpectedException(e.toString()));
    }
  }

  @override
  Future<Result<User>> updateUser(String id, UpdateUserRequest request) async {
    try {
      final userModel = await _remoteDataSource.updateUser(
        id,
        UpdateUserDto.fromRequest(request),
      );
      await _localDataSource.cacheUser(userModel);
      return Result.ok(userModel.toEntity());
    } on NotFoundException {
      return Result.error(UserNotFoundException(id));
    } on ValidationException catch (e) {
      return Result.error(e);
    } on Exception catch (e) {
      return Result.error(UnexpectedException(e.toString()));
    }
  }

  @override
  Future<Result<void>> deleteUser(String id) async {
    try {
      await _remoteDataSource.deleteUser(id);
      await _localDataSource.deleteUser(id);
      return const Result.ok(null);
    } on NotFoundException {
      return Result.error(UserNotFoundException(id));
    } on Exception catch (e) {
      return Result.error(UnexpectedException(e.toString()));
    }
  }

  @override
  Stream<User?> watchUser(String id) {
    return _localDataSource.watchUser(id).map((model) => model?.toEntity());
  }

  @override
  Stream<List<User>> watchUsers() {
    return _localDataSource.watchUsers().map(
          (models) => models.map((m) => m.toEntity()).toList(),
        );
  }

  /// Refreshes user data from remote source in background.
  Future<void> _refreshUser(String id) async {
    try {
      final userModel = await _remoteDataSource.getUser(id);
      await _localDataSource.cacheUser(userModel);
    } catch (e) {
      // Silently fail for background refresh
      debugPrint('Background refresh failed for user $id: $e');
    }
  }
}
```

## Data Source Interfaces

```dart
/// Remote data source for user operations.
abstract class UserRemoteDataSource {
  Future<UserModel> getUser(String id);
  Future<List<UserModel>> getUsers();
  Future<UserModel> createUser(CreateUserDto dto);
  Future<UserModel> updateUser(String id, UpdateUserDto dto);
  Future<void> deleteUser(String id);
}

/// Local data source for user caching.
abstract class UserLocalDataSource {
  Future<UserModel?> getUser(String id);
  Future<List<UserModel>> getUsers();
  Future<void> cacheUser(UserModel user);
  Future<void> cacheUsers(List<UserModel> users);
  Future<void> deleteUser(String id);
  Future<void> clearCache();
  Stream<UserModel?> watchUser(String id);
  Stream<List<UserModel>> watchUsers();
}
```

## Remote Data Source Implementation

```dart
/// API implementation of [UserRemoteDataSource].
class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  UserRemoteDataSourceImpl(this._client);

  final ApiClient _client;

  @override
  Future<UserModel> getUser(String id) async {
    final response = await _client.get('/users/$id');
    return UserModel.fromJson(response.data);
  }

  @override
  Future<List<UserModel>> getUsers() async {
    final response = await _client.get('/users');
    final List<dynamic> data = response.data;
    return data.map((json) => UserModel.fromJson(json)).toList();
  }

  @override
  Future<UserModel> createUser(CreateUserDto dto) async {
    final response = await _client.post('/users', data: dto.toJson());
    return UserModel.fromJson(response.data);
  }

  @override
  Future<UserModel> updateUser(String id, UpdateUserDto dto) async {
    final response = await _client.patch('/users/$id', data: dto.toJson());
    return UserModel.fromJson(response.data);
  }

  @override
  Future<void> deleteUser(String id) async {
    await _client.delete('/users/$id');
  }
}
```

## Local Data Source Implementation

```dart
/// Local storage implementation using SharedPreferences/Hive.
class UserLocalDataSourceImpl implements UserLocalDataSource {
  UserLocalDataSourceImpl(this._storage);

  final LocalStorage _storage;
  final _usersController = BehaviorSubject<List<UserModel>>.seeded([]);

  static const _usersKey = 'cached_users';

  @override
  Future<UserModel?> getUser(String id) async {
    final users = await getUsers();
    return users.where((u) => u.id == id).firstOrNull;
  }

  @override
  Future<List<UserModel>> getUsers() async {
    final json = await _storage.getString(_usersKey);
    if (json == null) return [];

    final List<dynamic> data = jsonDecode(json);
    return data.map((j) => UserModel.fromJson(j)).toList();
  }

  @override
  Future<void> cacheUser(UserModel user) async {
    final users = await getUsers();
    final index = users.indexWhere((u) => u.id == user.id);

    if (index >= 0) {
      users[index] = user;
    } else {
      users.add(user);
    }

    await _saveUsers(users);
  }

  @override
  Future<void> cacheUsers(List<UserModel> users) async {
    await _saveUsers(users);
  }

  @override
  Future<void> deleteUser(String id) async {
    final users = await getUsers();
    users.removeWhere((u) => u.id == id);
    await _saveUsers(users);
  }

  @override
  Future<void> clearCache() async {
    await _storage.remove(_usersKey);
    _usersController.add([]);
  }

  @override
  Stream<UserModel?> watchUser(String id) {
    return _usersController.stream.map(
      (users) => users.where((u) => u.id == id).firstOrNull,
    );
  }

  @override
  Stream<List<UserModel>> watchUsers() => _usersController.stream;

  Future<void> _saveUsers(List<UserModel> users) async {
    final json = jsonEncode(users.map((u) => u.toJson()).toList());
    await _storage.setString(_usersKey, json);
    _usersController.add(users);
  }
}
```

## Provider Setup

```dart
// Remote data source provider
final userRemoteDataSourceProvider = Provider<UserRemoteDataSource>((ref) {
  return UserRemoteDataSourceImpl(ref.watch(apiClientProvider));
});

// Local data source provider
final userLocalDataSourceProvider = Provider<UserLocalDataSource>((ref) {
  return UserLocalDataSourceImpl(ref.watch(localStorageProvider));
});

// Repository provider
final userRepositoryProvider = Provider<UserRepository>((ref) {
  return UserRepositoryImpl(
    remoteDataSource: ref.watch(userRemoteDataSourceProvider),
    localDataSource: ref.watch(userLocalDataSourceProvider),
  );
});
```

## Repository Checklist

- [ ] Define interface in domain layer (no external dependencies)
- [ ] Implementation in data layer
- [ ] Use Result pattern for error handling
- [ ] Implement caching strategy (cache-first, network-first, etc.)
- [ ] Handle network errors gracefully
- [ ] Provide real-time updates via streams
- [ ] Convert between models and entities
- [ ] Document all public methods
- [ ] Make dependencies injectable

## File Organization

```
lib/
├── features/
│   └── users/
│       ├── data/
│       │   ├── datasources/
│       │   │   ├── user_local_datasource.dart
│       │   │   └── user_remote_datasource.dart
│       │   ├── models/
│       │   │   └── user_model.dart
│       │   └── repositories/
│       │       └── user_repository_impl.dart
│       └── domain/
│           ├── entities/
│           │   └── user.dart
│           └── repositories/
│               └── user_repository.dart
```
