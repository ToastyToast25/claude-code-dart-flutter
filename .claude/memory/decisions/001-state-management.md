# ADR-001: State Management Choice

**Date**: 2026-01-21
**Status**: Accepted
**Author**: Claude Code System

## Context

The project needs a state management solution that:
- Is type-safe at compile time
- Supports dependency injection
- Is easily testable
- Doesn't require BuildContext for access
- Scales well with app complexity
- Has good community support and documentation

## Options Considered

### 1. Provider
**Pros:**
- Simple API
- Official Flutter recommendation
- Low learning curve

**Cons:**
- Requires BuildContext
- Not compile-time safe
- Verbose for complex state

### 2. Riverpod
**Pros:**
- Compile-time safe
- No BuildContext requirement
- Excellent testing support
- Code generation available
- Clear separation of concerns

**Cons:**
- Steeper learning curve
- Different patterns from Provider

### 3. BLoC
**Pros:**
- Event-driven, predictable
- Great for complex business logic
- Excellent debugging (event tracking)

**Cons:**
- More boilerplate
- Can be overkill for simple state

### 4. GetX
**Pros:**
- Very simple API
- All-in-one solution

**Cons:**
- Magic/implicit behavior
- Less testable
- Anti-patterns common

## Decision

**Use Riverpod as the primary state management solution.**

Use BLoC for features with complex event-driven logic where event tracking/replay is beneficial.

## Rationale

1. **Compile-time safety** prevents runtime errors from missing providers
2. **No BuildContext** allows business logic to be completely separated from UI
3. **Testing** is straightforward with `ProviderContainer`
4. **Code generation** reduces boilerplate with `riverpod_generator`
5. **Community** is active and growing
6. **Flexibility** to use BLoC where appropriate (they can coexist)

## Consequences

### Positive
- Type-safe provider access
- Easy unit testing of providers
- Clear provider dependencies
- IDE autocomplete works well

### Negative
- Team needs to learn Riverpod patterns
- Some migration effort if using Provider
- Two state management solutions (Riverpod + BLoC) requires guidelines

## Implementation

```dart
// Use Riverpod for most state
final userProvider = FutureProvider((ref) async {
  return ref.watch(userRepositoryProvider).getCurrentUser();
});

// Use BLoC for complex event-driven features
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  // When event tracking/replay is valuable
}
```

## Guidelines

1. **Default to Riverpod** for:
   - Simple state (counters, flags)
   - API data fetching
   - Form state
   - App-wide state (auth, settings)

2. **Use BLoC** for:
   - Complex multi-step flows
   - Features requiring event logging
   - When event replay is useful for debugging

## Review Date

Revisit in 6 months or when major issues arise.

---

*This decision applies to all features in this project.*
