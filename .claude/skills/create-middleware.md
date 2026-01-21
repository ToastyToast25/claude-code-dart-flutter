---
description: "Generates backend middleware for Shelf/Dart Frog (auth, CORS, rate limiting)"
globs: ["backend/**/middleware/*.dart", "lib/middleware/**/*.dart"]
alwaysApply: false
---

# Create Middleware Skill

Generate backend middleware for Shelf/Dart Frog servers.

## Trigger
- "create middleware"
- "new middleware"
- "add middleware"
- "backend middleware"

## Parameters
- **name**: Middleware name (e.g., "auth", "logging", "rateLimit")
- **type**: auth, logging, cors, rateLimit, validation, custom

## Generated Code

### Authentication Middleware

```dart
// backend/lib/middleware/auth_middleware.dart
import 'dart:convert';
import 'package:shelf/shelf.dart';
import '../services/jwt_service.dart';
import '../models/user.dart';

/// Middleware that validates JWT tokens and adds user to request context
Middleware authMiddleware({
  List<String> excludePaths = const [],
  List<String> excludePrefixes = const ['/api/v1/auth'],
}) {
  return (Handler innerHandler) {
    return (Request request) async {
      // Check if path should be excluded
      final path = request.requestedUri.path;
      if (excludePaths.contains(path) ||
          excludePrefixes.any((prefix) => path.startsWith(prefix))) {
        return innerHandler(request);
      }

      // Get authorization header
      final authHeader = request.headers['authorization'];
      if (authHeader == null || !authHeader.startsWith('Bearer ')) {
        return Response(
          401,
          body: jsonEncode({'error': 'Missing or invalid authorization header'}),
          headers: {'Content-Type': 'application/json'},
        );
      }

      // Extract and validate token
      final token = authHeader.substring(7);
      try {
        final payload = JwtService.verify(token);
        final user = User.fromTokenPayload(payload);

        // Add user to request context
        final updatedRequest = request.change(
          context: {
            ...request.context,
            'user': user,
          },
        );

        return innerHandler(updatedRequest);
      } on JwtException catch (e) {
        return Response(
          401,
          body: jsonEncode({'error': e.message}),
          headers: {'Content-Type': 'application/json'},
        );
      }
    };
  };
}

/// Extract user from request context
User? getUser(Request request) {
  return request.context['user'] as User?;
}

/// Require user to be present (use after authMiddleware)
User requireUser(Request request) {
  final user = getUser(request);
  if (user == null) {
    throw StateError('User not found in request context');
  }
  return user;
}
```

### Role-Based Authorization Middleware

```dart
// backend/lib/middleware/role_middleware.dart
import 'dart:convert';
import 'package:shelf/shelf.dart';
import 'auth_middleware.dart';

/// Middleware that checks if user has required role(s)
Middleware requireRole(List<String> allowedRoles) {
  return (Handler innerHandler) {
    return (Request request) async {
      final user = getUser(request);

      if (user == null) {
        return Response(
          401,
          body: jsonEncode({'error': 'Authentication required'}),
          headers: {'Content-Type': 'application/json'},
        );
      }

      if (!allowedRoles.any((role) => user.roles.contains(role))) {
        return Response(
          403,
          body: jsonEncode({
            'error': 'Insufficient permissions',
            'required': allowedRoles,
            'current': user.roles,
          }),
          headers: {'Content-Type': 'application/json'},
        );
      }

      return innerHandler(request);
    };
  };
}

/// Require admin role
Middleware requireAdmin() => requireRole(['admin', 'superadmin']);

/// Require any of the specified roles
Middleware requireAnyRole(List<String> roles) => requireRole(roles);
```

### Logging Middleware

```dart
// backend/lib/middleware/logging_middleware.dart
import 'dart:async';
import 'package:shelf/shelf.dart';

/// Middleware that logs all requests and responses
Middleware loggingMiddleware({
  bool logBody = false,
  bool logHeaders = false,
  List<String> sensitiveHeaders = const ['authorization', 'cookie'],
}) {
  return (Handler innerHandler) {
    return (Request request) async {
      final stopwatch = Stopwatch()..start();
      final requestId = _generateRequestId();
      final timestamp = DateTime.now().toIso8601String();

      // Log request
      final requestLog = StringBuffer()
        ..writeln('[$timestamp] [$requestId] --> ${request.method} ${request.requestedUri}');

      if (logHeaders) {
        final headers = Map<String, String>.from(request.headers);
        for (final header in sensitiveHeaders) {
          if (headers.containsKey(header)) {
            headers[header] = '***REDACTED***';
          }
        }
        requestLog.writeln('  Headers: $headers');
      }

      print(requestLog);

      // Process request
      Response response;
      String? errorMessage;
      try {
        response = await innerHandler(request);
      } catch (e, stack) {
        errorMessage = e.toString();
        print('[$timestamp] [$requestId] !!! ERROR: $e');
        print(stack);
        rethrow;
      } finally {
        stopwatch.stop();
      }

      // Log response
      final statusEmoji = response.statusCode < 400 ? '✓' : '✗';
      final responseLog = StringBuffer()
        ..writeln('[$timestamp] [$requestId] <-- $statusEmoji ${response.statusCode} '
            '${stopwatch.elapsedMilliseconds}ms');

      if (logHeaders) {
        responseLog.writeln('  Headers: ${response.headers}');
      }

      print(responseLog);

      // Add request ID to response headers
      return response.change(
        headers: {
          ...response.headers,
          'X-Request-Id': requestId,
        },
      );
    };
  };
}

String _generateRequestId() {
  return DateTime.now().microsecondsSinceEpoch.toRadixString(36);
}
```

### CORS Middleware

```dart
// backend/lib/middleware/cors_middleware.dart
import 'package:shelf/shelf.dart';

/// Middleware that handles CORS preflight requests and headers
Middleware corsMiddleware({
  List<String> allowedOrigins = const ['*'],
  List<String> allowedMethods = const ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  List<String> allowedHeaders = const ['Content-Type', 'Authorization', 'X-Requested-With'],
  List<String> exposedHeaders = const ['X-Request-Id'],
  bool allowCredentials = false,
  int maxAge = 86400,
}) {
  return (Handler innerHandler) {
    return (Request request) async {
      final origin = request.headers['origin'];

      // Check if origin is allowed
      final isAllowed = allowedOrigins.contains('*') ||
          (origin != null && allowedOrigins.contains(origin));

      final corsHeaders = <String, String>{
        'Access-Control-Allow-Origin': isAllowed
            ? (origin ?? '*')
            : allowedOrigins.first,
        'Access-Control-Allow-Methods': allowedMethods.join(', '),
        'Access-Control-Allow-Headers': allowedHeaders.join(', '),
        'Access-Control-Expose-Headers': exposedHeaders.join(', '),
        'Access-Control-Max-Age': maxAge.toString(),
      };

      if (allowCredentials) {
        corsHeaders['Access-Control-Allow-Credentials'] = 'true';
      }

      // Handle preflight OPTIONS request
      if (request.method == 'OPTIONS') {
        return Response.ok(
          null,
          headers: corsHeaders,
        );
      }

      // Process request and add CORS headers to response
      final response = await innerHandler(request);
      return response.change(
        headers: {
          ...response.headers,
          ...corsHeaders,
        },
      );
    };
  };
}
```

### Rate Limiting Middleware

```dart
// backend/lib/middleware/rate_limit_middleware.dart
import 'dart:async';
import 'dart:convert';
import 'package:shelf/shelf.dart';

/// In-memory rate limiter (use Redis for production)
class RateLimiter {
  final Map<String, _RateLimitEntry> _entries = {};
  final int maxRequests;
  final Duration window;

  RateLimiter({
    this.maxRequests = 100,
    this.window = const Duration(minutes: 1),
  });

  bool isAllowed(String key) {
    final now = DateTime.now();
    final entry = _entries[key];

    if (entry == null || now.isAfter(entry.windowEnd)) {
      _entries[key] = _RateLimitEntry(
        count: 1,
        windowEnd: now.add(window),
      );
      return true;
    }

    if (entry.count >= maxRequests) {
      return false;
    }

    entry.count++;
    return true;
  }

  int remaining(String key) {
    final entry = _entries[key];
    if (entry == null) return maxRequests;
    return (maxRequests - entry.count).clamp(0, maxRequests);
  }

  Duration? retryAfter(String key) {
    final entry = _entries[key];
    if (entry == null) return null;
    final now = DateTime.now();
    if (now.isAfter(entry.windowEnd)) return null;
    return entry.windowEnd.difference(now);
  }

  void cleanup() {
    final now = DateTime.now();
    _entries.removeWhere((key, entry) => now.isAfter(entry.windowEnd));
  }
}

class _RateLimitEntry {
  int count;
  final DateTime windowEnd;

  _RateLimitEntry({required this.count, required this.windowEnd});
}

/// Rate limiting middleware
Middleware rateLimitMiddleware({
  int maxRequests = 100,
  Duration window = const Duration(minutes: 1),
  String Function(Request)? keyExtractor,
}) {
  final limiter = RateLimiter(maxRequests: maxRequests, window: window);

  // Periodic cleanup
  Timer.periodic(const Duration(minutes: 5), (_) => limiter.cleanup());

  return (Handler innerHandler) {
    return (Request request) async {
      // Extract key (default: IP address)
      final key = keyExtractor?.call(request) ??
          request.headers['x-forwarded-for']?.split(',').first ??
          request.headers['x-real-ip'] ??
          'unknown';

      if (!limiter.isAllowed(key)) {
        final retryAfter = limiter.retryAfter(key);
        return Response(
          429,
          body: jsonEncode({
            'error': 'Too many requests',
            'retryAfter': retryAfter?.inSeconds,
          }),
          headers: {
            'Content-Type': 'application/json',
            'Retry-After': (retryAfter?.inSeconds ?? 60).toString(),
            'X-RateLimit-Limit': maxRequests.toString(),
            'X-RateLimit-Remaining': '0',
          },
        );
      }

      final response = await innerHandler(request);

      return response.change(
        headers: {
          ...response.headers,
          'X-RateLimit-Limit': maxRequests.toString(),
          'X-RateLimit-Remaining': limiter.remaining(key).toString(),
        },
      );
    };
  };
}
```

### Request Validation Middleware

```dart
// backend/lib/middleware/validation_middleware.dart
import 'dart:convert';
import 'package:shelf/shelf.dart';

typedef Validator = List<String> Function(Map<String, dynamic> body);

/// Middleware that validates request body against a schema
Middleware validateBody(Validator validator) {
  return (Handler innerHandler) {
    return (Request request) async {
      // Only validate methods with body
      if (!['POST', 'PUT', 'PATCH'].contains(request.method)) {
        return innerHandler(request);
      }

      // Check content type
      final contentType = request.headers['content-type'];
      if (contentType == null || !contentType.contains('application/json')) {
        return Response(
          415,
          body: jsonEncode({'error': 'Content-Type must be application/json'}),
          headers: {'Content-Type': 'application/json'},
        );
      }

      // Parse body
      Map<String, dynamic> body;
      try {
        final bodyString = await request.readAsString();
        if (bodyString.isEmpty) {
          body = {};
        } else {
          body = jsonDecode(bodyString) as Map<String, dynamic>;
        }
      } catch (e) {
        return Response(
          400,
          body: jsonEncode({'error': 'Invalid JSON body'}),
          headers: {'Content-Type': 'application/json'},
        );
      }

      // Validate
      final errors = validator(body);
      if (errors.isNotEmpty) {
        return Response(
          400,
          body: jsonEncode({
            'error': 'Validation failed',
            'details': errors,
          }),
          headers: {'Content-Type': 'application/json'},
        );
      }

      // Add parsed body to context
      final updatedRequest = request.change(
        context: {
          ...request.context,
          'body': body,
        },
      );

      return innerHandler(updatedRequest);
    };
  };
}

/// Get parsed body from request context
Map<String, dynamic> getBody(Request request) {
  return request.context['body'] as Map<String, dynamic>? ?? {};
}

// Validator helpers
List<String> createUserValidator(Map<String, dynamic> body) {
  final errors = <String>[];

  if (body['email'] == null || (body['email'] as String).isEmpty) {
    errors.add('Email is required');
  } else if (!_isValidEmail(body['email'] as String)) {
    errors.add('Invalid email format');
  }

  if (body['password'] == null || (body['password'] as String).length < 8) {
    errors.add('Password must be at least 8 characters');
  }

  if (body['name'] == null || (body['name'] as String).isEmpty) {
    errors.add('Name is required');
  }

  return errors;
}

bool _isValidEmail(String email) {
  return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(email);
}
```

### Error Handling Middleware

```dart
// backend/lib/middleware/error_middleware.dart
import 'dart:convert';
import 'package:shelf/shelf.dart';

/// Middleware that catches and formats errors
Middleware errorMiddleware({
  bool showStackTrace = false,
}) {
  return (Handler innerHandler) {
    return (Request request) async {
      try {
        return await innerHandler(request);
      } on HttpException catch (e) {
        return Response(
          e.statusCode,
          body: jsonEncode({
            'error': e.message,
            if (e.code != null) 'code': e.code,
          }),
          headers: {'Content-Type': 'application/json'},
        );
      } on ValidationException catch (e) {
        return Response(
          400,
          body: jsonEncode({
            'error': 'Validation failed',
            'details': e.errors,
          }),
          headers: {'Content-Type': 'application/json'},
        );
      } catch (e, stack) {
        print('Unhandled error: $e');
        print(stack);

        return Response(
          500,
          body: jsonEncode({
            'error': 'Internal server error',
            if (showStackTrace) 'details': e.toString(),
            if (showStackTrace) 'stack': stack.toString(),
          }),
          headers: {'Content-Type': 'application/json'},
        );
      }
    };
  };
}

class HttpException implements Exception {
  final int statusCode;
  final String message;
  final String? code;

  const HttpException(this.statusCode, this.message, {this.code});

  factory HttpException.badRequest(String message, {String? code}) =>
      HttpException(400, message, code: code);

  factory HttpException.unauthorized(String message, {String? code}) =>
      HttpException(401, message, code: code);

  factory HttpException.forbidden(String message, {String? code}) =>
      HttpException(403, message, code: code);

  factory HttpException.notFound(String message, {String? code}) =>
      HttpException(404, message, code: code);

  factory HttpException.conflict(String message, {String? code}) =>
      HttpException(409, message, code: code);
}

class ValidationException implements Exception {
  final List<String> errors;

  const ValidationException(this.errors);
}
```

### Composing Middleware

```dart
// backend/lib/middleware/middleware.dart
import 'package:shelf/shelf.dart';
import 'auth_middleware.dart';
import 'cors_middleware.dart';
import 'error_middleware.dart';
import 'logging_middleware.dart';
import 'rate_limit_middleware.dart';

/// Create the middleware pipeline
Pipeline createMiddlewarePipeline({
  required bool isDevelopment,
}) {
  return const Pipeline()
      .addMiddleware(errorMiddleware(showStackTrace: isDevelopment))
      .addMiddleware(loggingMiddleware(
        logBody: isDevelopment,
        logHeaders: isDevelopment,
      ))
      .addMiddleware(corsMiddleware(
        allowedOrigins: isDevelopment
            ? ['*']
            : ['https://example.com', 'https://admin.example.com'],
        allowCredentials: true,
      ))
      .addMiddleware(rateLimitMiddleware(
        maxRequests: isDevelopment ? 1000 : 100,
      ))
      .addMiddleware(authMiddleware(
        excludePrefixes: ['/api/v1/auth', '/api/v1/public', '/health'],
      ));
}
```

## Usage

```
User: create middleware auth
User: create middleware rate limit 100 requests per minute
User: create middleware cors for admin.example.com
```
