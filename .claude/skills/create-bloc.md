---
description: "Creates BLoC or Cubit classes for state management with events and states"
globs: ["lib/**/*_bloc.dart", "lib/**/*_cubit.dart", "lib/**/bloc/*.dart"]
alwaysApply: false
---

# Create BLoC Skill

Create a BLoC or Cubit for state management.

## Trigger Keywords
- create bloc
- new bloc
- create cubit
- add bloc
- state management bloc

---

## Cubit Template (Simpler)

Use Cubit when you don't need event tracking.

```dart
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';

part '[name]_state.dart';

/// Cubit for managing [feature] state.
class [Name]Cubit extends Cubit<[Name]State> {
  [Name]Cubit(this._repository) : super(const [Name]Initial());

  final [Repository]Repository _repository;

  Future<void> load() async {
    emit(const [Name]Loading());

    final result = await _repository.getData();

    result.fold(
      (failure) => emit([Name]Error(failure.message)),
      (data) => emit([Name]Loaded(data)),
    );
  }

  void reset() {
    emit(const [Name]Initial());
  }
}
```

### Cubit State

```dart
// [name]_state.dart
part of '[name]_cubit.dart';

sealed class [Name]State extends Equatable {
  const [Name]State();

  @override
  List<Object?> get props => [];
}

final class [Name]Initial extends [Name]State {
  const [Name]Initial();
}

final class [Name]Loading extends [Name]State {
  const [Name]Loading();
}

final class [Name]Loaded extends [Name]State {
  const [Name]Loaded(this.data);

  final [DataType] data;

  @override
  List<Object?> get props => [data];
}

final class [Name]Error extends [Name]State {
  const [Name]Error(this.message);

  final String message;

  @override
  List<Object?> get props => [message];
}
```

---

## BLoC Template (Full)

Use BLoC when you need event tracking or complex event handling.

```dart
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';

part '[name]_event.dart';
part '[name]_state.dart';

/// BLoC for managing [feature] state.
class [Name]Bloc extends Bloc<[Name]Event, [Name]State> {
  [Name]Bloc(this._repository) : super(const [Name]Initial()) {
    on<[Name]Started>(_onStarted);
    on<[Name]Loaded>(_onLoaded);
    on<[Name]Created>(_onCreated);
    on<[Name]Updated>(_onUpdated);
    on<[Name]Deleted>(_onDeleted);
  }

  final [Repository]Repository _repository;

  Future<void> _onStarted(
    [Name]Started event,
    Emitter<[Name]State> emit,
  ) async {
    emit(const [Name]Loading());

    final result = await _repository.getAll();

    result.fold(
      (failure) => emit([Name]Failure(failure.message)),
      (items) => emit([Name]Success(items)),
    );
  }

  Future<void> _onLoaded(
    [Name]Loaded event,
    Emitter<[Name]State> emit,
  ) async {
    emit(const [Name]Loading());

    final result = await _repository.getById(event.id);

    result.fold(
      (failure) => emit([Name]Failure(failure.message)),
      (item) => emit([Name]ItemLoaded(item)),
    );
  }

  Future<void> _onCreated(
    [Name]Created event,
    Emitter<[Name]State> emit,
  ) async {
    emit(const [Name]Loading());

    final result = await _repository.create(event.data);

    result.fold(
      (failure) => emit([Name]Failure(failure.message)),
      (item) {
        emit([Name]OperationSuccess('Created successfully'));
        add(const [Name]Started()); // Refresh list
      },
    );
  }

  Future<void> _onUpdated(
    [Name]Updated event,
    Emitter<[Name]State> emit,
  ) async {
    emit(const [Name]Loading());

    final result = await _repository.update(event.id, event.data);

    result.fold(
      (failure) => emit([Name]Failure(failure.message)),
      (item) {
        emit([Name]OperationSuccess('Updated successfully'));
        add(const [Name]Started()); // Refresh list
      },
    );
  }

  Future<void> _onDeleted(
    [Name]Deleted event,
    Emitter<[Name]State> emit,
  ) async {
    emit(const [Name]Loading());

    final result = await _repository.delete(event.id);

    result.fold(
      (failure) => emit([Name]Failure(failure.message)),
      (_) {
        emit([Name]OperationSuccess('Deleted successfully'));
        add(const [Name]Started()); // Refresh list
      },
    );
  }
}
```

### BLoC Events

```dart
// [name]_event.dart
part of '[name]_bloc.dart';

sealed class [Name]Event extends Equatable {
  const [Name]Event();

  @override
  List<Object?> get props => [];
}

final class [Name]Started extends [Name]Event {
  const [Name]Started();
}

final class [Name]Loaded extends [Name]Event {
  const [Name]Loaded(this.id);

  final String id;

  @override
  List<Object?> get props => [id];
}

final class [Name]Created extends [Name]Event {
  const [Name]Created(this.data);

  final CreateDto data;

  @override
  List<Object?> get props => [data];
}

final class [Name]Updated extends [Name]Event {
  const [Name]Updated(this.id, this.data);

  final String id;
  final UpdateDto data;

  @override
  List<Object?> get props => [id, data];
}

final class [Name]Deleted extends [Name]Event {
  const [Name]Deleted(this.id);

  final String id;

  @override
  List<Object?> get props => [id];
}
```

### BLoC State

```dart
// [name]_state.dart
part of '[name]_bloc.dart';

sealed class [Name]State extends Equatable {
  const [Name]State();

  @override
  List<Object?> get props => [];
}

final class [Name]Initial extends [Name]State {
  const [Name]Initial();
}

final class [Name]Loading extends [Name]State {
  const [Name]Loading();
}

final class [Name]Success extends [Name]State {
  const [Name]Success(this.items);

  final List<[Item]> items;

  @override
  List<Object?> get props => [items];
}

final class [Name]ItemLoaded extends [Name]State {
  const [Name]ItemLoaded(this.item);

  final [Item] item;

  @override
  List<Object?> get props => [item];
}

final class [Name]OperationSuccess extends [Name]State {
  const [Name]OperationSuccess(this.message);

  final String message;

  @override
  List<Object?> get props => [message];
}

final class [Name]Failure extends [Name]State {
  const [Name]Failure(this.message);

  final String message;

  @override
  List<Object?> get props => [message];
}
```

---

## Providing BLoC/Cubit

```dart
// Single BLoC
BlocProvider(
  create: (context) => [Name]Bloc(
    context.read<[Repository]Repository>(),
  )..add(const [Name]Started()),
  child: const [Name]Page(),
)

// Multiple BLoCs
MultiBlocProvider(
  providers: [
    BlocProvider(create: (context) => AuthBloc(context.read<AuthRepository>())),
    BlocProvider(create: (context) => UserBloc(context.read<UserRepository>())),
  ],
  child: const MyApp(),
)

// Lazy creation
BlocProvider(
  lazy: false, // Create immediately
  create: (context) => [Name]Bloc(),
  child: const [Name]Page(),
)
```

---

## Consuming BLoC/Cubit

### BlocBuilder

```dart
BlocBuilder<[Name]Bloc, [Name]State>(
  builder: (context, state) {
    return switch (state) {
      [Name]Initial() => const SizedBox.shrink(),
      [Name]Loading() => const CircularProgressIndicator(),
      [Name]Success(:final items) => ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, index) => ListTile(
          title: Text(items[index].name),
        ),
      ),
      [Name]Failure(:final message) => Text('Error: $message'),
      _ => const SizedBox.shrink(),
    };
  },
)
```

### BlocListener

```dart
BlocListener<[Name]Bloc, [Name]State>(
  listener: (context, state) {
    if (state is [Name]OperationSuccess) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.message)),
      );
    }
    if (state is [Name]Failure) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(state.message),
          backgroundColor: Colors.red,
        ),
      );
    }
  },
  child: const [Name]View(),
)
```

### BlocConsumer

```dart
BlocConsumer<[Name]Bloc, [Name]State>(
  listener: (context, state) {
    // Handle side effects
  },
  builder: (context, state) {
    // Build UI
    return Container();
  },
)
```

### BlocSelector

```dart
BlocSelector<[Name]Bloc, [Name]State, bool>(
  selector: (state) => state is [Name]Loading,
  builder: (context, isLoading) {
    return isLoading
        ? const CircularProgressIndicator()
        : const SizedBox.shrink();
  },
)
```

---

## File Location

```
lib/
└── features/
    └── [feature_name]/
        └── presentation/
            └── bloc/
                ├── [name]_bloc.dart
                ├── [name]_event.dart  // part of bloc
                └── [name]_state.dart  // part of bloc

            // Or for cubit:
            └── cubit/
                ├── [name]_cubit.dart
                └── [name]_state.dart  // part of cubit
```

---

## Testing

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockRepository extends Mock implements [Repository]Repository {}

void main() {
  late [Name]Bloc bloc;
  late MockRepository mockRepository;

  setUp(() {
    mockRepository = MockRepository();
    bloc = [Name]Bloc(mockRepository);
  });

  tearDown(() {
    bloc.close();
  });

  group('[Name]Bloc', () {
    test('initial state is [Name]Initial', () {
      expect(bloc.state, const [Name]Initial());
    });

    blocTest<[Name]Bloc, [Name]State>(
      'emits [Loading, Success] when Started is added',
      build: () {
        when(() => mockRepository.getAll())
            .thenAnswer((_) async => Right([testItems]));
        return bloc;
      },
      act: (bloc) => bloc.add(const [Name]Started()),
      expect: () => [
        const [Name]Loading(),
        [Name]Success([testItems]),
      ],
    );

    blocTest<[Name]Bloc, [Name]State>(
      'emits [Loading, Failure] when error occurs',
      build: () {
        when(() => mockRepository.getAll())
            .thenAnswer((_) async => Left(ServerFailure('Error')));
        return bloc;
      },
      act: (bloc) => bloc.add(const [Name]Started()),
      expect: () => [
        const [Name]Loading(),
        const [Name]Failure('Error'),
      ],
    );
  });
}
```

---

## Checklist

- [ ] Events/state extend Equatable
- [ ] States are sealed classes
- [ ] All event handlers are registered in constructor
- [ ] Repository is injected via constructor
- [ ] Error states include meaningful messages
- [ ] BlocProvider wraps the widget tree
- [ ] Tests cover success and failure cases
- [ ] No business logic in UI layer
