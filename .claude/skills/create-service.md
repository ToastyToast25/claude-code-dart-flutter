---
description: "Creates service classes for business logic, API clients, and external integrations"
globs: ["lib/**/services/*.dart", "lib/core/services/**/*.dart"]
alwaysApply: false
---

# Create Service Skill

Create a service class for business logic or external integrations.

## Trigger Keywords
- create service
- new service
- add service
- service class

---

## Service Template

```dart
/// Service for handling [description].
///
/// This service provides [functionality description] and manages
/// [what it manages/coordinates].
class [Name]Service {
  const [Name]Service(this._dependency);

  final [Dependency] _dependency;

  /// [Method description].
  ///
  /// Returns [what it returns] or throws [what exceptions].
  Future<[ReturnType]> [methodName]([params]) async {
    try {
      // Implementation
      return result;
    } catch (e) {
      throw [ServiceException]('Failed to [action]: $e');
    }
  }
}
```

---

## Common Service Patterns

### API Service

```dart
import 'package:dio/dio.dart';

/// Service for making HTTP requests to the backend API.
class ApiService {
  ApiService({Dio? dio}) : _dio = dio ?? Dio();

  final Dio _dio;

  /// Base configuration
  void configure({
    required String baseUrl,
    String? authToken,
    Duration? timeout,
  }) {
    _dio.options = BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: timeout ?? const Duration(seconds: 10),
      receiveTimeout: timeout ?? const Duration(seconds: 10),
      headers: {
        'Content-Type': 'application/json',
        if (authToken != null) 'Authorization': 'Bearer $authToken',
      },
    );
  }

  /// GET request
  Future<T> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    T Function(dynamic)? fromJson,
  }) async {
    try {
      final response = await _dio.get<dynamic>(
        path,
        queryParameters: queryParameters,
      );
      return fromJson != null ? fromJson(response.data) : response.data as T;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// POST request
  Future<T> post<T>(
    String path, {
    dynamic data,
    T Function(dynamic)? fromJson,
  }) async {
    try {
      final response = await _dio.post<dynamic>(path, data: data);
      return fromJson != null ? fromJson(response.data) : response.data as T;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// PUT request
  Future<T> put<T>(
    String path, {
    dynamic data,
    T Function(dynamic)? fromJson,
  }) async {
    try {
      final response = await _dio.put<dynamic>(path, data: data);
      return fromJson != null ? fromJson(response.data) : response.data as T;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// DELETE request
  Future<void> delete(String path) async {
    try {
      await _dio.delete<dynamic>(path);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  ApiException _handleError(DioException error) {
    return switch (error.type) {
      DioExceptionType.connectionTimeout ||
      DioExceptionType.sendTimeout ||
      DioExceptionType.receiveTimeout =>
        ApiException('Connection timeout', code: 'TIMEOUT'),
      DioExceptionType.badResponse => ApiException(
          error.response?.data?['message'] ?? 'Server error',
          code: error.response?.statusCode?.toString() ?? 'UNKNOWN',
        ),
      DioExceptionType.cancel => ApiException('Request cancelled', code: 'CANCELLED'),
      _ => ApiException('Network error: ${error.message}', code: 'NETWORK_ERROR'),
    };
  }
}

class ApiException implements Exception {
  const ApiException(this.message, {this.code});
  final String message;
  final String? code;

  @override
  String toString() => 'ApiException: $message (code: $code)';
}
```

### Authentication Service

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Service for managing user authentication state and tokens.
class AuthService {
  AuthService({
    required ApiService apiService,
    FlutterSecureStorage? storage,
  })  : _api = apiService,
        _storage = storage ?? const FlutterSecureStorage();

  final ApiService _api;
  final FlutterSecureStorage _storage;

  static const _accessTokenKey = 'access_token';
  static const _refreshTokenKey = 'refresh_token';

  String? _accessToken;

  /// Current access token (cached in memory)
  String? get accessToken => _accessToken;

  /// Whether user is authenticated
  bool get isAuthenticated => _accessToken != null;

  /// Initialize auth state from storage
  Future<void> initialize() async {
    _accessToken = await _storage.read(key: _accessTokenKey);
    if (_accessToken != null) {
      _api.configure(
        baseUrl: _api._dio.options.baseUrl,
        authToken: _accessToken,
      );
    }
  }

  /// Login with credentials
  Future<User> login({
    required String email,
    required String password,
  }) async {
    final response = await _api.post<Map<String, dynamic>>(
      '/auth/login',
      data: {'email': email, 'password': password},
    );

    final tokens = AuthTokens.fromJson(response);
    await _saveTokens(tokens);

    return User.fromJson(response['user'] as Map<String, dynamic>);
  }

  /// Logout and clear tokens
  Future<void> logout() async {
    try {
      await _api.post('/auth/logout');
    } catch (_) {
      // Ignore logout errors
    } finally {
      await _clearTokens();
    }
  }

  /// Refresh access token
  Future<void> refreshToken() async {
    final refreshToken = await _storage.read(key: _refreshTokenKey);
    if (refreshToken == null) {
      throw AuthException('No refresh token available');
    }

    final response = await _api.post<Map<String, dynamic>>(
      '/auth/refresh',
      data: {'refresh_token': refreshToken},
    );

    final tokens = AuthTokens.fromJson(response);
    await _saveTokens(tokens);
  }

  Future<void> _saveTokens(AuthTokens tokens) async {
    _accessToken = tokens.accessToken;
    await _storage.write(key: _accessTokenKey, value: tokens.accessToken);
    await _storage.write(key: _refreshTokenKey, value: tokens.refreshToken);
    _api.configure(
      baseUrl: _api._dio.options.baseUrl,
      authToken: tokens.accessToken,
    );
  }

  Future<void> _clearTokens() async {
    _accessToken = null;
    await _storage.delete(key: _accessTokenKey);
    await _storage.delete(key: _refreshTokenKey);
  }
}

class AuthException implements Exception {
  const AuthException(this.message);
  final String message;
}
```

### Analytics Service

```dart
/// Service for tracking analytics events.
abstract class AnalyticsService {
  /// Log a custom event
  Future<void> logEvent(String name, [Map<String, dynamic>? parameters]);

  /// Set user properties
  Future<void> setUserProperties(Map<String, dynamic> properties);

  /// Set user ID
  Future<void> setUserId(String? userId);

  /// Log screen view
  Future<void> logScreenView(String screenName, {String? screenClass});
}

/// Firebase Analytics implementation
class FirebaseAnalyticsService implements AnalyticsService {
  FirebaseAnalyticsService(this._analytics);

  final FirebaseAnalytics _analytics;

  @override
  Future<void> logEvent(String name, [Map<String, dynamic>? parameters]) async {
    await _analytics.logEvent(
      name: name,
      parameters: parameters?.map((k, v) => MapEntry(k, v.toString())),
    );
  }

  @override
  Future<void> setUserProperties(Map<String, dynamic> properties) async {
    for (final entry in properties.entries) {
      await _analytics.setUserProperty(
        name: entry.key,
        value: entry.value?.toString(),
      );
    }
  }

  @override
  Future<void> setUserId(String? userId) async {
    await _analytics.setUserId(id: userId);
  }

  @override
  Future<void> logScreenView(String screenName, {String? screenClass}) async {
    await _analytics.logScreenView(
      screenName: screenName,
      screenClass: screenClass,
    );
  }
}
```

### Cache Service

```dart
/// Service for caching data with expiration.
class CacheService {
  CacheService({SharedPreferences? prefs}) : _prefs = prefs;

  SharedPreferences? _prefs;

  Future<void> initialize() async {
    _prefs ??= await SharedPreferences.getInstance();
  }

  /// Get cached value
  T? get<T>(String key) {
    final data = _prefs?.getString(key);
    if (data == null) return null;

    final cached = CachedData.fromJson(jsonDecode(data) as Map<String, dynamic>);
    if (cached.isExpired) {
      _prefs?.remove(key);
      return null;
    }

    return cached.value as T;
  }

  /// Set cached value with optional TTL
  Future<void> set<T>(
    String key,
    T value, {
    Duration ttl = const Duration(hours: 1),
  }) async {
    final cached = CachedData(
      value: value,
      expiresAt: DateTime.now().add(ttl),
    );
    await _prefs?.setString(key, jsonEncode(cached.toJson()));
  }

  /// Remove cached value
  Future<void> remove(String key) async {
    await _prefs?.remove(key);
  }

  /// Clear all cached data
  Future<void> clear() async {
    await _prefs?.clear();
  }
}

class CachedData {
  CachedData({required this.value, required this.expiresAt});

  factory CachedData.fromJson(Map<String, dynamic> json) => CachedData(
        value: json['value'],
        expiresAt: DateTime.parse(json['expiresAt'] as String),
      );

  final dynamic value;
  final DateTime expiresAt;

  bool get isExpired => DateTime.now().isAfter(expiresAt);

  Map<String, dynamic> toJson() => {
        'value': value,
        'expiresAt': expiresAt.toIso8601String(),
      };
}
```

### Notification Service

```dart
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

/// Service for managing local and push notifications.
class NotificationService {
  NotificationService();

  final _localNotifications = FlutterLocalNotificationsPlugin();

  Future<void> initialize() async {
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    const iosSettings = DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );

    await _localNotifications.initialize(
      const InitializationSettings(
        android: androidSettings,
        iOS: iosSettings,
      ),
      onDidReceiveNotificationResponse: _onNotificationTapped,
    );
  }

  Future<void> showNotification({
    required String title,
    required String body,
    String? payload,
  }) async {
    const androidDetails = AndroidNotificationDetails(
      'default_channel',
      'Default',
      channelDescription: 'Default notification channel',
      importance: Importance.high,
      priority: Priority.high,
    );

    const iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    );

    await _localNotifications.show(
      DateTime.now().millisecondsSinceEpoch ~/ 1000,
      title,
      body,
      const NotificationDetails(
        android: androidDetails,
        iOS: iosDetails,
      ),
      payload: payload,
    );
  }

  void _onNotificationTapped(NotificationResponse response) {
    // Handle notification tap
    final payload = response.payload;
    if (payload != null) {
      // Navigate to appropriate screen
    }
  }
}
```

---

## File Location

```
lib/
├── core/
│   └── services/
│       ├── api_service.dart
│       ├── auth_service.dart
│       ├── cache_service.dart
│       └── notification_service.dart
│
└── features/
    └── [feature_name]/
        └── services/
            └── [feature]_service.dart
```

---

## Provider Integration

```dart
// Core services (single instance)
final apiServiceProvider = Provider<ApiService>((ref) {
  return ApiService()..configure(baseUrl: Environment.apiUrl);
});

final authServiceProvider = Provider<AuthService>((ref) {
  return AuthService(apiService: ref.watch(apiServiceProvider));
});

// Feature services
final userServiceProvider = Provider<UserService>((ref) {
  return UserService(
    api: ref.watch(apiServiceProvider),
    cache: ref.watch(cacheServiceProvider),
  );
});
```

---

## Testing

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockDependency extends Mock implements Dependency {}

void main() {
  late [Name]Service service;
  late MockDependency mockDependency;

  setUp(() {
    mockDependency = MockDependency();
    service = [Name]Service(mockDependency);
  });

  group('[Name]Service', () {
    test('[methodName] returns expected result', () async {
      // Arrange
      when(() => mockDependency.someMethod())
          .thenAnswer((_) async => expectedResult);

      // Act
      final result = await service.methodName();

      // Assert
      expect(result, expectedResult);
      verify(() => mockDependency.someMethod()).called(1);
    });

    test('[methodName] throws on error', () async {
      // Arrange
      when(() => mockDependency.someMethod())
          .thenThrow(Exception('Error'));

      // Act & Assert
      expect(
        () => service.methodName(),
        throwsA(isA<[ServiceException]>()),
      );
    });
  });
}
```

---

## Checklist

- [ ] Service has clear single responsibility
- [ ] Dependencies injected via constructor
- [ ] Methods are well-documented
- [ ] Error handling is consistent
- [ ] Has corresponding provider
- [ ] Unit tests cover main functionality
- [ ] No direct UI dependencies
