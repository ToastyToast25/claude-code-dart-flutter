---
description: "Scaffolds a complete feature module with data, domain, and presentation layers"
globs: ["lib/features/**/*.dart"]
alwaysApply: false
---

# Create Feature Skill

Generate a complete feature module with all layers following clean architecture.

## Trigger
- "create feature"
- "new feature"
- "scaffold feature"
- "generate feature"

## Parameters
- **name**: Feature name (e.g., "auth", "products", "orders")
- **entities**: List of entities for this feature
- **hasApi**: Whether feature needs API integration (default: true)
- **stateManagement**: bloc, cubit, riverpod, provider (default: bloc)

## Output Structure

```
lib/features/{name}/
├── data/
│   ├── datasources/
│   │   ├── {name}_local_datasource.dart
│   │   └── {name}_remote_datasource.dart
│   ├── models/
│   │   └── {entity}_model.dart
│   └── repositories/
│       └── {name}_repository_impl.dart
├── domain/
│   ├── entities/
│   │   └── {entity}.dart
│   ├── repositories/
│   │   └── {name}_repository.dart
│   └── usecases/
│       └── get_{entity}.dart
└── presentation/
    ├── bloc/
    │   ├── {name}_bloc.dart
    │   ├── {name}_event.dart
    │   └── {name}_state.dart
    ├── pages/
    │   └── {name}_page.dart
    └── widgets/
        └── {name}_widget.dart
```

## Generated Code

### Domain Layer

**Entity**
```dart
// lib/features/{name}/domain/entities/{entity}.dart
import 'package:equatable/equatable.dart';

class {Entity} extends Equatable {
  final String id;
  final String name;
  final DateTime createdAt;

  const {Entity}({
    required this.id,
    required this.name,
    required this.createdAt,
  });

  @override
  List<Object?> get props => [id, name, createdAt];
}
```

**Repository Interface**
```dart
// lib/features/{name}/domain/repositories/{name}_repository.dart
import 'package:fpdart/fpdart.dart';
import '../../../../core/error/failures.dart';
import '../entities/{entity}.dart';

abstract class {Name}Repository {
  Future<Either<Failure, List<{Entity}>>> getAll();
  Future<Either<Failure, {Entity}>> getById(String id);
  Future<Either<Failure, {Entity}>> create({Entity} entity);
  Future<Either<Failure, {Entity}>> update({Entity} entity);
  Future<Either<Failure, void>> delete(String id);
}
```

**Use Case**
```dart
// lib/features/{name}/domain/usecases/get_{entity}.dart
import 'package:fpdart/fpdart.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/{entity}.dart';
import '../repositories/{name}_repository.dart';

class Get{Entity} implements UseCase<{Entity}, String> {
  final {Name}Repository repository;

  Get{Entity}(this.repository);

  @override
  Future<Either<Failure, {Entity}>> call(String id) {
    return repository.getById(id);
  }
}

class GetAll{Entity}s implements UseCase<List<{Entity}>, NoParams> {
  final {Name}Repository repository;

  GetAll{Entity}s(this.repository);

  @override
  Future<Either<Failure, List<{Entity}>>> call(NoParams params) {
    return repository.getAll();
  }
}
```

### Data Layer

**Model**
```dart
// lib/features/{name}/data/models/{entity}_model.dart
import '../../domain/entities/{entity}.dart';

class {Entity}Model extends {Entity} {
  const {Entity}Model({
    required super.id,
    required super.name,
    required super.createdAt,
  });

  factory {Entity}Model.fromJson(Map<String, dynamic> json) {
    return {Entity}Model(
      id: json['id'] as String,
      name: json['name'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'created_at': createdAt.toIso8601String(),
  };

  factory {Entity}Model.fromEntity({Entity} entity) {
    return {Entity}Model(
      id: entity.id,
      name: entity.name,
      createdAt: entity.createdAt,
    );
  }
}
```

**Remote Data Source**
```dart
// lib/features/{name}/data/datasources/{name}_remote_datasource.dart
import '../../../../core/network/api_client.dart';
import '../models/{entity}_model.dart';

abstract class {Name}RemoteDataSource {
  Future<List<{Entity}Model>> getAll();
  Future<{Entity}Model> getById(String id);
  Future<{Entity}Model> create({Entity}Model model);
  Future<{Entity}Model> update({Entity}Model model);
  Future<void> delete(String id);
}

class {Name}RemoteDataSourceImpl implements {Name}RemoteDataSource {
  final ApiClient _client;
  static const _basePath = '/{name}s';

  {Name}RemoteDataSourceImpl(this._client);

  @override
  Future<List<{Entity}Model>> getAll() async {
    final response = await _client.get(_basePath);
    return (response as List)
        .map((json) => {Entity}Model.fromJson(json))
        .toList();
  }

  @override
  Future<{Entity}Model> getById(String id) async {
    final response = await _client.get('$_basePath/$id');
    return {Entity}Model.fromJson(response);
  }

  @override
  Future<{Entity}Model> create({Entity}Model model) async {
    final response = await _client.post(_basePath, body: model.toJson());
    return {Entity}Model.fromJson(response);
  }

  @override
  Future<{Entity}Model> update({Entity}Model model) async {
    final response = await _client.put(
      '$_basePath/${model.id}',
      body: model.toJson(),
    );
    return {Entity}Model.fromJson(response);
  }

  @override
  Future<void> delete(String id) async {
    await _client.delete('$_basePath/$id');
  }
}
```

**Local Data Source**
```dart
// lib/features/{name}/data/datasources/{name}_local_datasource.dart
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/{entity}_model.dart';

abstract class {Name}LocalDataSource {
  Future<List<{Entity}Model>> getCached();
  Future<void> cache(List<{Entity}Model> models);
  Future<void> clear();
}

class {Name}LocalDataSourceImpl implements {Name}LocalDataSource {
  final SharedPreferences _prefs;
  static const _cacheKey = 'cached_{name}s';

  {Name}LocalDataSourceImpl(this._prefs);

  @override
  Future<List<{Entity}Model>> getCached() async {
    final jsonString = _prefs.getString(_cacheKey);
    if (jsonString == null) return [];

    final jsonList = jsonDecode(jsonString) as List;
    return jsonList
        .map((json) => {Entity}Model.fromJson(json))
        .toList();
  }

  @override
  Future<void> cache(List<{Entity}Model> models) async {
    final jsonList = models.map((m) => m.toJson()).toList();
    await _prefs.setString(_cacheKey, jsonEncode(jsonList));
  }

  @override
  Future<void> clear() async {
    await _prefs.remove(_cacheKey);
  }
}
```

**Repository Implementation**
```dart
// lib/features/{name}/data/repositories/{name}_repository_impl.dart
import 'package:fpdart/fpdart.dart';
import '../../../../core/error/exceptions.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/network/network_info.dart';
import '../../domain/entities/{entity}.dart';
import '../../domain/repositories/{name}_repository.dart';
import '../datasources/{name}_local_datasource.dart';
import '../datasources/{name}_remote_datasource.dart';
import '../models/{entity}_model.dart';

class {Name}RepositoryImpl implements {Name}Repository {
  final {Name}RemoteDataSource remoteDataSource;
  final {Name}LocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  {Name}RepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, List<{Entity}>>> getAll() async {
    if (await networkInfo.isConnected) {
      try {
        final models = await remoteDataSource.getAll();
        await localDataSource.cache(models);
        return Right(models);
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    } else {
      try {
        final cached = await localDataSource.getCached();
        return Right(cached);
      } on CacheException catch (e) {
        return Left(CacheFailure(e.message));
      }
    }
  }

  @override
  Future<Either<Failure, {Entity}>> getById(String id) async {
    try {
      final model = await remoteDataSource.getById(id);
      return Right(model);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    }
  }

  @override
  Future<Either<Failure, {Entity}>> create({Entity} entity) async {
    try {
      final model = {Entity}Model.fromEntity(entity);
      final created = await remoteDataSource.create(model);
      return Right(created);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    }
  }

  @override
  Future<Either<Failure, {Entity}>> update({Entity} entity) async {
    try {
      final model = {Entity}Model.fromEntity(entity);
      final updated = await remoteDataSource.update(model);
      return Right(updated);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    }
  }

  @override
  Future<Either<Failure, void>> delete(String id) async {
    try {
      await remoteDataSource.delete(id);
      return const Right(null);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    }
  }
}
```

### Presentation Layer

**BLoC**
```dart
// lib/features/{name}/presentation/bloc/{name}_bloc.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';
import '../../../../core/usecases/usecase.dart';
import '../../domain/entities/{entity}.dart';
import '../../domain/usecases/get_{entity}.dart';

part '{name}_event.dart';
part '{name}_state.dart';

class {Name}Bloc extends Bloc<{Name}Event, {Name}State> {
  final GetAll{Entity}s getAll{Entity}s;
  final Get{Entity} get{Entity};

  {Name}Bloc({
    required this.getAll{Entity}s,
    required this.get{Entity},
  }) : super(const {Name}Initial()) {
    on<{Name}LoadAll>(_onLoadAll);
    on<{Name}LoadOne>(_onLoadOne);
    on<{Name}Refresh>(_onRefresh);
  }

  Future<void> _onLoadAll(
    {Name}LoadAll event,
    Emitter<{Name}State> emit,
  ) async {
    emit(const {Name}Loading());

    final result = await getAll{Entity}s(const NoParams());

    result.fold(
      (failure) => emit({Name}Error(failure.message)),
      (entities) => emit({Name}Loaded(entities)),
    );
  }

  Future<void> _onLoadOne(
    {Name}LoadOne event,
    Emitter<{Name}State> emit,
  ) async {
    emit(const {Name}Loading());

    final result = await get{Entity}(event.id);

    result.fold(
      (failure) => emit({Name}Error(failure.message)),
      (entity) => emit({Name}DetailLoaded(entity)),
    );
  }

  Future<void> _onRefresh(
    {Name}Refresh event,
    Emitter<{Name}State> emit,
  ) async {
    final result = await getAll{Entity}s(const NoParams());

    result.fold(
      (failure) => emit({Name}Error(failure.message)),
      (entities) => emit({Name}Loaded(entities)),
    );
  }
}
```

**Events**
```dart
// lib/features/{name}/presentation/bloc/{name}_event.dart
part of '{name}_bloc.dart';

sealed class {Name}Event extends Equatable {
  const {Name}Event();

  @override
  List<Object?> get props => [];
}

class {Name}LoadAll extends {Name}Event {
  const {Name}LoadAll();
}

class {Name}LoadOne extends {Name}Event {
  final String id;

  const {Name}LoadOne(this.id);

  @override
  List<Object?> get props => [id];
}

class {Name}Refresh extends {Name}Event {
  const {Name}Refresh();
}
```

**States**
```dart
// lib/features/{name}/presentation/bloc/{name}_state.dart
part of '{name}_bloc.dart';

sealed class {Name}State extends Equatable {
  const {Name}State();

  @override
  List<Object?> get props => [];
}

class {Name}Initial extends {Name}State {
  const {Name}Initial();
}

class {Name}Loading extends {Name}State {
  const {Name}Loading();
}

class {Name}Loaded extends {Name}State {
  final List<{Entity}> entities;

  const {Name}Loaded(this.entities);

  @override
  List<Object?> get props => [entities];
}

class {Name}DetailLoaded extends {Name}State {
  final {Entity} entity;

  const {Name}DetailLoaded(this.entity);

  @override
  List<Object?> get props => [entity];
}

class {Name}Error extends {Name}State {
  final String message;

  const {Name}Error(this.message);

  @override
  List<Object?> get props => [message];
}
```

**Page**
```dart
// lib/features/{name}/presentation/pages/{name}_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/{name}_bloc.dart';
import '../widgets/{name}_list.dart';

class {Name}Page extends StatelessWidget {
  const {Name}Page({super.key});

  static const routeName = '/{name}';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('{Name}'),
      ),
      body: BlocBuilder<{Name}Bloc, {Name}State>(
        builder: (context, state) => switch (state) {
          {Name}Initial() => const Center(
              child: Text('Press refresh to load'),
            ),
          {Name}Loading() => const Center(
              child: CircularProgressIndicator(),
            ),
          {Name}Loaded(:final entities) => {Name}List(entities: entities),
          {Name}DetailLoaded(:final entity) => {Name}Detail(entity: entity),
          {Name}Error(:final message) => Center(
              child: Text('Error: $message'),
            ),
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          context.read<{Name}Bloc>().add(const {Name}LoadAll());
        },
        child: const Icon(Icons.refresh),
      ),
    );
  }
}
```

## Usage

```
User: create feature products with entity Product
```

Generates complete feature module with:
- Product entity
- ProductModel with JSON serialization
- ProductRepository interface and implementation
- Remote and local data sources
- GetProduct and GetAllProducts use cases
- ProductBloc with events and states
- ProductPage and widgets
