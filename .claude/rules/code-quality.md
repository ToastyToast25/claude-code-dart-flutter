# Code Quality Rules

**MANDATORY**: All agents must follow these rules. No exceptions.

---

## Rule 1: No Backward Compatibility Code

**NEVER** write code that exists solely for backward compatibility.

### Prohibited Patterns

```dart
// ❌ WRONG: Renamed unused variables
final _unusedOldValue = oldValue;

// ❌ WRONG: Comments about removed code
// removed: oldFunction()

// ❌ WRONG: Legacy comments
// legacy code - keep for compatibility

// ❌ WRONG: Backward compat exports
export 'old_file.dart'; // backward compatibility

// ❌ WRONG: Deprecated with temporary flag
@Deprecated('Temporary - remove after migration')
void oldMethod() {}

// ❌ WRONG: TODO to remove later
// TODO: remove after v2.0
void temporaryFix() {}
```

### What To Do Instead

```dart
// ✅ CORRECT: Just delete unused code
// (no trace left behind)

// ✅ CORRECT: Write the new implementation
void newMethod() {
  // Clean implementation
}

// ✅ CORRECT: Remove old exports entirely
// (nothing here - file deleted)
```

---

## Rule 2: No Dead Code

**NEVER** leave unreachable or unused code.

### Prohibited Patterns

```dart
// ❌ WRONG: Code after return
String getValue() {
  return 'value';
  print('This never runs'); // Dead code
}

// ❌ WRONG: Always-false conditions
if (false) {
  doSomething(); // Dead code
}

// ❌ WRONG: Unused private methods
void _neverCalled() {
  // This method is never used
}

// ❌ WRONG: Unreachable catch blocks
try {
  // Code that can't throw SpecificException
} on SpecificException {
  // Dead code
}
```

### What To Do Instead

```dart
// ✅ CORRECT: Remove everything after return
String getValue() {
  return 'value';
}

// ✅ CORRECT: Delete unused methods entirely

// ✅ CORRECT: Only catch exceptions that can occur
```

---

## Rule 3: No Unresolved TODOs

**NEVER** commit code with unresolved TODO/FIXME comments.

### Prohibited Patterns

```dart
// ❌ WRONG: Unresolved TODO
// TODO: implement this later
void doSomething() {}

// ❌ WRONG: FIXME without fix
// FIXME: this is broken
int calculate() => 0;

// ❌ WRONG: HACK comment
// HACK: workaround for now
```

### What To Do Instead

```dart
// ✅ CORRECT: Implement it now or don't write it
void doSomething() {
  // Actual implementation
}

// ✅ CORRECT: Fix it now
int calculate() {
  return performCorrectCalculation();
}
```

---

## Rule 4: No Commented-Out Code

**NEVER** leave commented-out code blocks.

### Prohibited Patterns

```dart
// ❌ WRONG: Commented implementation
// void oldMethod() {
//   doOldThing();
// }

// ❌ WRONG: Commented imports
// import 'package:old_package/old_package.dart';

// ❌ WRONG: Commented logic
// if (condition) {
//   doSomething();
// }
```

### What To Do Instead

```dart
// ✅ CORRECT: Delete commented code entirely
// Use version control (git) for history

// ✅ CORRECT: Write only active code
void currentMethod() {
  doCurrentThing();
}
```

---

## Rule 5: No Deprecated API Usage

**NEVER** use deprecated APIs when creating new code.

### Prohibited Patterns

```dart
// ❌ WRONG: Using deprecated API
@deprecated
void oldWay() {}

void main() {
  oldWay(); // Using deprecated API
}

// ❌ WRONG: Creating new deprecated code
@Deprecated('Will be removed')
class OldClass {}
```

### What To Do Instead

```dart
// ✅ CORRECT: Use current APIs only
void currentWay() {}

void main() {
  currentWay();
}

// ✅ CORRECT: Don't create deprecated code
// If it's deprecated, don't write it
```

---

## Rule 6: No Magic Numbers

**NEVER** use unexplained numeric literals (except 0, 1, -1).

### Prohibited Patterns

```dart
// ❌ WRONG: Magic numbers
final timeout = 30000;
if (items.length > 50) {}
padding: EdgeInsets.all(16),
```

### What To Do Instead

```dart
// ✅ CORRECT: Named constants
const kApiTimeoutMs = 30000;
const kMaxItemsPerPage = 50;
const kDefaultPadding = 16.0;

final timeout = kApiTimeoutMs;
if (items.length > kMaxItemsPerPage) {}
padding: EdgeInsets.all(kDefaultPadding),
```

---

## Rule 7: No Hardcoded Strings (UI)

**NEVER** hardcode user-facing strings in UI code.

### Prohibited Patterns

```dart
// ❌ WRONG: Hardcoded strings
Text('Welcome to our app!'),
title: 'Error occurred',
hint: 'Enter your email',
```

### What To Do Instead

```dart
// ✅ CORRECT: Use localization or constants
Text(AppStrings.welcomeMessage),
title: l10n.errorTitle,
hint: Strings.emailHint,
```

---

## Rule 8: Clean Production Code Only

**ALWAYS** write code as if it's the final production version.

### Standards

1. **No debug code in commits**
   ```dart
   // ❌ WRONG
   print('DEBUG: value = $value');

   // ✅ CORRECT
   logger.debug('Processing value', {'value': value});
   ```

2. **No test credentials**
   ```dart
   // ❌ WRONG
   const apiKey = 'test-key-12345';

   // ✅ CORRECT
   final apiKey = Environment.apiKey;
   ```

3. **No placeholder implementations**
   ```dart
   // ❌ WRONG
   void processPayment() {
     // TODO: implement
     return;
   }

   // ✅ CORRECT
   void processPayment() {
     validatePaymentDetails();
     chargeCard();
     sendConfirmation();
   }
   ```

---

## Enforcement

### Before Every Commit

Run the quality checker:

```bash
./scripts/verify-quality.sh
```

### Automated Checks

All code must pass:
1. `dart analyze` with zero warnings
2. `dart format` check
3. Custom quality rules check
4. No backward compatibility patterns detected

### Failure Response

If quality check fails:
1. **Fix the issue immediately**
2. **Do not commit until fixed**
3. **Record the error in Learning System**
4. **Update patterns to prevent recurrence**

---

## Quick Reference

| Rule | Keyword | Action |
|------|---------|--------|
| No backward compat | `legacy`, `old`, `compat` | Delete |
| No dead code | Unreachable | Delete |
| No TODO/FIXME | `TODO`, `FIXME` | Implement or remove |
| No commented code | `//` blocks | Delete |
| No deprecated | `@deprecated` | Use current API |
| No magic numbers | Numeric literals | Use constants |
| No hardcoded strings | String literals | Use l10n/constants |
| Production only | Debug code | Remove |

---

## Agent Responsibility

Every agent MUST:

1. **Check own output** against these rules before presenting
2. **Fix violations** before suggesting code to user
3. **Never suggest** patterns that violate these rules
4. **Record violations** found and fixed in Learning System
5. **Run verification** before finalizing any code changes
