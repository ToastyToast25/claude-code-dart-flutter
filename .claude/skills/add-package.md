---
description: "Adds packages to pubspec.yaml with proper configuration and setup"
globs: ["pubspec.yaml", "pubspec.lock"]
alwaysApply: false
---

# Add Package Skill

Add a new package to pubspec.yaml with proper configuration and setup.

## Trigger Keywords
- add package
- install package
- add dependency
- new package

---

## Workflow

### 1. Add Package

```bash
# Add regular dependency
flutter pub add [package_name]

# Add dev dependency
flutter pub add --dev [package_name]

# Add specific version
flutter pub add [package_name]:^1.0.0

# Add from git
flutter pub add [package_name] --git-url=https://github.com/user/repo.git
```

### 2. Update .gitignore (if needed)

Trigger `skills/gitignore.md` for packages that generate files:
- freezed / json_serializable → `*.g.dart`, `*.freezed.dart`
- build_runner → `.dart_tool/build/`
- hive → `*.hive`, `*.lock`

### 3. Run Setup Commands

Package-specific initialization if required.

---

## Common Packages Quick Setup

### State Management

#### Riverpod
```bash
flutter pub add flutter_riverpod
flutter pub add riverpod_annotation
flutter pub add --dev riverpod_generator
flutter pub add --dev build_runner
```

```dart
// main.dart
void main() {
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}
```

#### BLoC
```bash
flutter pub add flutter_bloc
flutter pub add bloc
flutter pub add equatable
```

### Code Generation

#### Freezed (Immutable classes)
```bash
flutter pub add freezed_annotation
flutter pub add --dev freezed
flutter pub add --dev build_runner
flutter pub add json_annotation
flutter pub add --dev json_serializable
```

```yaml
# build.yaml
targets:
  $default:
    builders:
      freezed:
        options:
          copy_with: true
          equal: true
          to_string: true
```

Run: `dart run build_runner build --delete-conflicting-outputs`

### Networking

#### Dio
```bash
flutter pub add dio
flutter pub add pretty_dio_logger
```

```dart
final dio = Dio(BaseOptions(
  baseUrl: 'https://api.example.com',
  connectTimeout: const Duration(seconds: 5),
  receiveTimeout: const Duration(seconds: 3),
));

dio.interceptors.add(PrettyDioLogger());
```

#### Retrofit
```bash
flutter pub add retrofit
flutter pub add --dev retrofit_generator
flutter pub add --dev build_runner
flutter pub add dio
```

### Local Storage

#### SharedPreferences
```bash
flutter pub add shared_preferences
```

```dart
final prefs = await SharedPreferences.getInstance();
await prefs.setString('key', 'value');
final value = prefs.getString('key');
```

#### Hive
```bash
flutter pub add hive
flutter pub add hive_flutter
flutter pub add --dev hive_generator
flutter pub add --dev build_runner
```

```dart
// main.dart
await Hive.initFlutter();
Hive.registerAdapter(UserAdapter());
await Hive.openBox<User>('users');
```

#### Flutter Secure Storage
```bash
flutter pub add flutter_secure_storage
```

### Navigation

#### go_router
```bash
flutter pub add go_router
```

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(),
    ),
  ],
);

// main.dart
MaterialApp.router(
  routerConfig: router,
)
```

#### auto_route
```bash
flutter pub add auto_route
flutter pub add --dev auto_route_generator
flutter pub add --dev build_runner
```

### UI Components

#### Google Fonts
```bash
flutter pub add google_fonts
```

```dart
Text(
  'Hello',
  style: GoogleFonts.roboto(fontSize: 24),
)
```

#### Flutter SVG
```bash
flutter pub add flutter_svg
```

```dart
SvgPicture.asset('assets/icon.svg')
```

#### Cached Network Image
```bash
flutter pub add cached_network_image
```

```dart
CachedNetworkImage(
  imageUrl: 'https://example.com/image.jpg',
  placeholder: (context, url) => CircularProgressIndicator(),
  errorWidget: (context, url, error) => Icon(Icons.error),
)
```

### Firebase

```bash
flutter pub add firebase_core
flutter pub add firebase_auth
flutter pub add cloud_firestore
flutter pub add firebase_analytics
```

```bash
# Initialize Firebase
flutterfire configure
```

### Testing

```bash
flutter pub add --dev mocktail
flutter pub add --dev bloc_test
flutter pub add --dev network_image_mock
```

### Functional Programming

#### fpdart
```bash
flutter pub add fpdart
```

```dart
Either<Failure, Success> result = Right(Success());
Option<User> user = Some(user);
```

### Utilities

#### intl (Localization)
```bash
flutter pub add intl
flutter pub add flutter_localizations --sdk=flutter
```

#### url_launcher
```bash
flutter pub add url_launcher
```

```dart
await launchUrl(Uri.parse('https://example.com'));
```

#### permission_handler
```bash
flutter pub add permission_handler
```

---

## Package Setup Checklist

After adding a package:

1. [ ] Run `flutter pub get`
2. [ ] Update `.gitignore` if generates files
3. [ ] Add initialization code to `main.dart` if required
4. [ ] Create wrapper/service class if needed
5. [ ] Add configuration files (build.yaml, etc.)
6. [ ] Run build_runner if code generation package
7. [ ] Update documentation if significant dependency

---

## Version Management

```yaml
# pubspec.yaml

dependencies:
  # Any version (not recommended)
  package: any

  # Exact version
  package: 1.2.3

  # Range (recommended)
  package: ^1.2.3  # >=1.2.3 <2.0.0

  # Minimum version
  package: ">=1.2.3"

  # Range with ceiling
  package: ">=1.2.3 <2.0.0"
```

---

## Dependency Overrides (Conflict Resolution)

```yaml
# pubspec.yaml

dependency_overrides:
  # Force specific version
  collection: 1.17.0

  # Use local path
  my_package:
    path: ../my_package

  # Use git
  my_package:
    git:
      url: https://github.com/user/repo.git
      ref: fix-branch
```

---

## Commands Reference

```bash
# Add package
flutter pub add [package]

# Add dev dependency
flutter pub add --dev [package]

# Remove package
flutter pub remove [package]

# Get all packages
flutter pub get

# Upgrade packages
flutter pub upgrade

# Check outdated
flutter pub outdated

# Show dependency tree
flutter pub deps

# Run build_runner
dart run build_runner build --delete-conflicting-outputs

# Watch mode (build_runner)
dart run build_runner watch --delete-conflicting-outputs
```
