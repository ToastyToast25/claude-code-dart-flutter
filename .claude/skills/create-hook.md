---
description: "Creates Flutter Hooks for reusable stateful logic (flutter_hooks)"
globs: ["lib/**/hooks/*.dart", "lib/core/hooks/**/*.dart"]
alwaysApply: false
---

# Create Hook Skill

Generate Flutter Hooks for reusable stateful logic (using flutter_hooks package).

## Trigger
- "create hook"
- "new hook"
- "custom hook"
- "flutter hook"

## Parameters
- **name**: Hook name (e.g., "useAuth", "useDebounce", "useForm")
- **type**: state, lifecycle, async, animation, custom

## Dependencies Required

```yaml
dependencies:
  flutter_hooks: ^0.20.5
```

## Generated Code

### State Hook

```dart
// lib/core/hooks/use_toggle.dart
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

/// Hook for managing boolean toggle state
ToggleState useToggle([bool initialValue = false]) {
  final state = useState(initialValue);

  return ToggleState(
    value: state.value,
    toggle: () => state.value = !state.value,
    setTrue: () => state.value = true,
    setFalse: () => state.value = false,
    setValue: (value) => state.value = value,
  );
}

class ToggleState {
  final bool value;
  final VoidCallback toggle;
  final VoidCallback setTrue;
  final VoidCallback setFalse;
  final void Function(bool) setValue;

  const ToggleState({
    required this.value,
    required this.toggle,
    required this.setTrue,
    required this.setFalse,
    required this.setValue,
  });
}

// Usage:
// final dialog = useToggle();
// ElevatedButton(onPressed: dialog.toggle, child: Text('Toggle'))
// if (dialog.value) AlertDialog(...)
```

### Debounce Hook

```dart
// lib/core/hooks/use_debounce.dart
import 'dart:async';
import 'package:flutter_hooks/flutter_hooks.dart';

/// Hook for debouncing a value
T useDebounce<T>(T value, {Duration delay = const Duration(milliseconds: 500)}) {
  final debouncedValue = useState(value);

  useEffect(() {
    final timer = Timer(delay, () {
      debouncedValue.value = value;
    });

    return timer.cancel;
  }, [value, delay]);

  return debouncedValue.value;
}

/// Hook for debounced callback
void Function(T) useDebouncedCallback<T>(
  void Function(T) callback, {
  Duration delay = const Duration(milliseconds: 500),
}) {
  final timer = useRef<Timer?>(null);

  useEffect(() {
    return () => timer.value?.cancel();
  }, []);

  return (T value) {
    timer.value?.cancel();
    timer.value = Timer(delay, () => callback(value));
  };
}

// Usage:
// final searchQuery = useState('');
// final debouncedQuery = useDebounce(searchQuery.value);
// useEffect(() {
//   // This runs 500ms after user stops typing
//   searchApi(debouncedQuery);
// }, [debouncedQuery]);
```

### Form Hook

```dart
// lib/core/hooks/use_form.dart
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

/// Hook for managing form state
FormHookState useForm({
  Map<String, String> initialValues = const {},
  Map<String, String? Function(String?)>? validators,
}) {
  final formKey = useMemoized(() => GlobalKey<FormState>());
  final values = useState(Map<String, String>.from(initialValues));
  final errors = useState(<String, String?>{});
  final touched = useState(<String, bool>{});
  final isSubmitting = useState(false);

  String? getValue(String field) => values.value[field];

  void setValue(String field, String value) {
    values.value = {...values.value, field: value};
    touched.value = {...touched.value, field: true};

    // Validate on change if already touched
    if (touched.value[field] == true && validators?[field] != null) {
      errors.value = {...errors.value, field: validators![field]!(value)};
    }
  }

  String? getError(String field) => errors.value[field];

  bool isTouched(String field) => touched.value[field] ?? false;

  void setFieldTouched(String field, [bool value = true]) {
    touched.value = {...touched.value, field: value};
  }

  bool validate() {
    if (validators == null) return true;

    final newErrors = <String, String?>{};
    for (final entry in validators.entries) {
      newErrors[entry.key] = entry.value(values.value[entry.key]);
    }

    errors.value = newErrors;
    return newErrors.values.every((e) => e == null);
  }

  void reset() {
    values.value = Map.from(initialValues);
    errors.value = {};
    touched.value = {};
    formKey.currentState?.reset();
  }

  Future<void> handleSubmit(Future<void> Function(Map<String, String>) onSubmit) async {
    if (!validate()) return;

    isSubmitting.value = true;
    try {
      await onSubmit(values.value);
    } finally {
      isSubmitting.value = false;
    }
  }

  return FormHookState(
    formKey: formKey,
    values: values.value,
    errors: errors.value,
    touched: touched.value,
    isSubmitting: isSubmitting.value,
    getValue: getValue,
    setValue: setValue,
    getError: getError,
    isTouched: isTouched,
    setFieldTouched: setFieldTouched,
    validate: validate,
    reset: reset,
    handleSubmit: handleSubmit,
  );
}

class FormHookState {
  final GlobalKey<FormState> formKey;
  final Map<String, String> values;
  final Map<String, String?> errors;
  final Map<String, bool> touched;
  final bool isSubmitting;
  final String? Function(String) getValue;
  final void Function(String, String) setValue;
  final String? Function(String) getError;
  final bool Function(String) isTouched;
  final void Function(String, [bool]) setFieldTouched;
  final bool Function() validate;
  final void Function() reset;
  final Future<void> Function(Future<void> Function(Map<String, String>)) handleSubmit;

  const FormHookState({
    required this.formKey,
    required this.values,
    required this.errors,
    required this.touched,
    required this.isSubmitting,
    required this.getValue,
    required this.setValue,
    required this.getError,
    required this.isTouched,
    required this.setFieldTouched,
    required this.validate,
    required this.reset,
    required this.handleSubmit,
  });

  bool get isValid => errors.values.every((e) => e == null);
  bool get isDirty => values.isNotEmpty;
}

// Usage:
// final form = useForm(
//   initialValues: {'email': '', 'password': ''},
//   validators: {
//     'email': (v) => v?.isEmpty ?? true ? 'Email required' : null,
//     'password': (v) => (v?.length ?? 0) < 8 ? 'Min 8 characters' : null,
//   },
// );
//
// TextFormField(
//   onChanged: (v) => form.setValue('email', v),
//   decoration: InputDecoration(errorText: form.getError('email')),
// )
```

### Async Hook

```dart
// lib/core/hooks/use_async.dart
import 'package:flutter_hooks/flutter_hooks.dart';

/// Hook for managing async operations
AsyncState<T> useAsync<T>(
  Future<T> Function() asyncFunction, {
  List<Object?> keys = const [],
  bool immediate = true,
}) {
  final state = useState<AsyncState<T>>(
    immediate ? const AsyncState.loading() : const AsyncState.idle(),
  );

  final execute = useCallback(() async {
    state.value = const AsyncState.loading();
    try {
      final result = await asyncFunction();
      state.value = AsyncState.success(result);
    } catch (e, stack) {
      state.value = AsyncState.error(e, stack);
    }
  }, [asyncFunction]);

  useEffect(() {
    if (immediate) {
      execute();
    }
    return null;
  }, keys);

  return state.value.copyWith(execute: execute);
}

/// Hook for lazy async operations (triggered manually)
AsyncState<T> useAsyncCallback<T>(Future<T> Function() asyncFunction) {
  return useAsync(asyncFunction, immediate: false);
}

sealed class AsyncState<T> {
  final VoidCallback? execute;

  const AsyncState({this.execute});

  const factory AsyncState.idle({VoidCallback? execute}) = AsyncIdle<T>;
  const factory AsyncState.loading({VoidCallback? execute}) = AsyncLoading<T>;
  const factory AsyncState.success(T data, {VoidCallback? execute}) = AsyncSuccess<T>;
  const factory AsyncState.error(Object error, StackTrace? stackTrace, {VoidCallback? execute}) = AsyncError<T>;

  AsyncState<T> copyWith({VoidCallback? execute}) {
    return switch (this) {
      AsyncIdle() => AsyncIdle(execute: execute),
      AsyncLoading() => AsyncLoading(execute: execute),
      AsyncSuccess(:final data) => AsyncSuccess(data, execute: execute),
      AsyncError(:final error, :final stackTrace) => AsyncError(error, stackTrace, execute: execute),
    };
  }

  bool get isIdle => this is AsyncIdle;
  bool get isLoading => this is AsyncLoading;
  bool get isSuccess => this is AsyncSuccess;
  bool get isError => this is AsyncError;

  T? get data => switch (this) {
    AsyncSuccess(:final data) => data,
    _ => null,
  };

  Object? get error => switch (this) {
    AsyncError(:final error) => error,
    _ => null,
  };

  R when<R>({
    required R Function() idle,
    required R Function() loading,
    required R Function(T data) success,
    required R Function(Object error, StackTrace? stackTrace) error,
  }) {
    return switch (this) {
      AsyncIdle() => idle(),
      AsyncLoading() => loading(),
      AsyncSuccess(:final data) => success(data),
      AsyncError(error: final e, stackTrace: final s) => error(e, s),
    };
  }
}

class AsyncIdle<T> extends AsyncState<T> {
  const AsyncIdle({super.execute});
}

class AsyncLoading<T> extends AsyncState<T> {
  const AsyncLoading({super.execute});
}

class AsyncSuccess<T> extends AsyncState<T> {
  final T data;
  const AsyncSuccess(this.data, {super.execute});
}

class AsyncError<T> extends AsyncState<T> {
  final Object error;
  final StackTrace? stackTrace;
  const AsyncError(this.error, this.stackTrace, {super.execute});
}

// Usage:
// final users = useAsync(() => userRepository.getAll());
//
// return users.when(
//   idle: () => Text('Press button to load'),
//   loading: () => CircularProgressIndicator(),
//   success: (data) => UserList(users: data),
//   error: (e, s) => Text('Error: $e'),
// );
```

### Animation Hook

```dart
// lib/core/hooks/use_animation.dart
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

/// Hook for managing animation controller
AnimationController useAnimationControllerWithState({
  required Duration duration,
  bool autoPlay = false,
  double initialValue = 0.0,
  double lowerBound = 0.0,
  double upperBound = 1.0,
  AnimationBehavior animationBehavior = AnimationBehavior.normal,
}) {
  final controller = useAnimationController(
    duration: duration,
    initialValue: initialValue,
    lowerBound: lowerBound,
    upperBound: upperBound,
    animationBehavior: animationBehavior,
  );

  useEffect(() {
    if (autoPlay) {
      controller.forward();
    }
    return null;
  }, []);

  return controller;
}

/// Hook for fade animation
FadeAnimationState useFadeAnimation({
  Duration duration = const Duration(milliseconds: 300),
  bool initiallyVisible = true,
}) {
  final controller = useAnimationController(duration: duration);
  final animation = useMemoized(
    () => CurvedAnimation(parent: controller, curve: Curves.easeInOut),
    [controller],
  );

  useEffect(() {
    if (initiallyVisible) {
      controller.value = 1.0;
    }
    return null;
  }, []);

  return FadeAnimationState(
    animation: animation,
    fadeIn: controller.forward,
    fadeOut: controller.reverse,
    toggle: () {
      if (controller.isCompleted) {
        controller.reverse();
      } else {
        controller.forward();
      }
    },
    isVisible: controller.value > 0,
  );
}

class FadeAnimationState {
  final Animation<double> animation;
  final Future<void> Function() fadeIn;
  final Future<void> Function() fadeOut;
  final VoidCallback toggle;
  final bool isVisible;

  const FadeAnimationState({
    required this.animation,
    required this.fadeIn,
    required this.fadeOut,
    required this.toggle,
    required this.isVisible,
  });
}

/// Hook for slide animation
SlideAnimationState useSlideAnimation({
  Duration duration = const Duration(milliseconds: 300),
  Offset begin = const Offset(0, 1),
  Offset end = Offset.zero,
  Curve curve = Curves.easeInOut,
}) {
  final controller = useAnimationController(duration: duration);
  final animation = useMemoized(
    () => Tween<Offset>(begin: begin, end: end).animate(
      CurvedAnimation(parent: controller, curve: curve),
    ),
    [controller, begin, end, curve],
  );

  return SlideAnimationState(
    animation: animation,
    slideIn: controller.forward,
    slideOut: controller.reverse,
  );
}

class SlideAnimationState {
  final Animation<Offset> animation;
  final Future<void> Function() slideIn;
  final Future<void> Function() slideOut;

  const SlideAnimationState({
    required this.animation,
    required this.slideIn,
    required this.slideOut,
  });
}

// Usage:
// final fade = useFadeAnimation();
// FadeTransition(opacity: fade.animation, child: MyWidget())
// ElevatedButton(onPressed: fade.toggle, child: Text('Toggle'))
```

### Lifecycle Hook

```dart
// lib/core/hooks/use_lifecycle.dart
import 'package:flutter/widgets.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

/// Hook that runs callback on mount (like initState)
void useMount(void Function() callback) {
  useEffect(() {
    callback();
    return null;
  }, const []);
}

/// Hook that runs callback on unmount (like dispose)
void useUnmount(void Function() callback) {
  useEffect(() => callback, const []);
}

/// Hook that runs callback when dependencies change (like didUpdateWidget)
void useUpdateEffect(void Function() callback, List<Object?> keys) {
  final isFirstRun = useRef(true);

  useEffect(() {
    if (isFirstRun.value) {
      isFirstRun.value = false;
      return null;
    }
    callback();
    return null;
  }, keys);
}

/// Hook that tracks previous value
T? usePrevious<T>(T value) {
  final ref = useRef<T?>(null);

  useEffect(() {
    ref.value = value;
    return null;
  }, [value]);

  return ref.value;
}

/// Hook for app lifecycle events
void useAppLifecycle({
  VoidCallback? onResume,
  VoidCallback? onPause,
  VoidCallback? onInactive,
  VoidCallback? onDetached,
}) {
  useEffect(() {
    final observer = _LifecycleObserver(
      onResume: onResume,
      onPause: onPause,
      onInactive: onInactive,
      onDetached: onDetached,
    );

    WidgetsBinding.instance.addObserver(observer);
    return () => WidgetsBinding.instance.removeObserver(observer);
  }, []);
}

class _LifecycleObserver extends WidgetsBindingObserver {
  final VoidCallback? onResume;
  final VoidCallback? onPause;
  final VoidCallback? onInactive;
  final VoidCallback? onDetached;

  _LifecycleObserver({
    this.onResume,
    this.onPause,
    this.onInactive,
    this.onDetached,
  });

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    switch (state) {
      case AppLifecycleState.resumed:
        onResume?.call();
      case AppLifecycleState.paused:
        onPause?.call();
      case AppLifecycleState.inactive:
        onInactive?.call();
      case AppLifecycleState.detached:
        onDetached?.call();
      case AppLifecycleState.hidden:
        break;
    }
  }
}

// Usage:
// useMount(() => analytics.logScreenView('Home'));
// useUnmount(() => subscription.cancel());
// useAppLifecycle(onResume: () => refreshData());
```

### Text Editing Hook

```dart
// lib/core/hooks/use_text_editing.dart
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

/// Hook for text editing controller with useful helpers
TextEditingState useTextEditing({String initialText = ''}) {
  final controller = useTextEditingController(text: initialText);
  final focusNode = useFocusNode();
  final text = useState(initialText);

  useEffect(() {
    void listener() {
      text.value = controller.text;
    }
    controller.addListener(listener);
    return () => controller.removeListener(listener);
  }, [controller]);

  return TextEditingState(
    controller: controller,
    focusNode: focusNode,
    text: text.value,
    setText: (value) => controller.text = value,
    clear: () => controller.clear(),
    focus: () => focusNode.requestFocus(),
    unfocus: () => focusNode.unfocus(),
    isEmpty: text.value.isEmpty,
    isNotEmpty: text.value.isNotEmpty,
  );
}

class TextEditingState {
  final TextEditingController controller;
  final FocusNode focusNode;
  final String text;
  final void Function(String) setText;
  final VoidCallback clear;
  final VoidCallback focus;
  final VoidCallback unfocus;
  final bool isEmpty;
  final bool isNotEmpty;

  const TextEditingState({
    required this.controller,
    required this.focusNode,
    required this.text,
    required this.setText,
    required this.clear,
    required this.focus,
    required this.unfocus,
    required this.isEmpty,
    required this.isNotEmpty,
  });
}

// Usage:
// final search = useTextEditing();
// TextField(
//   controller: search.controller,
//   focusNode: search.focusNode,
// )
// if (search.isNotEmpty) IconButton(onPressed: search.clear, icon: Icon(Icons.clear))
```

## Usage Examples

```
User: create hook useDebounce
User: create hook useForm with validation
User: create hook useAnimation for fade effect
User: create hook useAsync for API calls
```
