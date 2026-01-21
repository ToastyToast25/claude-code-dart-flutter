---
description: "Implements secure input handling, sanitization, and protection against XSS, SSRF, injection attacks"
globs: ["lib/**/*.dart", "backend/**/*.dart", "routes/**/*.dart"]
alwaysApply: false
---

# Input Security Skill

Secure input handling with protection against common web vulnerabilities (OWASP Top 10).

## Trigger Keywords
- input security
- sanitize input
- prevent xss
- prevent injection
- secure input
- input validation security

---

## XSS Prevention

### HTML Escaping

```dart
import 'dart:convert';

/// Escape HTML entities to prevent XSS
class HtmlSanitizer {
  HtmlSanitizer._();

  /// Escape HTML special characters
  static String escapeHtml(String input) {
    return const HtmlEscape().convert(input);
  }

  /// Escape for use in HTML attributes
  static String escapeAttribute(String input) {
    return const HtmlEscape(HtmlEscapeMode.attribute).convert(input);
  }

  /// Escape for use in single-quoted attributes
  static String escapeSqAttribute(String input) {
    return const HtmlEscape(HtmlEscapeMode.sqAttribute).convert(input);
  }

  /// Strip all HTML tags (for plain text only)
  static String stripHtml(String input) {
    return input.replaceAll(RegExp(r'<[^>]*>'), '');
  }

  /// Allow only safe HTML tags
  static String sanitizeHtml(String input, {List<String>? allowedTags}) {
    final allowed = allowedTags ?? ['b', 'i', 'u', 'strong', 'em', 'br', 'p'];
    final allowedPattern = allowed.join('|');

    // Remove all tags except allowed ones
    var result = input;

    // Remove script tags and their content
    result = result.replaceAll(
      RegExp(r'<script[^>]*>[\s\S]*?</script>', caseSensitive: false),
      '',
    );

    // Remove event handlers
    result = result.replaceAll(
      RegExp(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', caseSensitive: false),
      '',
    );

    // Remove javascript: and data: URLs
    result = result.replaceAll(
      RegExp(r'(href|src)\s*=\s*["\']?(javascript|data):[^"\'>\s]*', caseSensitive: false),
      '',
    );

    // Remove disallowed tags (keep allowed ones)
    result = result.replaceAllMapped(
      RegExp(r'</?([a-z][a-z0-9]*)[^>]*>', caseSensitive: false),
      (match) {
        final tag = match.group(1)?.toLowerCase();
        if (tag != null && allowed.contains(tag)) {
          return match.group(0)!;
        }
        return '';
      },
    );

    return result;
  }
}
```

### Content Security Policy

```dart
/// CSP header builder for web responses
class ContentSecurityPolicy {
  final Map<String, List<String>> _directives = {};

  ContentSecurityPolicy();

  /// Strict default policy
  factory ContentSecurityPolicy.strict() {
    return ContentSecurityPolicy()
      ..defaultSrc(["'self'"])
      ..scriptSrc(["'self'"])
      ..styleSrc(["'self'", "'unsafe-inline'"]) // Often needed for Flutter web
      ..imgSrc(["'self'", 'data:', 'https:'])
      ..fontSrc(["'self'"])
      ..connectSrc(["'self'"])
      ..frameAncestors(["'none'"])
      ..baseUri(["'self'"])
      ..formAction(["'self'"]);
  }

  void defaultSrc(List<String> sources) => _directives['default-src'] = sources;
  void scriptSrc(List<String> sources) => _directives['script-src'] = sources;
  void styleSrc(List<String> sources) => _directives['style-src'] = sources;
  void imgSrc(List<String> sources) => _directives['img-src'] = sources;
  void fontSrc(List<String> sources) => _directives['font-src'] = sources;
  void connectSrc(List<String> sources) => _directives['connect-src'] = sources;
  void frameAncestors(List<String> sources) => _directives['frame-ancestors'] = sources;
  void baseUri(List<String> sources) => _directives['base-uri'] = sources;
  void formAction(List<String> sources) => _directives['form-action'] = sources;

  String build() {
    return _directives.entries
        .map((e) => '${e.key} ${e.value.join(' ')}')
        .join('; ');
  }
}
```

### Flutter Web XSS Prevention

```dart
// Flutter already escapes text by default, but be careful with:

// ✅ Safe - Flutter escapes automatically
Text(userInput)
SelectableText(userInput)

// ⚠️ Dangerous - renders HTML
// Only use HtmlWidget with sanitized content
import 'package:flutter_html/flutter_html.dart';

Html(
  data: HtmlSanitizer.sanitizeHtml(userContent),
  // Whitelist allowed tags
  tagsList: const ['p', 'b', 'i', 'u', 'br', 'a'],
  onLinkTap: (url, _, __) {
    // Validate URL before opening
    if (UrlValidator.isSafeUrl(url)) {
      launchUrl(Uri.parse(url));
    }
  },
)

// ❌ Never do this
// ignore: avoid_web_only_libraries
import 'dart:html';
// document.body!.setInnerHtml(userInput); // XSS vulnerability!
```

---

## SSRF Prevention

### URL Validation

```dart
/// Validates URLs to prevent SSRF attacks
class UrlValidator {
  UrlValidator._();

  /// Blocked IP ranges (private, loopback, link-local)
  static final _blockedRanges = [
    // Loopback
    RegExp(r'^127\.'),
    RegExp(r'^::1$'),
    RegExp(r'^localhost$', caseSensitive: false),

    // Private networks
    RegExp(r'^10\.'),
    RegExp(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.'),
    RegExp(r'^192\.168\.'),

    // Link-local
    RegExp(r'^169\.254\.'),
    RegExp(r'^fe80:'),

    // Cloud metadata endpoints
    RegExp(r'^169\.254\.169\.254$'), // AWS/GCP metadata
    RegExp(r'^100\.100\.100\.200$'), // Alibaba Cloud
    RegExp(r'^metadata\.google\.internal$', caseSensitive: false),
  ];

  /// Blocked schemes
  static final _blockedSchemes = ['file', 'ftp', 'gopher', 'data', 'javascript'];

  /// Validate URL is safe for server-side requests
  static bool isSafeUrl(String? url) {
    if (url == null || url.isEmpty) return false;

    final uri = Uri.tryParse(url);
    if (uri == null) return false;

    return isSafeUri(uri);
  }

  /// Validate URI is safe for server-side requests
  static bool isSafeUri(Uri uri) {
    // Check scheme
    if (_blockedSchemes.contains(uri.scheme.toLowerCase())) {
      return false;
    }

    // Require HTTPS for external requests (or HTTP for development)
    if (uri.scheme != 'https' && uri.scheme != 'http') {
      return false;
    }

    // Check host
    final host = uri.host.toLowerCase();

    // Block empty host
    if (host.isEmpty) return false;

    // Block IP-based URLs to private ranges
    for (final pattern in _blockedRanges) {
      if (pattern.hasMatch(host)) {
        return false;
      }
    }

    // Block URLs with credentials
    if (uri.userInfo.isNotEmpty) {
      return false;
    }

    // Block suspicious ports
    final suspiciousPorts = [22, 23, 25, 445, 3389, 6379, 27017];
    if (uri.hasPort && suspiciousPorts.contains(uri.port)) {
      return false;
    }

    return true;
  }

  /// Resolve and validate URL (checks DNS resolution)
  static Future<bool> isSafeUrlResolved(String url) async {
    if (!isSafeUrl(url)) return false;

    final uri = Uri.parse(url);

    try {
      // Resolve hostname to IP addresses
      final addresses = await InternetAddress.lookup(uri.host);

      // Check all resolved IPs
      for (final address in addresses) {
        final ip = address.address;
        for (final pattern in _blockedRanges) {
          if (pattern.hasMatch(ip)) {
            return false; // DNS rebinding attack prevention
          }
        }
      }

      return true;
    } catch (e) {
      return false;
    }
  }

  /// Validate URL for user-facing links (less strict)
  static bool isValidUserUrl(String? url) {
    if (url == null || url.isEmpty) return false;

    final uri = Uri.tryParse(url);
    if (uri == null) return false;

    // Only allow http/https
    if (uri.scheme != 'http' && uri.scheme != 'https') {
      return false;
    }

    // Must have a host
    if (uri.host.isEmpty) return false;

    return true;
  }
}
```

### Safe HTTP Client

```dart
import 'package:http/http.dart' as http;

/// HTTP client with SSRF protections
class SafeHttpClient extends http.BaseClient {
  final http.Client _inner;
  final Duration _timeout;
  final int _maxRedirects;

  SafeHttpClient({
    http.Client? client,
    Duration timeout = const Duration(seconds: 30),
    int maxRedirects = 5,
  })  : _inner = client ?? http.Client(),
        _timeout = timeout,
        _maxRedirects = maxRedirects;

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    // Validate URL before making request
    if (!UrlValidator.isSafeUri(request.url)) {
      throw SecurityException('URL blocked by SSRF protection: ${request.url}');
    }

    // For extra safety, resolve and check DNS
    if (!await UrlValidator.isSafeUrlResolved(request.url.toString())) {
      throw SecurityException('URL failed DNS validation: ${request.url}');
    }

    // Make request with timeout
    final response = await _inner.send(request).timeout(_timeout);

    // Check redirect location
    if (response.isRedirect && response.headers.containsKey('location')) {
      final location = response.headers['location']!;
      if (!UrlValidator.isSafeUrl(location)) {
        throw SecurityException('Redirect blocked by SSRF protection: $location');
      }
    }

    return response;
  }

  @override
  void close() => _inner.close();
}

class SecurityException implements Exception {
  final String message;
  SecurityException(this.message);

  @override
  String toString() => 'SecurityException: $message';
}
```

---

## SQL/NoSQL Injection Prevention

### Parameterized Queries (Prisma)

```dart
// ✅ Always use Prisma's type-safe queries
final user = await prisma.user.findUnique(
  where: UserWhereUniqueInput(id: userId),
);

// ✅ Safe filtering
final users = await prisma.user.findMany(
  where: UserWhereInput(
    email: PrismaUnion.$1(StringFilter(contains: searchTerm)),
    status: PrismaUnion.$1(UserStatus.active),
  ),
);

// ❌ Never construct raw queries with user input
// final result = await prisma.$queryRaw("SELECT * FROM users WHERE email = '$email'");
```

### Raw Query Safety

```dart
// If you MUST use raw queries, use parameterized queries:

// PostgreSQL with parameters
final result = await connection.query(
  'SELECT * FROM users WHERE email = @email AND status = @status',
  substitutionValues: {
    'email': email,
    'status': status,
  },
);

// SQLite with parameters
final result = await db.rawQuery(
  'SELECT * FROM users WHERE email = ? AND status = ?',
  [email, status],
);
```

### NoSQL Injection Prevention

```dart
// MongoDB - avoid operator injection

// ❌ Vulnerable to operator injection
// final query = {'email': userInput}; // userInput could be {'$ne': ''}

// ✅ Explicitly cast to string
final query = {'email': userInput.toString()};

// ✅ Or validate input type
if (userInput is! String) {
  throw ValidationException('Invalid email format');
}

// ✅ Better: use a typed query builder
final users = await usersCollection.find(
  where.eq('email', email.toString()).eq('status', 'active'),
).toList();
```

---

## Command Injection Prevention

### Safe Process Execution

```dart
import 'dart:io';

/// Safe command execution utilities
class SafeProcess {
  SafeProcess._();

  /// Allowed commands whitelist
  static const _allowedCommands = [
    'convert', // ImageMagick
    'ffmpeg',
    'ffprobe',
    'git',
  ];

  /// Execute command with safety checks
  static Future<ProcessResult> run(
    String executable,
    List<String> arguments, {
    String? workingDirectory,
    Map<String, String>? environment,
  }) async {
    // Whitelist check
    if (!_allowedCommands.contains(executable)) {
      throw SecurityException('Command not in whitelist: $executable');
    }

    // Validate arguments - no shell metacharacters
    for (final arg in arguments) {
      if (_containsShellMetacharacters(arg)) {
        throw SecurityException('Invalid characters in argument: $arg');
      }
    }

    // Run without shell
    return Process.run(
      executable,
      arguments,
      workingDirectory: workingDirectory,
      environment: environment,
      runInShell: false, // IMPORTANT: Never run in shell
    );
  }

  /// Check for dangerous shell metacharacters
  static bool _containsShellMetacharacters(String input) {
    // Block shell metacharacters
    final dangerous = RegExp(r'[;&|`$(){}[\]<>!\n\r]');
    return dangerous.hasMatch(input);
  }

  /// Sanitize filename for use in commands
  static String sanitizeFilename(String filename) {
    // Only allow alphanumeric, dash, underscore, dot
    return filename.replaceAll(RegExp(r'[^a-zA-Z0-9._-]'), '_');
  }

  /// Validate file path is within allowed directory
  static bool isPathWithinDirectory(String path, String allowedDir) {
    final resolvedPath = File(path).absolute.path;
    final resolvedDir = Directory(allowedDir).absolute.path;
    return resolvedPath.startsWith(resolvedDir);
  }
}
```

---

## Path Traversal Prevention

```dart
/// Prevent path traversal attacks
class PathValidator {
  PathValidator._();

  /// Validate and sanitize file path
  static String? sanitizePath(String input, String baseDir) {
    // Remove null bytes
    var path = input.replaceAll('\x00', '');

    // Normalize path separators
    path = path.replaceAll('\\', '/');

    // Remove path traversal sequences
    while (path.contains('../') || path.contains('./')) {
      path = path.replaceAll('../', '').replaceAll('./', '');
    }

    // Resolve to absolute path
    final absolutePath = File('$baseDir/$path').absolute.path;
    final absoluteBase = Directory(baseDir).absolute.path;

    // Verify path is within base directory
    if (!absolutePath.startsWith(absoluteBase)) {
      return null; // Path traversal attempt
    }

    return absolutePath;
  }

  /// Check if filename is safe
  static bool isSafeFilename(String filename) {
    // No path separators
    if (filename.contains('/') || filename.contains('\\')) {
      return false;
    }

    // No special names
    if (filename == '.' || filename == '..') {
      return false;
    }

    // No null bytes
    if (filename.contains('\x00')) {
      return false;
    }

    // Only allowed characters
    return RegExp(r'^[a-zA-Z0-9._-]+$').hasMatch(filename);
  }
}
```

---

## Request Validation Middleware

```dart
import 'package:shelf/shelf.dart';
import 'dart:convert';

/// Security middleware for request validation
Middleware securityMiddleware() {
  return (Handler handler) {
    return (Request request) async {
      // 1. Validate Content-Type for POST/PUT/PATCH
      if (['POST', 'PUT', 'PATCH'].contains(request.method)) {
        final contentType = request.headers['content-type'];
        if (contentType == null ||
            !contentType.contains('application/json')) {
          return Response(
            415,
            body: jsonEncode({'error': 'Content-Type must be application/json'}),
          );
        }
      }

      // 2. Check request size
      final contentLength = request.headers['content-length'];
      if (contentLength != null) {
        final size = int.tryParse(contentLength) ?? 0;
        const maxSize = 1024 * 1024; // 1MB
        if (size > maxSize) {
          return Response(
            413,
            body: jsonEncode({'error': 'Request too large'}),
          );
        }
      }

      // 3. Validate JSON body
      if (['POST', 'PUT', 'PATCH'].contains(request.method)) {
        try {
          final body = await request.readAsString();
          if (body.isNotEmpty) {
            jsonDecode(body); // Validate JSON syntax
          }
        } catch (e) {
          return Response(
            400,
            body: jsonEncode({'error': 'Invalid JSON body'}),
          );
        }
      }

      // 4. Add security headers to response
      final response = await handler(request);
      return response.change(headers: {
        ...response.headers,
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
      });
    };
  };
}
```

---

## Input Sanitization Utilities

```dart
/// Comprehensive input sanitization
class InputSanitizer {
  InputSanitizer._();

  /// Sanitize string for general use
  static String sanitizeString(String input, {int maxLength = 1000}) {
    var result = input;

    // Trim whitespace
    result = result.trim();

    // Limit length
    if (result.length > maxLength) {
      result = result.substring(0, maxLength);
    }

    // Remove null bytes
    result = result.replaceAll('\x00', '');

    // Normalize Unicode
    result = result.replaceAll(RegExp(r'[\u200B-\u200D\uFEFF]'), ''); // Zero-width chars

    return result;
  }

  /// Sanitize for use in filenames
  static String sanitizeFilename(String input) {
    return input
        .replaceAll(RegExp(r'[<>:"/\\|?*\x00-\x1F]'), '_')
        .replaceAll('..', '_')
        .trim();
  }

  /// Sanitize email
  static String? sanitizeEmail(String input) {
    final email = input.trim().toLowerCase();
    final regex = RegExp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');
    return regex.hasMatch(email) ? email : null;
  }

  /// Sanitize phone number
  static String? sanitizePhone(String input) {
    final digits = input.replaceAll(RegExp(r'\D'), '');
    if (digits.length < 10 || digits.length > 15) {
      return null;
    }
    return digits;
  }

  /// Sanitize integer
  static int? sanitizeInt(dynamic input, {int? min, int? max}) {
    int? value;
    if (input is int) {
      value = input;
    } else if (input is String) {
      value = int.tryParse(input);
    }

    if (value == null) return null;
    if (min != null && value < min) return null;
    if (max != null && value > max) return null;

    return value;
  }

  /// Sanitize UUID
  static String? sanitizeUuid(String input) {
    final uuid = input.trim().toLowerCase();
    final regex = RegExp(
      r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    );
    return regex.hasMatch(uuid) ? uuid : null;
  }

  /// Sanitize slug
  static String sanitizeSlug(String input) {
    return input
        .toLowerCase()
        .trim()
        .replaceAll(RegExp(r'[^a-z0-9]+'), '-')
        .replaceAll(RegExp(r'^-+|-+$'), '');
  }
}
```

---

## Security Checklist

### Input Handling
- [ ] All user input is validated on the server
- [ ] Input length limits enforced
- [ ] Input type validation (string, int, email, etc.)
- [ ] Special characters escaped for output context

### XSS Prevention
- [ ] HTML output is escaped
- [ ] Content-Security-Policy header set
- [ ] No inline JavaScript with user data
- [ ] Rich text sanitized before rendering

### SSRF Prevention
- [ ] URLs validated before server-side requests
- [ ] Private IP ranges blocked
- [ ] Cloud metadata endpoints blocked
- [ ] Redirects validated

### Injection Prevention
- [ ] SQL queries use parameterized statements
- [ ] NoSQL queries validate input types
- [ ] Commands never use shell execution
- [ ] File paths validated against traversal

### General
- [ ] Security headers on all responses
- [ ] Rate limiting on sensitive endpoints
- [ ] Error messages don't leak internal details
- [ ] Logging doesn't include sensitive data

---

## Usage Examples

```
User: add xss protection to the api
User: sanitize user input before saving
User: prevent ssrf in the image proxy
User: secure the file upload endpoint
```
