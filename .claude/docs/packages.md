# Popular Dart/Flutter Packages Reference

Quick reference for commonly used packages.

## State Management

### riverpod

```yaml
dependencies:
  flutter_riverpod: ^2.4.0
```

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Simple state
final counterProvider = StateProvider((ref) => 0);

// Async data
final userProvider = FutureProvider((ref) => fetchUser());

// Complex state
class TodoNotifier extends StateNotifier<List<Todo>> {
  TodoNotifier() : super([]);
  void add(Todo todo) => state = [...state, todo];
}
final todosProvider = StateNotifierProvider((ref) => TodoNotifier());

// Widget
class MyApp extends ConsumerWidget {
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('$count');
  }
}
```

### flutter_bloc

```yaml
dependencies:
  flutter_bloc: ^8.1.0
```

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

// Cubit (simpler)
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);
  void increment() => emit(state + 1);
}

// BLoC (event-driven)
class CounterBloc extends Bloc<CounterEvent, int> {
  CounterBloc() : super(0) {
    on<Increment>((event, emit) => emit(state + 1));
  }
}

// Widget
BlocBuilder<CounterCubit, int>(
  builder: (context, count) => Text('$count'),
)
```

## Networking

### http

```yaml
dependencies:
  http: ^1.1.0
```

```dart
import 'package:http/http.dart' as http;

final response = await http.get(Uri.parse('https://api.example.com/users'));
if (response.statusCode == 200) {
  final users = jsonDecode(response.body);
}
```

### dio

```yaml
dependencies:
  dio: ^5.3.0
```

```dart
import 'package:dio/dio.dart';

final dio = Dio(BaseOptions(baseUrl: 'https://api.example.com'));

// Interceptors
dio.interceptors.add(LogInterceptor());
dio.interceptors.add(InterceptorsWrapper(
  onRequest: (options, handler) {
    options.headers['Authorization'] = 'Bearer $token';
    handler.next(options);
  },
));

// Requests
final response = await dio.get('/users');
final user = await dio.post('/users', data: {'name': 'John'});
```

## Code Generation

### freezed

```yaml
dependencies:
  freezed_annotation: ^2.4.0

dev_dependencies:
  build_runner: ^2.4.0
  freezed: ^2.4.0
```

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    @Default(false) bool isActive,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// Run: dart run build_runner build
```

### json_serializable

```yaml
dependencies:
  json_annotation: ^4.8.0

dev_dependencies:
  build_runner: ^2.4.0
  json_serializable: ^6.7.0
```

```dart
import 'package:json_annotation/json_annotation.dart';

part 'user.g.dart';

@JsonSerializable()
class User {
  User({required this.id, required this.name, this.email});

  final String id;
  final String name;
  @JsonKey(name: 'email_address')
  final String? email;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

## Navigation

### go_router

```yaml
dependencies:
  go_router: ^12.0.0
```

```dart
import 'package:go_router/go_router.dart';

final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'users/:id',
          builder: (context, state) {
            final id = state.pathParameters['id']!;
            return UserScreen(id: id);
          },
        ),
      ],
    ),
  ],
);

// Navigate
context.go('/users/123');
context.push('/users/123');
context.pop();
```

### auto_route

```yaml
dependencies:
  auto_route: ^7.8.0

dev_dependencies:
  auto_route_generator: ^7.3.0
  build_runner: ^2.4.0
```

```dart
import 'package:auto_route/auto_route.dart';

@AutoRouterConfig()
class AppRouter extends $AppRouter {
  @override
  List<AutoRoute> get routes => [
    AutoRoute(page: HomeRoute.page, initial: true),
    AutoRoute(page: UserRoute.page, path: '/users/:id'),
  ];
}

// Screen annotation
@RoutePage()
class HomeScreen extends StatelessWidget { }

// Navigate
context.router.push(UserRoute(id: '123'));
```

## Dependency Injection

### get_it

```yaml
dependencies:
  get_it: ^7.6.0
```

```dart
import 'package:get_it/get_it.dart';

final getIt = GetIt.instance;

void setupDependencies() {
  // Singleton
  getIt.registerSingleton<ApiClient>(ApiClient());

  // Lazy singleton
  getIt.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(getIt()),
  );

  // Factory (new instance each time)
  getIt.registerFactory<LoginUseCase>(() => LoginUseCase(getIt()));
}

// Use
final repository = getIt<UserRepository>();
```

### injectable

```yaml
dependencies:
  get_it: ^7.6.0
  injectable: ^2.3.0

dev_dependencies:
  injectable_generator: ^2.4.0
  build_runner: ^2.4.0
```

```dart
import 'package:injectable/injectable.dart';

@singleton
class ApiClient {}

@lazySingleton
class UserRepository {
  UserRepository(this._apiClient);
  final ApiClient _apiClient;
}

@injectable
class LoginUseCase {
  LoginUseCase(this._repository);
  final UserRepository _repository;
}

// Configure
@InjectableInit()
void configureDependencies() => getIt.init();
```

## Testing

### mockito

```yaml
dev_dependencies:
  mockito: ^5.4.0
  build_runner: ^2.4.0
```

```dart
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([UserRepository])
import 'test.mocks.dart';

void main() {
  late MockUserRepository mockRepo;

  setUp(() {
    mockRepo = MockUserRepository();
  });

  test('should return user', () async {
    when(mockRepo.getUser('1'))
        .thenAnswer((_) async => User(id: '1', name: 'John'));

    final user = await mockRepo.getUser('1');

    expect(user.name, 'John');
    verify(mockRepo.getUser('1')).called(1);
  });
}
```

### mocktail

```yaml
dev_dependencies:
  mocktail: ^1.0.0
```

```dart
import 'package:mocktail/mocktail.dart';

class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late MockUserRepository mockRepo;

  setUp(() {
    mockRepo = MockUserRepository();
  });

  test('should return user', () async {
    when(() => mockRepo.getUser('1'))
        .thenAnswer((_) async => User(id: '1', name: 'John'));

    final user = await mockRepo.getUser('1');

    expect(user.name, 'John');
    verify(() => mockRepo.getUser('1')).called(1);
  });
}
```

## UI Components

### google_fonts

```yaml
dependencies:
  google_fonts: ^6.1.0
```

```dart
import 'package:google_fonts/google_fonts.dart';

Text(
  'Hello',
  style: GoogleFonts.roboto(fontSize: 24),
)

// Theme
ThemeData(
  textTheme: GoogleFonts.robotoTextTheme(),
)
```

### cached_network_image

```yaml
dependencies:
  cached_network_image: ^3.3.0
```

```dart
import 'package:cached_network_image/cached_network_image.dart';

CachedNetworkImage(
  imageUrl: 'https://example.com/image.jpg',
  placeholder: (context, url) => const CircularProgressIndicator(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
)
```

## Storage

### shared_preferences

```yaml
dependencies:
  shared_preferences: ^2.2.0
```

```dart
import 'package:shared_preferences/shared_preferences.dart';

final prefs = await SharedPreferences.getInstance();

// Write
await prefs.setString('name', 'John');
await prefs.setBool('isLoggedIn', true);

// Read
final name = prefs.getString('name');
final isLoggedIn = prefs.getBool('isLoggedIn') ?? false;

// Remove
await prefs.remove('name');
```

### hive

```yaml
dependencies:
  hive: ^2.2.0
  hive_flutter: ^1.1.0

dev_dependencies:
  hive_generator: ^2.0.0
  build_runner: ^2.4.0
```

```dart
import 'package:hive_flutter/hive_flutter.dart';

// Initialize
await Hive.initFlutter();

// Open box
final box = await Hive.openBox('settings');

// Write
await box.put('theme', 'dark');

// Read
final theme = box.get('theme', defaultValue: 'light');

// TypeAdapter for custom types
@HiveType(typeId: 0)
class User extends HiveObject {
  @HiveField(0)
  late String name;
}
```

## Utilities

### equatable

```yaml
dependencies:
  equatable: ^2.0.0
```

```dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  const User({required this.id, required this.name});

  final String id;
  final String name;

  @override
  List<Object?> get props => [id, name];
}

// Now User('1', 'John') == User('1', 'John')
```

### intl

```yaml
dependencies:
  intl: ^0.18.0
```

```dart
import 'package:intl/intl.dart';

// Date formatting
final formatter = DateFormat('yyyy-MM-dd');
print(formatter.format(DateTime.now()));

// Number formatting
final currency = NumberFormat.currency(symbol: '\$');
print(currency.format(1234.56)); // $1,234.56

// Plural
Intl.plural(
  count,
  zero: 'no items',
  one: 'one item',
  other: '$count items',
)
```

### collection

```yaml
dependencies:
  collection: ^1.18.0
```

```dart
import 'package:collection/collection.dart';

// firstWhereOrNull
final user = users.firstWhereOrNull((u) => u.id == id);

// groupBy
final grouped = groupBy(users, (u) => u.department);

// sortedBy
final sorted = users.sortedBy((u) => u.name);

// mapIndexed
final indexed = items.mapIndexed((i, item) => '$i: $item');
```

## Database

### orm (Prisma Dart)

```yaml
dependencies:
  orm: ^5.0.0  # Prisma Dart client

dev_dependencies:
  orm_generator: ^5.0.0
  build_runner: ^2.4.0
```

```dart
import 'package:orm/orm.dart';

// Initialize client
final prisma = PrismaClient();

// CRUD operations
// Create
final user = await prisma.user.create(
  data: UserCreateInput(
    email: 'john@example.com',
    name: 'John Doe',
  ),
);

// Read
final user = await prisma.user.findUnique(
  where: UserWhereUniqueInput(id: userId),
);

// Read with relations
final userWithPosts = await prisma.user.findUnique(
  where: UserWhereUniqueInput(id: userId),
  include: UserInclude(posts: true),
);

// Update
final updated = await prisma.user.update(
  where: UserWhereUniqueInput(id: userId),
  data: UserUpdateInput(
    name: StringFieldUpdateOperationsInput(set: 'New Name'),
  ),
);

// Delete
await prisma.user.delete(
  where: UserWhereUniqueInput(id: userId),
);

// Transactions
final result = await prisma.$transaction((tx) async {
  final user = await tx.user.create(...);
  final profile = await tx.profile.create(...);
  return user;
});
```

## Security

### flutter_secure_storage

```yaml
dependencies:
  flutter_secure_storage: ^9.0.0
```

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

const storage = FlutterSecureStorage(
  aOptions: AndroidOptions(encryptedSharedPreferences: true),
  iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock),
);

// Write
await storage.write(key: 'token', value: 'secret_token');

// Read
final token = await storage.read(key: 'token');

// Delete
await storage.delete(key: 'token');

// Delete all
await storage.deleteAll();
```

### crypto

```yaml
dependencies:
  crypto: ^3.0.0
```

```dart
import 'package:crypto/crypto.dart';
import 'dart:convert';

// SHA-256 hash
final hash = sha256.convert(utf8.encode('password')).toString();

// HMAC
final hmac = Hmac(sha256, utf8.encode('secret_key'));
final digest = hmac.convert(utf8.encode('message')).toString();

// MD5 (not for security, only checksums)
final md5Hash = md5.convert(utf8.encode('data')).toString();
```

## Authentication

### firebase_auth

```yaml
dependencies:
  firebase_auth: ^4.15.0
  firebase_core: ^2.24.0
```

```dart
import 'package:firebase_auth/firebase_auth.dart';

final auth = FirebaseAuth.instance;

// Sign up
final credential = await auth.createUserWithEmailAndPassword(
  email: email,
  password: password,
);

// Sign in
final credential = await auth.signInWithEmailAndPassword(
  email: email,
  password: password,
);

// Sign out
await auth.signOut();

// Auth state changes
auth.authStateChanges().listen((User? user) {
  if (user == null) {
    print('User signed out');
  } else {
    print('User signed in: ${user.email}');
  }
});

// Current user
final user = auth.currentUser;
```

### dart_jsonwebtoken

```yaml
dependencies:
  dart_jsonwebtoken: ^2.12.0
```

```dart
import 'package:dart_jsonwebtoken/dart_jsonwebtoken.dart';

// Create JWT
final jwt = JWT({
  'sub': userId,
  'email': email,
  'role': 'user',
});

final token = jwt.sign(
  SecretKey('your-secret-key'),
  expiresIn: Duration(hours: 1),
);

// Verify JWT
try {
  final jwt = JWT.verify(token, SecretKey('your-secret-key'));
  final payload = jwt.payload;
  print('User ID: ${payload['sub']}');
} on JWTExpiredException {
  print('Token expired');
} on JWTException catch (e) {
  print('Invalid token: ${e.message}');
}
```

## Backend/Server

### shelf

```yaml
dependencies:
  shelf: ^1.4.0
  shelf_router: ^1.1.0
```

```dart
import 'package:shelf/shelf.dart';
import 'package:shelf/shelf_io.dart' as io;
import 'package:shelf_router/shelf_router.dart';

final router = Router();

router.get('/hello', (Request request) {
  return Response.ok('Hello, World!');
});

router.get('/users/<id>', (Request request, String id) {
  return Response.ok('User: $id');
});

router.post('/users', (Request request) async {
  final body = await request.readAsString();
  return Response.ok('Created', headers: {'Content-Type': 'application/json'});
});

// Middleware
final handler = Pipeline()
    .addMiddleware(logRequests())
    .addMiddleware(corsHeaders())
    .addHandler(router);

// Start server
await io.serve(handler, 'localhost', 8080);
```

### dart_frog

```yaml
dependencies:
  dart_frog: ^1.0.0
```

```dart
// routes/index.dart
import 'package:dart_frog/dart_frog.dart';

Response onRequest(RequestContext context) {
  return Response(body: 'Hello World');
}

// routes/users/[id].dart
Response onRequest(RequestContext context, String id) {
  return Response.json({'id': id});
}

// Middleware
Handler middleware(Handler handler) {
  return (context) async {
    // Before
    final response = await handler(context);
    // After
    return response;
  };
}
```
