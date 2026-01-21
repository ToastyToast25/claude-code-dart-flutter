---
description: Predefined package combinations for common Flutter project setups
globs:
  - "pubspec.yaml"
alwaysApply: false
---

# Package Presets

Pre-configured package combinations for different project types.

## When to Use

Use these presets when:
- Starting a new project
- Adding a new feature module
- Upgrading from basic to production setup

## Presets

### Preset: Minimal

Basic Flutter app with essentials only.

```yaml
dependencies:
  flutter:
    sdk: flutter

  # State (pick one)
  provider: ^6.1.1

  # HTTP
  http: ^1.1.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1
```

**Use for**: Prototypes, learning projects, simple apps

---

### Preset: Standard

Production-ready Flutter app.

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter

  # State Management
  flutter_riverpod: ^2.4.9
  riverpod_annotation: ^2.3.3

  # Networking
  dio: ^5.4.0
  retrofit: ^4.0.3
  connectivity_plus: ^5.0.2

  # Local Storage
  shared_preferences: ^2.2.2
  flutter_secure_storage: ^9.0.0

  # Navigation
  go_router: ^13.0.1

  # Models
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1
  equatable: ^2.0.5

  # Utilities
  dartz: ^0.10.1
  get_it: ^7.6.4
  injectable: ^2.3.2
  intl: ^0.18.1
  uuid: ^4.2.2

  # UI
  gap: ^3.0.1
  shimmer: ^3.0.0
  cached_network_image: ^3.3.1
  flutter_svg: ^2.0.9

  # Forms
  reactive_forms: ^16.1.1

  # Logging
  logger: ^2.0.2+1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1

  # Code Generation
  build_runner: ^2.4.8
  freezed: ^2.4.6
  json_serializable: ^6.7.1
  riverpod_generator: ^2.3.9
  injectable_generator: ^2.4.1
  retrofit_generator: ^8.0.6

  # Testing
  mocktail: ^1.0.1
  bloc_test: ^9.1.5
```

**Use for**: Most production apps

---

### Preset: Firebase

Full Firebase integration.

```yaml
dependencies:
  # ... include Standard preset ...

  # Firebase Core
  firebase_core: ^2.24.2
  firebase_auth: ^4.16.0
  cloud_firestore: ^4.14.0
  firebase_storage: ^11.6.0

  # Firebase Extras
  firebase_messaging: ^14.7.10
  firebase_analytics: ^10.8.0
  firebase_crashlytics: ^3.4.9
  firebase_remote_config: ^4.3.8

  # Auth Providers
  google_sign_in: ^6.2.1
  sign_in_with_apple: ^5.0.0

dev_dependencies:
  # ... include Standard preset ...
```

**Use for**: Apps using Firebase as backend

---

### Preset: Enterprise

Maximum reliability and monitoring.

```yaml
dependencies:
  # ... include Standard preset ...

  # Error Tracking
  sentry_flutter: ^7.14.0

  # Analytics
  firebase_analytics: ^10.8.0
  mixpanel_flutter: ^2.2.0

  # Performance
  firebase_performance: ^0.9.3+8

  # Feature Flags
  firebase_remote_config: ^4.3.8

  # Security
  local_auth: ^2.1.8           # Biometrics
  flutter_jailbreak_detection: ^1.10.0

  # Offline Support
  hive: ^2.2.3
  hive_flutter: ^1.1.0

  # Background Tasks
  workmanager: ^0.5.2

dev_dependencies:
  # ... include Standard preset ...

  # Additional Testing
  golden_toolkit: ^0.15.0
  patrol: ^3.3.0              # E2E testing
```

**Use for**: Large-scale apps, enterprise clients

---

### Preset: E-Commerce

Online store essentials.

```yaml
dependencies:
  # ... include Standard preset ...

  # Payments
  flutter_stripe: ^10.0.0

  # In-App Purchases
  in_app_purchase: ^3.1.13

  # Product Display
  carousel_slider: ^4.2.1
  photo_view: ^0.14.0
  smooth_page_indicator: ^1.1.0

  # Search
  algolia_helper_flutter: ^1.0.0

  # Maps (for delivery)
  google_maps_flutter: ^2.5.3
  geolocator: ^10.1.0

  # QR/Barcode
  mobile_scanner: ^3.5.5

dev_dependencies:
  # ... include Standard preset ...
```

**Use for**: Shopping apps, marketplaces

---

### Preset: Social

Social features and media.

```yaml
dependencies:
  # ... include Standard preset ...

  # Media
  image_picker: ^1.0.7
  video_player: ^2.8.2
  camera: ^0.10.5+7
  image_cropper: ^5.0.1

  # File Handling
  file_picker: ^6.1.1
  path_provider: ^2.1.2

  # Sharing
  share_plus: ^7.2.1

  # Deep Links
  uni_links: ^0.5.1
  firebase_dynamic_links: ^5.4.8

  # Push Notifications
  firebase_messaging: ^14.7.10
  flutter_local_notifications: ^16.3.0

  # Chat (if needed)
  # stream_chat_flutter: ^7.0.0

dev_dependencies:
  # ... include Standard preset ...
  network_image_mock: ^2.1.1
```

**Use for**: Social media apps, community apps

---

### Preset: Backend (dart_frog)

Dart backend server.

```yaml
name: backend
description: Dart backend server

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  dart_frog: ^1.1.0

  # Database
  postgres: ^2.6.4
  # OR
  # mysql_client: ^0.0.27

  # ORM
  prisma_client:
    git:
      url: https://github.com/prisma/prisma-dart.git
      path: packages/prisma_client

  # Authentication
  dart_jsonwebtoken: ^2.12.2
  crypto: ^3.0.3
  bcrypt: ^1.1.3

  # Validation
  validators: ^3.0.0

  # Utilities
  dotenv: ^4.2.0
  uuid: ^4.2.2
  collection: ^1.18.0

  # Email
  mailer: ^6.0.1

  # File Upload
  mime: ^1.0.5

dev_dependencies:
  dart_frog_test: ^1.0.0
  test: ^1.24.9
  mocktail: ^1.0.1
```

**Use for**: Dart backend APIs

---

## Quick Commands

### Add Standard Preset

```bash
# Add all standard dependencies at once
flutter pub add flutter_riverpod riverpod_annotation dio retrofit go_router freezed_annotation json_annotation equatable dartz get_it injectable intl

# Add dev dependencies
flutter pub add --dev build_runner freezed json_serializable riverpod_generator injectable_generator retrofit_generator mocktail
```

### Add Firebase Preset

```bash
# Core Firebase
flutter pub add firebase_core firebase_auth cloud_firestore

# Auth providers
flutter pub add google_sign_in sign_in_with_apple
```

### Add Enterprise Monitoring

```bash
flutter pub add sentry_flutter firebase_analytics firebase_performance firebase_crashlytics
```

## Version Compatibility Matrix

| Package | Flutter 3.16+ | Flutter 3.19+ |
|---------|---------------|---------------|
| riverpod | 2.4.x | 2.5.x |
| go_router | 13.x | 14.x |
| dio | 5.4.x | 5.4.x |
| freezed | 2.4.x | 2.5.x |

## Conflict Resolution

### State Management Conflicts

Don't mix:
- `provider` + `riverpod` (use riverpod only)
- `bloc` + `riverpod` (pick one)
- `getx` + anything else

### Storage Conflicts

Pick one per category:
- Local KV: `shared_preferences` OR `hive`
- Secure: Always use `flutter_secure_storage`
- Database: `sqflite` OR `drift` OR `hive`

### HTTP Conflicts

Pick one:
- `dio` (recommended, interceptors)
- `http` (simple, lightweight)
- `chopper` (code gen)
