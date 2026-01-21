---
description: "Scaffolds backend API endpoints using Shelf or Dart Frog frameworks"
globs: ["backend/**/*.dart", "lib/api/**/*.dart", "routes/**/*.dart"]
alwaysApply: false
---

# Create API Endpoint Skill

Scaffold backend API endpoints using shelf or dart_frog.

## Trigger Keywords
- create api endpoint
- create endpoint
- new api route
- add endpoint
- backend route

---

## Shelf Router Endpoint

### Basic Handler

```dart
import 'dart:convert';
import 'package:shelf/shelf.dart';
import 'package:shelf_router/shelf_router.dart';

part '[handler_name]_handler.g.dart';

class [HandlerName]Handler {
  [HandlerName]Handler(this._repository);

  final [Repository]Repository _repository;

  Router get router => _$[HandlerName]HandlerRouter(this);

  @Route.get('/')
  Future<Response> getAll(Request request) async {
    try {
      final items = await _repository.getAll();
      return Response.ok(
        jsonEncode(items.map((e) => e.toJson()).toList()),
        headers: {'Content-Type': 'application/json'},
      );
    } catch (e) {
      return Response.internalServerError(
        body: jsonEncode({'error': e.toString()}),
      );
    }
  }

  @Route.get('/<id>')
  Future<Response> getById(Request request, String id) async {
    try {
      final item = await _repository.getById(id);
      if (item == null) {
        return Response.notFound(
          jsonEncode({'error': 'Not found'}),
        );
      }
      return Response.ok(
        jsonEncode(item.toJson()),
        headers: {'Content-Type': 'application/json'},
      );
    } catch (e) {
      return Response.internalServerError(
        body: jsonEncode({'error': e.toString()}),
      );
    }
  }

  @Route.post('/')
  Future<Response> create(Request request) async {
    try {
      final body = await request.readAsString();
      final data = jsonDecode(body) as Map<String, dynamic>;

      final item = await _repository.create(data);
      return Response(
        201,
        body: jsonEncode(item.toJson()),
        headers: {'Content-Type': 'application/json'},
      );
    } catch (e) {
      return Response.internalServerError(
        body: jsonEncode({'error': e.toString()}),
      );
    }
  }

  @Route.put('/<id>')
  Future<Response> update(Request request, String id) async {
    try {
      final body = await request.readAsString();
      final data = jsonDecode(body) as Map<String, dynamic>;

      final item = await _repository.update(id, data);
      if (item == null) {
        return Response.notFound(
          jsonEncode({'error': 'Not found'}),
        );
      }
      return Response.ok(
        jsonEncode(item.toJson()),
        headers: {'Content-Type': 'application/json'},
      );
    } catch (e) {
      return Response.internalServerError(
        body: jsonEncode({'error': e.toString()}),
      );
    }
  }

  @Route.delete('/<id>')
  Future<Response> delete(Request request, String id) async {
    try {
      final deleted = await _repository.delete(id);
      if (!deleted) {
        return Response.notFound(
          jsonEncode({'error': 'Not found'}),
        );
      }
      return Response(204);
    } catch (e) {
      return Response.internalServerError(
        body: jsonEncode({'error': e.toString()}),
      );
    }
  }
}
```

### Mounting Router

```dart
import 'package:shelf/shelf.dart';
import 'package:shelf_router/shelf_router.dart';

Router createRouter() {
  final router = Router();

  // Mount handlers
  router.mount('/api/v1/users', UserHandler(userRepository).router);
  router.mount('/api/v1/products', ProductHandler(productRepository).router);
  router.mount('/api/v1/orders', OrderHandler(orderRepository).router);

  return router;
}
```

---

## Dart Frog Endpoint

### Route Handler

```dart
// routes/api/v1/[resource]/index.dart
import 'dart:io';
import 'package:dart_frog/dart_frog.dart';

Future<Response> onRequest(RequestContext context) async {
  switch (context.request.method) {
    case HttpMethod.get:
      return _get(context);
    case HttpMethod.post:
      return _post(context);
    default:
      return Response(statusCode: HttpStatus.methodNotAllowed);
  }
}

Future<Response> _get(RequestContext context) async {
  final repository = context.read<[Repository]Repository>();

  try {
    final items = await repository.getAll();
    return Response.json(
      body: items.map((e) => e.toJson()).toList(),
    );
  } catch (e) {
    return Response.json(
      statusCode: HttpStatus.internalServerError,
      body: {'error': e.toString()},
    );
  }
}

Future<Response> _post(RequestContext context) async {
  final repository = context.read<[Repository]Repository>();

  try {
    final body = await context.request.json() as Map<String, dynamic>;
    final item = await repository.create(body);

    return Response.json(
      statusCode: HttpStatus.created,
      body: item.toJson(),
    );
  } catch (e) {
    return Response.json(
      statusCode: HttpStatus.internalServerError,
      body: {'error': e.toString()},
    );
  }
}
```

### Dynamic Route Handler

```dart
// routes/api/v1/[resource]/[id].dart
import 'dart:io';
import 'package:dart_frog/dart_frog.dart';

Future<Response> onRequest(RequestContext context, String id) async {
  switch (context.request.method) {
    case HttpMethod.get:
      return _get(context, id);
    case HttpMethod.put:
      return _put(context, id);
    case HttpMethod.delete:
      return _delete(context, id);
    default:
      return Response(statusCode: HttpStatus.methodNotAllowed);
  }
}

Future<Response> _get(RequestContext context, String id) async {
  final repository = context.read<[Repository]Repository>();

  try {
    final item = await repository.getById(id);
    if (item == null) {
      return Response.json(
        statusCode: HttpStatus.notFound,
        body: {'error': 'Not found'},
      );
    }
    return Response.json(body: item.toJson());
  } catch (e) {
    return Response.json(
      statusCode: HttpStatus.internalServerError,
      body: {'error': e.toString()},
    );
  }
}

Future<Response> _put(RequestContext context, String id) async {
  final repository = context.read<[Repository]Repository>();

  try {
    final body = await context.request.json() as Map<String, dynamic>;
    final item = await repository.update(id, body);

    if (item == null) {
      return Response.json(
        statusCode: HttpStatus.notFound,
        body: {'error': 'Not found'},
      );
    }
    return Response.json(body: item.toJson());
  } catch (e) {
    return Response.json(
      statusCode: HttpStatus.internalServerError,
      body: {'error': e.toString()},
    );
  }
}

Future<Response> _delete(RequestContext context, String id) async {
  final repository = context.read<[Repository]Repository>();

  try {
    final deleted = await repository.delete(id);
    if (!deleted) {
      return Response.json(
        statusCode: HttpStatus.notFound,
        body: {'error': 'Not found'},
      );
    }
    return Response(statusCode: HttpStatus.noContent);
  } catch (e) {
    return Response.json(
      statusCode: HttpStatus.internalServerError,
      body: {'error': e.toString()},
    );
  }
}
```

### Middleware

```dart
// routes/api/v1/_middleware.dart
import 'package:dart_frog/dart_frog.dart';

Handler middleware(Handler handler) {
  return handler
      .use(requestLogger())
      .use(_authMiddleware())
      .use(_corsMiddleware());
}

Middleware _authMiddleware() {
  return (handler) {
    return (context) async {
      final authHeader = context.request.headers['Authorization'];

      if (authHeader == null || !authHeader.startsWith('Bearer ')) {
        return Response.json(
          statusCode: 401,
          body: {'error': 'Unauthorized'},
        );
      }

      final token = authHeader.substring(7);
      // Validate token...

      return handler(context);
    };
  };
}

Middleware _corsMiddleware() {
  return (handler) {
    return (context) async {
      final response = await handler(context);
      return response.copyWith(
        headers: {
          ...response.headers,
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      );
    };
  };
}
```

---

## Response Helpers

```dart
import 'dart:convert';
import 'package:shelf/shelf.dart';

extension ResponseHelpers on Response {
  static Response json(
    Object? body, {
    int statusCode = 200,
    Map<String, String>? headers,
  }) {
    return Response(
      statusCode,
      body: jsonEncode(body),
      headers: {
        'Content-Type': 'application/json',
        ...?headers,
      },
    );
  }

  static Response created(Object? body) => json(body, statusCode: 201);

  static Response noContent() => Response(204);

  static Response badRequest(String message) => json(
    {'error': message},
    statusCode: 400,
  );

  static Response unauthorized([String message = 'Unauthorized']) => json(
    {'error': message},
    statusCode: 401,
  );

  static Response forbidden([String message = 'Forbidden']) => json(
    {'error': message},
    statusCode: 403,
  );

  static Response notFound([String message = 'Not found']) => json(
    {'error': message},
    statusCode: 404,
  );

  static Response serverError(Object error) => json(
    {'error': error.toString()},
    statusCode: 500,
  );
}
```

---

## File Structure

### Shelf
```
lib/
├── handlers/
│   ├── user_handler.dart
│   ├── product_handler.dart
│   └── order_handler.dart
├── middleware/
│   ├── auth_middleware.dart
│   └── cors_middleware.dart
└── server.dart
```

### Dart Frog
```
routes/
├── api/
│   └── v1/
│       ├── _middleware.dart
│       ├── users/
│       │   ├── index.dart
│       │   └── [id].dart
│       ├── products/
│       │   ├── index.dart
│       │   └── [id].dart
│       └── orders/
│           ├── index.dart
│           └── [id].dart
```

---

## Security Requirements

### Input Validation

```dart
// Always validate and sanitize input
Future<Response> _post(RequestContext context) async {
  final body = await context.request.json() as Map<String, dynamic>;

  // 1. Validate required fields
  if (!body.containsKey('email') || !body.containsKey('name')) {
    return Response.json(
      statusCode: 400,
      body: {'error': 'Missing required fields'},
    );
  }

  // 2. Sanitize string inputs
  final email = InputSanitizer.sanitizeEmail(body['email']?.toString() ?? '');
  if (email == null) {
    return Response.json(
      statusCode: 400,
      body: {'error': 'Invalid email format'},
    );
  }

  // 3. Limit string lengths
  final name = InputSanitizer.sanitizeString(
    body['name']?.toString() ?? '',
    maxLength: 100,
  );

  // 4. Validate numeric ranges
  final age = InputSanitizer.sanitizeInt(body['age'], min: 0, max: 150);

  // Continue with validated data...
}
```

### Prevent Mass Assignment

```dart
// ❌ Dangerous - allows any field to be set
final user = User.fromJson(body);
await repository.update(user);

// ✅ Safe - explicitly pick allowed fields
final updateData = UserUpdateDto(
  name: body['name'] as String?,
  email: body['email'] as String?,
  // Explicitly exclude: role, isAdmin, passwordHash
);
await repository.update(id, updateData);
```

### Secure Error Handling

```dart
// ❌ Leaks internal details
catch (e, stack) {
  return Response.json(
    statusCode: 500,
    body: {'error': e.toString(), 'stack': stack.toString()},
  );
}

// ✅ Generic error to client, detailed log server-side
catch (e, stack) {
  logger.error('Endpoint error', error: e, stackTrace: stack);
  return Response.json(
    statusCode: 500,
    body: {'error': 'An internal error occurred'},
  );
}
```

### ID Parameter Validation

```dart
// Always validate ID parameters
Future<Response> _get(RequestContext context, String id) async {
  // Validate UUID format
  final validId = InputSanitizer.sanitizeUuid(id);
  if (validId == null) {
    return Response.json(
      statusCode: 400,
      body: {'error': 'Invalid ID format'},
    );
  }

  // Now safe to use
  final item = await repository.getById(validId);
  // ...
}
```

### Authorization Checks

```dart
// Always verify user has access to the resource
Future<Response> _get(RequestContext context, String id) async {
  final currentUser = context.read<User>();
  final item = await repository.getById(id);

  if (item == null) {
    return Response.json(statusCode: 404, body: {'error': 'Not found'});
  }

  // Check ownership or admin status
  if (item.ownerId != currentUser.id && !currentUser.isAdmin) {
    return Response.json(statusCode: 403, body: {'error': 'Access denied'});
  }

  return Response.json(body: item.toJson());
}
```

---

## Checklist

### Functionality
- [ ] Proper HTTP methods (GET, POST, PUT, DELETE)
- [ ] Appropriate status codes returned
- [ ] JSON content type headers
- [ ] Error handling with try/catch

### Security
- [ ] Input validation on ALL user data
- [ ] Input sanitization (escape, trim, limit length)
- [ ] ID parameter format validation
- [ ] Authorization checks (ownership/role)
- [ ] No mass assignment vulnerabilities
- [ ] Generic error messages in production
- [ ] Rate limiting on sensitive endpoints
- [ ] Request size limits enforced
- [ ] Authentication middleware applied
- [ ] Sensitive data excluded from responses
- [ ] No SQL/NoSQL injection (parameterized queries)
- [ ] CORS properly configured (not *)

### Best Practices
- [ ] Request logging (without sensitive data)
- [ ] Response caching headers where appropriate
- [ ] API versioning
