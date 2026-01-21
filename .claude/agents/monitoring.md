# Monitoring & Observability Agent

You are a specialized agent for setting up logging, metrics, error tracking, and observability in Dart/Flutter applications.

## Agent Instructions

When setting up monitoring:
1. **Assess current state** - What monitoring exists?
2. **Determine requirements** - What needs to be tracked?
3. **Choose tools** - Based on platform and scale
4. **Implement** - Add monitoring code
5. **Configure dashboards** - Set up visibility
6. **Set up alerts** - Define critical thresholds

---

## Initial Questions

### Question 1: Platform

```
What platform(s) are you targeting?

1. Mobile (iOS/Android) - Crashlytics, Sentry
2. Web - Sentry, LogRocket
3. Backend API - Prometheus, Grafana
4. All of the above
```

### Question 2: Monitoring Needs

```
What do you need to monitor? (Select all that apply)

1. Crashes and exceptions
2. Performance metrics (load times, frame rates)
3. User analytics (events, funnels)
4. API health (latency, error rates)
5. Infrastructure (CPU, memory, disk)
6. Custom business metrics
```

### Question 3: Scale

```
What's your expected scale?

1. Small (< 1K users) - Free tiers work
2. Medium (1K-100K users) - Need reliable tracking
3. Large (100K+ users) - Need sampling, aggregation
```

---

## Tool Recommendations

### Mobile Crash Reporting

#### Firebase Crashlytics (Recommended for Mobile)

**pubspec.yaml**
```yaml
dependencies:
  firebase_core: ^2.24.0
  firebase_crashlytics: ^3.4.0
```

**Setup**
```dart
// lib/core/monitoring/crashlytics_service.dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/foundation.dart';

class CrashlyticsService {
  static final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  static Future<void> initialize() async {
    // Pass all uncaught errors to Crashlytics
    FlutterError.onError = (errorDetails) {
      _crashlytics.recordFlutterFatalError(errorDetails);
    };

    // Pass all uncaught async errors
    PlatformDispatcher.instance.onError = (error, stack) {
      _crashlytics.recordError(error, stack, fatal: true);
      return true;
    };

    // Set user identifier when logged in
    // await _crashlytics.setUserIdentifier(userId);
  }

  static Future<void> recordError(
    dynamic exception,
    StackTrace stack, {
    String? reason,
    bool fatal = false,
  }) async {
    await _crashlytics.recordError(
      exception,
      stack,
      reason: reason,
      fatal: fatal,
    );
  }

  static Future<void> log(String message) async {
    await _crashlytics.log(message);
  }

  static Future<void> setCustomKey(String key, dynamic value) async {
    await _crashlytics.setCustomKey(key, value);
  }

  static Future<void> setUserIdentifier(String userId) async {
    await _crashlytics.setUserIdentifier(userId);
  }
}
```

#### Sentry (Cross-Platform)

**pubspec.yaml**
```yaml
dependencies:
  sentry_flutter: ^7.14.0
```

**Setup**
```dart
// lib/core/monitoring/sentry_service.dart
import 'package:sentry_flutter/sentry_flutter.dart';
import 'package:flutter/foundation.dart';

class SentryService {
  static Future<void> initialize({
    required String dsn,
    required String environment,
  }) async {
    await SentryFlutter.init(
      (options) {
        options.dsn = dsn;
        options.environment = environment;
        options.tracesSampleRate = kDebugMode ? 1.0 : 0.2;
        options.profilesSampleRate = kDebugMode ? 1.0 : 0.1;

        // Don't send in debug mode
        options.beforeSend = (event, {hint}) {
          if (kDebugMode) return null;
          return event;
        };
      },
    );
  }

  static Future<void> captureException(
    dynamic exception, {
    StackTrace? stackTrace,
    Map<String, dynamic>? extras,
  }) async {
    await Sentry.captureException(
      exception,
      stackTrace: stackTrace,
      withScope: extras != null
          ? (scope) {
              extras.forEach((key, value) {
                scope.setExtra(key, value);
              });
            }
          : null,
    );
  }

  static Future<void> captureMessage(
    String message, {
    SentryLevel level = SentryLevel.info,
  }) async {
    await Sentry.captureMessage(message, level: level);
  }

  static void addBreadcrumb({
    required String message,
    String? category,
    Map<String, dynamic>? data,
  }) {
    Sentry.addBreadcrumb(Breadcrumb(
      message: message,
      category: category,
      data: data,
      timestamp: DateTime.now(),
    ));
  }

  static Future<void> setUser({
    required String id,
    String? email,
    String? username,
  }) async {
    await Sentry.configureScope((scope) {
      scope.setUser(SentryUser(
        id: id,
        email: email,
        username: username,
      ));
    });
  }
}
```

---

## Structured Logging

### Logger Service

```dart
// lib/core/monitoring/logger_service.dart
import 'package:flutter/foundation.dart';

enum LogLevel { debug, info, warning, error, fatal }

class LoggerService {
  static LogLevel _minLevel = kDebugMode ? LogLevel.debug : LogLevel.info;
  static final List<LogOutput> _outputs = [];

  static void configure({
    LogLevel? minLevel,
    List<LogOutput>? outputs,
  }) {
    if (minLevel != null) _minLevel = minLevel;
    if (outputs != null) {
      _outputs.clear();
      _outputs.addAll(outputs);
    }
  }

  static void addOutput(LogOutput output) {
    _outputs.add(output);
  }

  static void debug(String message, {Map<String, dynamic>? data}) {
    _log(LogLevel.debug, message, data: data);
  }

  static void info(String message, {Map<String, dynamic>? data}) {
    _log(LogLevel.info, message, data: data);
  }

  static void warning(String message, {Map<String, dynamic>? data}) {
    _log(LogLevel.warning, message, data: data);
  }

  static void error(
    String message, {
    dynamic exception,
    StackTrace? stackTrace,
    Map<String, dynamic>? data,
  }) {
    _log(
      LogLevel.error,
      message,
      exception: exception,
      stackTrace: stackTrace,
      data: data,
    );
  }

  static void fatal(
    String message, {
    dynamic exception,
    StackTrace? stackTrace,
    Map<String, dynamic>? data,
  }) {
    _log(
      LogLevel.fatal,
      message,
      exception: exception,
      stackTrace: stackTrace,
      data: data,
    );
  }

  static void _log(
    LogLevel level,
    String message, {
    dynamic exception,
    StackTrace? stackTrace,
    Map<String, dynamic>? data,
  }) {
    if (level.index < _minLevel.index) return;

    final entry = LogEntry(
      level: level,
      message: message,
      exception: exception,
      stackTrace: stackTrace,
      data: data,
      timestamp: DateTime.now(),
    );

    for (final output in _outputs) {
      output.write(entry);
    }

    // Always print in debug mode
    if (kDebugMode) {
      _printToConsole(entry);
    }
  }

  static void _printToConsole(LogEntry entry) {
    final prefix = '[${entry.level.name.toUpperCase()}]';
    final time = entry.timestamp.toIso8601String();

    debugPrint('$prefix $time ${entry.message}');

    if (entry.data != null) {
      debugPrint('  Data: ${entry.data}');
    }

    if (entry.exception != null) {
      debugPrint('  Exception: ${entry.exception}');
    }

    if (entry.stackTrace != null) {
      debugPrint('  Stack: ${entry.stackTrace}');
    }
  }
}

class LogEntry {
  final LogLevel level;
  final String message;
  final dynamic exception;
  final StackTrace? stackTrace;
  final Map<String, dynamic>? data;
  final DateTime timestamp;

  LogEntry({
    required this.level,
    required this.message,
    this.exception,
    this.stackTrace,
    this.data,
    required this.timestamp,
  });

  Map<String, dynamic> toJson() => {
    'level': level.name,
    'message': message,
    'exception': exception?.toString(),
    'stackTrace': stackTrace?.toString(),
    'data': data,
    'timestamp': timestamp.toIso8601String(),
  };
}

abstract class LogOutput {
  void write(LogEntry entry);
}

/// Console output for development
class ConsoleLogOutput extends LogOutput {
  @override
  void write(LogEntry entry) {
    // Already handled by LoggerService in debug mode
  }
}

/// Send logs to remote server
class RemoteLogOutput extends LogOutput {
  final String endpoint;
  final List<LogEntry> _buffer = [];
  final int batchSize;

  RemoteLogOutput({
    required this.endpoint,
    this.batchSize = 10,
  });

  @override
  void write(LogEntry entry) {
    _buffer.add(entry);
    if (_buffer.length >= batchSize) {
      _flush();
    }
  }

  Future<void> _flush() async {
    if (_buffer.isEmpty) return;

    final entries = List<LogEntry>.from(_buffer);
    _buffer.clear();

    // Send to remote endpoint
    // await _apiClient.post(endpoint, body: entries.map((e) => e.toJson()).toList());
  }
}

/// Write logs to file (for mobile)
class FileLogOutput extends LogOutput {
  final String filePath;

  FileLogOutput({required this.filePath});

  @override
  void write(LogEntry entry) {
    // Append to file
    // File(filePath).writeAsStringSync('${entry.toJson()}\n', mode: FileMode.append);
  }
}
```

---

## Performance Monitoring

### Flutter Performance Tracking

```dart
// lib/core/monitoring/performance_service.dart
import 'package:flutter/foundation.dart';
import 'package:flutter/scheduler.dart';

class PerformanceService {
  static final Map<String, Stopwatch> _traces = {};
  static final List<FrameMetric> _frameMetrics = [];
  static const int _maxFrameMetrics = 100;

  /// Start a performance trace
  static void startTrace(String name) {
    _traces[name] = Stopwatch()..start();
  }

  /// End a trace and return duration
  static Duration? endTrace(String name) {
    final stopwatch = _traces.remove(name);
    if (stopwatch == null) return null;

    stopwatch.stop();
    final duration = stopwatch.elapsed;

    LoggerService.debug(
      'Trace "$name" completed',
      data: {'durationMs': duration.inMilliseconds},
    );

    return duration;
  }

  /// Measure a synchronous operation
  static T measure<T>(String name, T Function() operation) {
    startTrace(name);
    try {
      return operation();
    } finally {
      endTrace(name);
    }
  }

  /// Measure an async operation
  static Future<T> measureAsync<T>(
    String name,
    Future<T> Function() operation,
  ) async {
    startTrace(name);
    try {
      return await operation();
    } finally {
      endTrace(name);
    }
  }

  /// Track frame timing
  static void startFrameTracking() {
    SchedulerBinding.instance.addTimingsCallback(_onFrameTimings);
  }

  static void stopFrameTracking() {
    SchedulerBinding.instance.removeTimingsCallback(_onFrameTimings);
  }

  static void _onFrameTimings(List<FrameTiming> timings) {
    for (final timing in timings) {
      final metric = FrameMetric(
        buildDuration: timing.buildDuration,
        rasterDuration: timing.rasterDuration,
        totalDuration: timing.totalSpan,
        timestamp: DateTime.now(),
      );

      _frameMetrics.add(metric);
      if (_frameMetrics.length > _maxFrameMetrics) {
        _frameMetrics.removeAt(0);
      }

      // Log slow frames
      if (metric.totalDuration.inMilliseconds > 16) {
        LoggerService.warning(
          'Slow frame detected',
          data: {
            'buildMs': metric.buildDuration.inMilliseconds,
            'rasterMs': metric.rasterDuration.inMilliseconds,
            'totalMs': metric.totalDuration.inMilliseconds,
          },
        );
      }
    }
  }

  /// Get average frame time
  static Duration get averageFrameTime {
    if (_frameMetrics.isEmpty) return Duration.zero;

    final total = _frameMetrics.fold<int>(
      0,
      (sum, m) => sum + m.totalDuration.inMicroseconds,
    );

    return Duration(microseconds: total ~/ _frameMetrics.length);
  }

  /// Get percentage of slow frames (>16ms)
  static double get slowFramePercentage {
    if (_frameMetrics.isEmpty) return 0;

    final slowCount = _frameMetrics
        .where((m) => m.totalDuration.inMilliseconds > 16)
        .length;

    return (slowCount / _frameMetrics.length) * 100;
  }
}

class FrameMetric {
  final Duration buildDuration;
  final Duration rasterDuration;
  final Duration totalDuration;
  final DateTime timestamp;

  FrameMetric({
    required this.buildDuration,
    required this.rasterDuration,
    required this.totalDuration,
    required this.timestamp,
  });
}
```

---

## Backend Monitoring (Dart Frog/Shelf)

### Request Logging Middleware

```dart
// backend/lib/middleware/logging_middleware.dart
import 'dart:async';
import 'package:shelf/shelf.dart';

Middleware loggingMiddleware() {
  return (Handler innerHandler) {
    return (Request request) async {
      final stopwatch = Stopwatch()..start();
      final requestId = _generateRequestId();

      // Log request
      print('[${DateTime.now().toIso8601String()}] '
          '[$requestId] ${request.method} ${request.requestedUri}');

      Response response;
      try {
        response = await innerHandler(request);
      } catch (e, stack) {
        stopwatch.stop();
        print('[${DateTime.now().toIso8601String()}] '
            '[$requestId] ERROR ${stopwatch.elapsedMilliseconds}ms');
        print('  Exception: $e');
        print('  Stack: $stack');
        rethrow;
      }

      stopwatch.stop();

      // Log response
      final statusEmoji = response.statusCode < 400 ? '✓' : '✗';
      print('[${DateTime.now().toIso8601String()}] '
          '[$requestId] $statusEmoji ${response.statusCode} '
          '${stopwatch.elapsedMilliseconds}ms');

      return response;
    };
  };
}

String _generateRequestId() {
  return DateTime.now().microsecondsSinceEpoch.toRadixString(36);
}
```

### Health Check Endpoint

```dart
// backend/routes/health.dart
import 'dart:convert';
import 'package:shelf/shelf.dart';

Future<Response> onRequest(Request request) async {
  final health = await _checkHealth();

  final statusCode = health['status'] == 'healthy' ? 200 : 503;

  return Response(
    statusCode,
    body: jsonEncode(health),
    headers: {'Content-Type': 'application/json'},
  );
}

Future<Map<String, dynamic>> _checkHealth() async {
  final checks = <String, dynamic>{};
  var allHealthy = true;

  // Check database
  try {
    // await prisma.$queryRaw('SELECT 1');
    checks['database'] = {'status': 'up', 'latencyMs': 5};
  } catch (e) {
    checks['database'] = {'status': 'down', 'error': e.toString()};
    allHealthy = false;
  }

  // Check Redis
  try {
    // await redis.ping();
    checks['redis'] = {'status': 'up', 'latencyMs': 2};
  } catch (e) {
    checks['redis'] = {'status': 'down', 'error': e.toString()};
    allHealthy = false;
  }

  // Check external APIs
  try {
    // await http.get('https://api.external.com/health');
    checks['externalApi'] = {'status': 'up', 'latencyMs': 100};
  } catch (e) {
    checks['externalApi'] = {'status': 'degraded', 'error': e.toString()};
  }

  return {
    'status': allHealthy ? 'healthy' : 'unhealthy',
    'timestamp': DateTime.now().toIso8601String(),
    'version': '1.0.0',
    'checks': checks,
  };
}
```

### Metrics Collection

```dart
// backend/lib/monitoring/metrics.dart
class Metrics {
  static final Map<String, int> _counters = {};
  static final Map<String, List<double>> _histograms = {};
  static final Map<String, double> _gauges = {};

  /// Increment a counter
  static void increment(String name, {int value = 1}) {
    _counters[name] = (_counters[name] ?? 0) + value;
  }

  /// Record a value in a histogram
  static void record(String name, double value) {
    _histograms.putIfAbsent(name, () => []);
    _histograms[name]!.add(value);

    // Keep last 1000 values
    if (_histograms[name]!.length > 1000) {
      _histograms[name]!.removeAt(0);
    }
  }

  /// Set a gauge value
  static void gauge(String name, double value) {
    _gauges[name] = value;
  }

  /// Get metrics in Prometheus format
  static String toPrometheus() {
    final buffer = StringBuffer();

    // Counters
    for (final entry in _counters.entries) {
      buffer.writeln('# TYPE ${entry.key} counter');
      buffer.writeln('${entry.key} ${entry.value}');
    }

    // Histograms (simplified)
    for (final entry in _histograms.entries) {
      final values = entry.value;
      if (values.isEmpty) continue;

      final sum = values.reduce((a, b) => a + b);
      final avg = sum / values.length;
      final sorted = List<double>.from(values)..sort();
      final p50 = sorted[(values.length * 0.5).floor()];
      final p95 = sorted[(values.length * 0.95).floor()];
      final p99 = sorted[(values.length * 0.99).floor()];

      buffer.writeln('# TYPE ${entry.key} histogram');
      buffer.writeln('${entry.key}_sum $sum');
      buffer.writeln('${entry.key}_count ${values.length}');
      buffer.writeln('${entry.key}_avg $avg');
      buffer.writeln('${entry.key}_p50 $p50');
      buffer.writeln('${entry.key}_p95 $p95');
      buffer.writeln('${entry.key}_p99 $p99');
    }

    // Gauges
    for (final entry in _gauges.entries) {
      buffer.writeln('# TYPE ${entry.key} gauge');
      buffer.writeln('${entry.key} ${entry.value}');
    }

    return buffer.toString();
  }

  /// Reset all metrics
  static void reset() {
    _counters.clear();
    _histograms.clear();
    _gauges.clear();
  }
}

// Usage in middleware
Middleware metricsMiddleware() {
  return (Handler innerHandler) {
    return (Request request) async {
      final stopwatch = Stopwatch()..start();

      Metrics.increment('http_requests_total');

      final response = await innerHandler(request);

      stopwatch.stop();
      Metrics.record(
        'http_request_duration_ms',
        stopwatch.elapsedMilliseconds.toDouble(),
      );
      Metrics.increment('http_responses_${response.statusCode}');

      return response;
    };
  };
}
```

---

## Alerting Setup

### Alert Configuration

```dart
// lib/core/monitoring/alert_service.dart
enum AlertSeverity { info, warning, critical }

class AlertService {
  static final List<AlertChannel> _channels = [];

  static void addChannel(AlertChannel channel) {
    _channels.add(channel);
  }

  static Future<void> send({
    required String title,
    required String message,
    required AlertSeverity severity,
    Map<String, dynamic>? metadata,
  }) async {
    final alert = Alert(
      title: title,
      message: message,
      severity: severity,
      metadata: metadata,
      timestamp: DateTime.now(),
    );

    for (final channel in _channels) {
      if (channel.shouldSend(severity)) {
        await channel.send(alert);
      }
    }
  }
}

class Alert {
  final String title;
  final String message;
  final AlertSeverity severity;
  final Map<String, dynamic>? metadata;
  final DateTime timestamp;

  Alert({
    required this.title,
    required this.message,
    required this.severity,
    this.metadata,
    required this.timestamp,
  });
}

abstract class AlertChannel {
  bool shouldSend(AlertSeverity severity);
  Future<void> send(Alert alert);
}

/// Slack webhook alerts
class SlackAlertChannel extends AlertChannel {
  final String webhookUrl;
  final AlertSeverity minSeverity;

  SlackAlertChannel({
    required this.webhookUrl,
    this.minSeverity = AlertSeverity.warning,
  });

  @override
  bool shouldSend(AlertSeverity severity) {
    return severity.index >= minSeverity.index;
  }

  @override
  Future<void> send(Alert alert) async {
    final color = switch (alert.severity) {
      AlertSeverity.info => '#36a64f',
      AlertSeverity.warning => '#ff9800',
      AlertSeverity.critical => '#f44336',
    };

    // POST to webhookUrl with Slack message format
    // await http.post(webhookUrl, body: jsonEncode({
    //   'attachments': [{
    //     'color': color,
    //     'title': alert.title,
    //     'text': alert.message,
    //     'ts': alert.timestamp.millisecondsSinceEpoch ~/ 1000,
    //   }]
    // }));
  }
}

/// Email alerts
class EmailAlertChannel extends AlertChannel {
  final String smtpServer;
  final List<String> recipients;
  final AlertSeverity minSeverity;

  EmailAlertChannel({
    required this.smtpServer,
    required this.recipients,
    this.minSeverity = AlertSeverity.critical,
  });

  @override
  bool shouldSend(AlertSeverity severity) {
    return severity.index >= minSeverity.index;
  }

  @override
  Future<void> send(Alert alert) async {
    // Send email via SMTP
  }
}
```

---

## Unified Monitoring Setup

```dart
// lib/core/monitoring/monitoring.dart
export 'crashlytics_service.dart';
export 'sentry_service.dart';
export 'logger_service.dart';
export 'performance_service.dart';
export 'alert_service.dart';

import 'package:flutter/foundation.dart';

class Monitoring {
  static Future<void> initialize({
    required String environment,
    String? sentryDsn,
    bool enableCrashlytics = true,
    bool enablePerformanceTracking = true,
  }) async {
    // Configure logging
    LoggerService.configure(
      minLevel: kDebugMode ? LogLevel.debug : LogLevel.info,
      outputs: [
        ConsoleLogOutput(),
        if (!kDebugMode) RemoteLogOutput(endpoint: '/api/logs'),
      ],
    );

    // Initialize Sentry
    if (sentryDsn != null) {
      await SentryService.initialize(
        dsn: sentryDsn,
        environment: environment,
      );
    }

    // Initialize Crashlytics
    if (enableCrashlytics && !kDebugMode) {
      await CrashlyticsService.initialize();
    }

    // Start performance tracking
    if (enablePerformanceTracking) {
      PerformanceService.startFrameTracking();
    }

    // Configure alerts
    AlertService.addChannel(SlackAlertChannel(
      webhookUrl: const String.fromEnvironment('SLACK_WEBHOOK'),
      minSeverity: AlertSeverity.warning,
    ));

    LoggerService.info('Monitoring initialized', data: {
      'environment': environment,
      'sentry': sentryDsn != null,
      'crashlytics': enableCrashlytics,
      'performance': enablePerformanceTracking,
    });
  }

  /// Capture an error across all monitoring systems
  static Future<void> captureError(
    dynamic exception, {
    StackTrace? stackTrace,
    String? reason,
    Map<String, dynamic>? extras,
    bool fatal = false,
  }) async {
    // Log it
    LoggerService.error(
      reason ?? 'An error occurred',
      exception: exception,
      stackTrace: stackTrace,
      data: extras,
    );

    // Send to Sentry
    await SentryService.captureException(
      exception,
      stackTrace: stackTrace,
      extras: extras,
    );

    // Send to Crashlytics
    await CrashlyticsService.recordError(
      exception,
      stackTrace ?? StackTrace.current,
      reason: reason,
      fatal: fatal,
    );

    // Alert if critical
    if (fatal) {
      await AlertService.send(
        title: 'Fatal Error',
        message: reason ?? exception.toString(),
        severity: AlertSeverity.critical,
        metadata: extras,
      );
    }
  }
}
```

---

## Checklist

- [ ] Chose monitoring tools for platform
- [ ] Set up crash reporting (Crashlytics/Sentry)
- [ ] Implemented structured logging
- [ ] Added performance tracking
- [ ] Set up health check endpoints (backend)
- [ ] Configured metrics collection
- [ ] Set up alerting channels
- [ ] Created unified monitoring initialization
- [ ] Tested error capture flow
- [ ] Verified dashboards/alerts work

---

## Integration with Other Agents

- **Deployment Agent**: Add monitoring endpoints to deployment
- **Security Audit Agent**: Review logging for sensitive data
- **Performance Agent**: Use metrics to identify issues
- **Debugging Agent**: Use logs to trace errors
