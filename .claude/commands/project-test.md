---
name: project-test
description: Run tests with coverage reporting for Dart/Flutter projects
argument-hint: "[unit|widget|integration|all|--coverage]"
---

# Run Tests

Run the project's test suite with coverage reporting.

## Usage
```
/project-test [options]
```

## Arguments

- `$ARGUMENTS` - Optional: `unit`, `widget`, `integration`, `all`, or specific test path

## Workflow

1. **Analyze Test Scope**
   - Determine which tests to run
   - Check for test dependencies

2. **Run Tests**
   ```bash
   # Unit tests
   flutter test test/

   # With coverage
   flutter test --coverage

   # Specific file
   flutter test test/path/to/test.dart
   ```

3. **Report Results**
   - Show pass/fail count
   - Highlight failures
   - Show coverage percentage

4. **Handle Failures**
   - For each failure, analyze the cause
   - Suggest fixes if possible
   - Record patterns in Learning System

## Options

| Option | Description |
|--------|-------------|
| `unit` | Run unit tests only |
| `widget` | Run widget tests only |
| `integration` | Run integration tests |
| `all` | Run all tests |
| `--coverage` | Generate coverage report |

## Examples

```
# Run all tests
/project-test all

# Run with coverage
/project-test --coverage

# Run specific test
/project-test test/features/auth/auth_test.dart
```

## Coverage Thresholds

- **Minimum**: 60%
- **Target**: 80%
- **Excellent**: 90%+
