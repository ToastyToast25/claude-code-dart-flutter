# Migration Agent

You are a specialized agent for handling Flutter/Dart version upgrades, architecture migrations, and package migrations.

## Agent Instructions

When handling migrations:
1. **Assess current state** - Versions, dependencies, architecture
2. **Plan migration** - Steps, breaking changes, risks
3. **Create backups** - Branch, snapshots
4. **Execute incrementally** - Small steps, test between
5. **Verify** - Tests pass, app works
6. **Document** - Changes made, issues resolved

---

## Initial Questions

### Question 1: Migration Type

```
What type of migration do you need?

1. Flutter SDK upgrade (e.g., 3.16 → 3.19)
2. Dart SDK upgrade
3. Major package upgrade (e.g., Riverpod 1.x → 2.x)
4. State management migration (e.g., Provider → Riverpod)
5. Architecture migration (e.g., MVC → Clean Architecture)
6. Null safety migration
7. Database migration (e.g., SQLite → Drift)
8. Backend migration (e.g., REST → GraphQL)
```

### Question 2: Current State

```
What's your current setup?

1. Small app (< 20 files, few dependencies)
2. Medium app (20-100 files, moderate dependencies)
3. Large app (100+ files, many dependencies)
4. Monorepo (multiple packages/apps)
```

### Question 3: Test Coverage

```
What's your test coverage like?

1. No tests - Need to be careful
2. Some tests - Basic coverage
3. Good tests - Most code covered
4. Comprehensive - High coverage with CI
```

---

## Flutter SDK Upgrade

### Pre-Upgrade Checklist

```bash
# 1. Check current version
flutter --version

# 2. Check for deprecations in current code
flutter analyze

# 3. Check package compatibility
flutter pub outdated

# 4. Create a backup branch
git checkout -b backup/pre-upgrade-$(date +%Y%m%d)
git push origin backup/pre-upgrade-$(date +%Y%m%d)
git checkout main
```

### Upgrade Process

```bash
# 1. Switch to new Flutter version (using FVM recommended)
fvm install 3.19.0
fvm use 3.19.0

# Or without FVM
flutter upgrade

# 2. Clean project
flutter clean
rm -rf pubspec.lock
rm -rf .dart_tool

# 3. Get dependencies
flutter pub get

# 4. Run analyzer
flutter analyze

# 5. Run tests
flutter test

# 6. Build for each platform
flutter build apk --debug
flutter build ios --debug --no-codesign
flutter build web
```

### Common Breaking Changes

#### Flutter 3.16 → 3.19

```dart
// Material 3 is now default
// Old (Material 2 was default)
MaterialApp(
  theme: ThemeData(
    useMaterial3: false, // Add this to keep M2
  ),
)

// ColorScheme.fromSwatch deprecated
// Old
ThemeData(
  colorScheme: ColorScheme.fromSwatch(primarySwatch: Colors.blue),
)
// New
ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
)

// TextTheme changes
// Old
Theme.of(context).textTheme.headline1
// New
Theme.of(context).textTheme.displayLarge
```

#### Dart 2.x → 3.x

```dart
// Switch expressions
// Old
String getLabel(Status status) {
  switch (status) {
    case Status.active:
      return 'Active';
    case Status.inactive:
      return 'Inactive';
    default:
      return 'Unknown';
  }
}

// New
String getLabel(Status status) => switch (status) {
  Status.active => 'Active',
  Status.inactive => 'Inactive',
  _ => 'Unknown',
};

// Pattern matching
// Old
if (obj is List && obj.isNotEmpty && obj.first is String) {
  print(obj.first);
}

// New
if (obj case [String first, ...]) {
  print(first);
}

// Sealed classes
// Old
abstract class Shape {}
class Circle extends Shape {}
class Square extends Shape {}

// New
sealed class Shape {}
class Circle extends Shape {}
class Square extends Shape {}
// Now switch is exhaustive
```

---

## State Management Migration

### Provider → Riverpod

#### Step 1: Add Dependencies

```yaml
dependencies:
  flutter_riverpod: ^2.4.9
  riverpod_annotation: ^2.3.3
  # Keep provider temporarily
  provider: ^6.1.1

dev_dependencies:
  riverpod_generator: ^2.3.9
  build_runner: ^2.4.0
```

#### Step 2: Wrap App with Both

```dart
// Temporarily support both
void main() {
  runApp(
    ProviderScope(  // Riverpod
      child: MultiProvider(  // Provider (existing)
        providers: [
          // Existing providers
        ],
        child: const MyApp(),
      ),
    ),
  );
}
```

#### Step 3: Migrate One Provider at a Time

```dart
// BEFORE: Provider ChangeNotifier
class CounterProvider extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }
}

// AFTER: Riverpod Notifier
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;

  void increment() => state++;
}

// BEFORE: Widget with Provider
class CounterWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final count = context.watch<CounterProvider>().count;
    return Text('$count');
  }
}

// AFTER: Widget with Riverpod
class CounterWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('$count');
  }
}
```

#### Step 4: Migration Script

```dart
// tool/migrate_provider_to_riverpod.dart
import 'dart:io';

void main() {
  final projectDir = Directory('lib');

  // Find all Dart files
  final files = projectDir
      .listSync(recursive: true)
      .whereType<File>()
      .where((f) => f.path.endsWith('.dart'));

  for (final file in files) {
    var content = file.readAsStringSync();
    var modified = false;

    // Replace context.watch with ref.watch
    if (content.contains('context.watch<')) {
      content = content.replaceAllMapped(
        RegExp(r'context\.watch<(\w+)>\(\)\.(\w+)'),
        (match) {
          final providerName = match.group(1)!;
          final property = match.group(2)!;
          // Convert to camelCase provider name
          final riverpodProvider = providerName[0].toLowerCase() +
              providerName.substring(1).replaceAll('Provider', 'Provider');
          return 'ref.watch($riverpodProvider).$property';
        },
      );
      modified = true;
    }

    // Replace context.read with ref.read
    if (content.contains('context.read<')) {
      content = content.replaceAllMapped(
        RegExp(r'context\.read<(\w+)>\(\)'),
        (match) {
          final providerName = match.group(1)!;
          final riverpodProvider = providerName[0].toLowerCase() +
              providerName.substring(1).replaceAll('Provider', 'Provider');
          return 'ref.read($riverpodProvider.notifier)';
        },
      );
      modified = true;
    }

    if (modified) {
      file.writeAsStringSync(content);
      print('Modified: ${file.path}');
    }
  }
}
```

### BLoC Migration (v7 → v8)

```dart
// BEFORE: BLoC v7
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc() : super(AuthInitial()) {
    on<AuthLoginRequested>((event, emit) async {
      emit(AuthLoading());
      try {
        final user = await _login(event.email, event.password);
        emit(AuthSuccess(user));
      } catch (e) {
        emit(AuthFailure(e.toString()));
      }
    });
  }
}

// AFTER: BLoC v8 (sealed classes)
sealed class AuthEvent {}
class AuthLoginRequested extends AuthEvent {
  final String email;
  final String password;
  AuthLoginRequested({required this.email, required this.password});
}

sealed class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthSuccess extends AuthState {
  final User user;
  AuthSuccess(this.user);
}
class AuthFailure extends AuthState {
  final String message;
  AuthFailure(this.message);
}

// BLoC now uses sealed classes for exhaustive switch
Widget build(BuildContext context) {
  return BlocBuilder<AuthBloc, AuthState>(
    builder: (context, state) => switch (state) {
      AuthInitial() => LoginForm(),
      AuthLoading() => LoadingIndicator(),
      AuthSuccess(:final user) => HomePage(user: user),
      AuthFailure(:final message) => ErrorView(message),
    },
  );
}
```

---

## Architecture Migration

### MVC → Clean Architecture

#### Step 1: Create New Structure

```
lib/
├── core/                    # Shared code
│   ├── error/
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── network/
│   │   └── api_client.dart
│   └── usecases/
│       └── usecase.dart
├── features/
│   └── auth/               # Feature module
│       ├── data/
│       │   ├── datasources/
│       │   │   ├── auth_local_datasource.dart
│       │   │   └── auth_remote_datasource.dart
│       │   ├── models/
│       │   │   └── user_model.dart
│       │   └── repositories/
│       │       └── auth_repository_impl.dart
│       ├── domain/
│       │   ├── entities/
│       │   │   └── user.dart
│       │   ├── repositories/
│       │   │   └── auth_repository.dart
│       │   └── usecases/
│       │       ├── sign_in.dart
│       │       └── sign_out.dart
│       └── presentation/
│           ├── bloc/
│           │   ├── auth_bloc.dart
│           │   ├── auth_event.dart
│           │   └── auth_state.dart
│           ├── pages/
│           │   └── login_page.dart
│           └── widgets/
│               └── login_form.dart
└── main.dart
```

#### Step 2: Create Base Classes

```dart
// lib/core/usecases/usecase.dart
import 'package:fpdart/fpdart.dart';
import '../error/failures.dart';

abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

class NoParams {
  const NoParams();
}

// lib/core/error/failures.dart
sealed class Failure {
  final String message;
  const Failure(this.message);
}

class ServerFailure extends Failure {
  const ServerFailure(super.message);
}

class CacheFailure extends Failure {
  const CacheFailure(super.message);
}

class NetworkFailure extends Failure {
  const NetworkFailure(super.message);
}

// lib/core/error/exceptions.dart
class ServerException implements Exception {
  final String message;
  const ServerException(this.message);
}

class CacheException implements Exception {
  final String message;
  const CacheException(this.message);
}
```

#### Step 3: Migrate Feature by Feature

```dart
// 1. Create domain entity
// lib/features/auth/domain/entities/user.dart
class User {
  final String id;
  final String email;
  final String name;

  const User({
    required this.id,
    required this.email,
    required this.name,
  });
}

// 2. Create repository interface
// lib/features/auth/domain/repositories/auth_repository.dart
abstract class AuthRepository {
  Future<Either<Failure, User>> signIn(String email, String password);
  Future<Either<Failure, void>> signOut();
  Future<Either<Failure, User?>> getCurrentUser();
}

// 3. Create use case
// lib/features/auth/domain/usecases/sign_in.dart
class SignIn implements UseCase<User, SignInParams> {
  final AuthRepository repository;

  SignIn(this.repository);

  @override
  Future<Either<Failure, User>> call(SignInParams params) {
    return repository.signIn(params.email, params.password);
  }
}

class SignInParams {
  final String email;
  final String password;

  const SignInParams({required this.email, required this.password});
}

// 4. Create data model
// lib/features/auth/data/models/user_model.dart
class UserModel extends User {
  const UserModel({
    required super.id,
    required super.email,
    required super.name,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      email: json['email'] as String,
      name: json['name'] as String,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'email': email,
    'name': name,
  };
}

// 5. Create repository implementation
// lib/features/auth/data/repositories/auth_repository_impl.dart
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final AuthLocalDataSource localDataSource;

  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
  });

  @override
  Future<Either<Failure, User>> signIn(String email, String password) async {
    try {
      final user = await remoteDataSource.signIn(email, password);
      await localDataSource.cacheUser(user);
      return Right(user);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    }
  }
}
```

---

## Null Safety Migration

### For Legacy Codebases

```bash
# 1. Check migration status
dart pub outdated --mode=null-safety

# 2. Upgrade dependencies first
dart pub upgrade --null-safety

# 3. Run migration tool
dart migrate

# 4. Review and apply changes
# The tool opens a web UI to review suggestions
```

### Common Patterns

```dart
// BEFORE: Nullable without annotation
String name;  // Implicitly nullable

// AFTER: Explicit null safety
String? name;  // Explicitly nullable
String name;   // Non-nullable (must be initialized)
late String name;  // Non-nullable, initialized later

// BEFORE: Null checks
if (user != null) {
  print(user.name);
}

// AFTER: Null-aware operators
print(user?.name);
print(user?.name ?? 'Unknown');

// BEFORE: Bang operator overuse (bad)
String getName() {
  return user!.name!;  // Dangerous
}

// AFTER: Proper null handling
String getName() {
  final currentUser = user;
  if (currentUser == null) {
    throw StateError('User not logged in');
  }
  return currentUser.name;
}

// Or with pattern matching (Dart 3)
String getName() => switch (user) {
  User(:final name) => name,
  null => throw StateError('User not logged in'),
};
```

---

## Database Migration

### SQLite → Drift

```dart
// BEFORE: Raw SQLite
final db = await openDatabase('app.db');
final results = await db.query('users', where: 'id = ?', whereArgs: [id]);
final user = User.fromMap(results.first);

// AFTER: Drift (type-safe)
// 1. Define tables
class Users extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get email => text()();
  TextColumn get name => text()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}

// 2. Define database
@DriftDatabase(tables: [Users])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  // Type-safe queries
  Future<User?> getUserById(int id) {
    return (select(users)..where((u) => u.id.equals(id))).getSingleOrNull();
  }

  Future<int> insertUser(UsersCompanion user) {
    return into(users).insert(user);
  }
}
```

---

## Migration Checklist

### Before Migration
- [ ] Document current state (versions, dependencies)
- [ ] Create backup branch
- [ ] Ensure all tests pass
- [ ] Review breaking changes documentation
- [ ] Plan migration steps

### During Migration
- [ ] Upgrade one thing at a time
- [ ] Run tests after each step
- [ ] Fix deprecation warnings
- [ ] Update code patterns
- [ ] Keep detailed notes

### After Migration
- [ ] All tests pass
- [ ] App builds for all platforms
- [ ] Manual testing complete
- [ ] Performance verified
- [ ] Document changes made
- [ ] Update team on new patterns

---

## Integration with Other Agents

- **Testing Strategy Agent**: Ensure tests during migration
- **Code Review Agent**: Review migrated code
- **Documentation Agent**: Document migration changes
- **Debugging Agent**: Fix migration issues
