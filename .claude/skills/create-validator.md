---
description: "Generates form validators with common validation rules (email, password, phone)"
globs: ["lib/**/validators/*.dart", "lib/core/validators/**/*.dart"]
alwaysApply: false
---

# Create Validator Skill

Generate form and input validation classes with common validation rules.

## Trigger
- "create validator"
- "new validator"
- "form validation"
- "input validation"

## Parameters
- **name**: Validator name (e.g., "email", "password", "phone")
- **rules**: List of validation rules
- **customMessage**: Custom error messages

## Generated Code

### Validator Base

```dart
// lib/core/validators/validator.dart

/// Base validator that combines multiple validation rules
class Validator {
  final List<String? Function(String?)> _rules;

  const Validator(this._rules);

  /// Validate a value and return first error or null
  String? validate(String? value) {
    for (final rule in _rules) {
      final error = rule(value);
      if (error != null) return error;
    }
    return null;
  }

  /// Validate and return all errors
  List<String> validateAll(String? value) {
    return _rules
        .map((rule) => rule(value))
        .whereType<String>()
        .toList();
  }

  /// Check if valid (for quick boolean check)
  bool isValid(String? value) => validate(value) == null;

  /// Combine with another validator
  Validator and(Validator other) {
    return Validator([..._rules, ...other._rules]);
  }

  /// Use as FormField validator
  String? call(String? value) => validate(value);
}
```

### Validation Rules

```dart
// lib/core/validators/rules.dart

/// Collection of reusable validation rules
class Rules {
  Rules._();

  /// Field is required
  static String? Function(String?) required([String? message]) {
    return (value) {
      if (value == null || value.trim().isEmpty) {
        return message ?? 'This field is required';
      }
      return null;
    };
  }

  /// Minimum length
  static String? Function(String?) minLength(int length, [String? message]) {
    return (value) {
      if (value != null && value.length < length) {
        return message ?? 'Must be at least $length characters';
      }
      return null;
    };
  }

  /// Maximum length
  static String? Function(String?) maxLength(int length, [String? message]) {
    return (value) {
      if (value != null && value.length > length) {
        return message ?? 'Must be at most $length characters';
      }
      return null;
    };
  }

  /// Exact length
  static String? Function(String?) exactLength(int length, [String? message]) {
    return (value) {
      if (value != null && value.length != length) {
        return message ?? 'Must be exactly $length characters';
      }
      return null;
    };
  }

  /// Valid email format
  static String? Function(String?) email([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      final regex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
      if (!regex.hasMatch(value)) {
        return message ?? 'Please enter a valid email';
      }
      return null;
    };
  }

  /// Valid phone number
  static String? Function(String?) phone([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      final cleaned = value.replaceAll(RegExp(r'[\s\-\(\)]'), '');
      final regex = RegExp(r'^\+?[0-9]{10,15}$');
      if (!regex.hasMatch(cleaned)) {
        return message ?? 'Please enter a valid phone number';
      }
      return null;
    };
  }

  /// Valid URL
  static String? Function(String?) url([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      final uri = Uri.tryParse(value);
      if (uri == null || !uri.hasScheme || !uri.hasAuthority) {
        return message ?? 'Please enter a valid URL';
      }
      return null;
    };
  }

  /// Numeric only
  static String? Function(String?) numeric([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      if (double.tryParse(value) == null) {
        return message ?? 'Please enter a valid number';
      }
      return null;
    };
  }

  /// Integer only
  static String? Function(String?) integer([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      if (int.tryParse(value) == null) {
        return message ?? 'Please enter a whole number';
      }
      return null;
    };
  }

  /// Minimum value (numeric)
  static String? Function(String?) min(num minValue, [String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      final number = num.tryParse(value);
      if (number == null || number < minValue) {
        return message ?? 'Must be at least $minValue';
      }
      return null;
    };
  }

  /// Maximum value (numeric)
  static String? Function(String?) max(num maxValue, [String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      final number = num.tryParse(value);
      if (number == null || number > maxValue) {
        return message ?? 'Must be at most $maxValue';
      }
      return null;
    };
  }

  /// Range (numeric)
  static String? Function(String?) range(num minVal, num maxVal, [String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      final number = num.tryParse(value);
      if (number == null || number < minVal || number > maxVal) {
        return message ?? 'Must be between $minVal and $maxVal';
      }
      return null;
    };
  }

  /// Matches regex pattern
  static String? Function(String?) pattern(RegExp regex, [String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      if (!regex.hasMatch(value)) {
        return message ?? 'Invalid format';
      }
      return null;
    };
  }

  /// Matches another field
  static String? Function(String?) matches(String? other, [String? message]) {
    return (value) {
      if (value != other) {
        return message ?? 'Fields do not match';
      }
      return null;
    };
  }

  /// Contains uppercase
  static String? Function(String?) hasUppercase([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      if (!value.contains(RegExp(r'[A-Z]'))) {
        return message ?? 'Must contain at least one uppercase letter';
      }
      return null;
    };
  }

  /// Contains lowercase
  static String? Function(String?) hasLowercase([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      if (!value.contains(RegExp(r'[a-z]'))) {
        return message ?? 'Must contain at least one lowercase letter';
      }
      return null;
    };
  }

  /// Contains digit
  static String? Function(String?) hasDigit([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      if (!value.contains(RegExp(r'[0-9]'))) {
        return message ?? 'Must contain at least one number';
      }
      return null;
    };
  }

  /// Contains special character
  static String? Function(String?) hasSpecialChar([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      if (!value.contains(RegExp(r'[!@#$%^&*(),.?":{}|<>]'))) {
        return message ?? 'Must contain at least one special character';
      }
      return null;
    };
  }

  /// No whitespace
  static String? Function(String?) noWhitespace([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      if (value.contains(RegExp(r'\s'))) {
        return message ?? 'Must not contain spaces';
      }
      return null;
    };
  }

  /// Alphanumeric only
  static String? Function(String?) alphanumeric([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      if (!RegExp(r'^[a-zA-Z0-9]+$').hasMatch(value)) {
        return message ?? 'Must contain only letters and numbers';
      }
      return null;
    };
  }

  /// Letters only
  static String? Function(String?) lettersOnly([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;
      if (!RegExp(r'^[a-zA-Z]+$').hasMatch(value)) {
        return message ?? 'Must contain only letters';
      }
      return null;
    };
  }

  /// Custom validation
  static String? Function(String?) custom(
    bool Function(String?) validator,
    String message,
  ) {
    return (value) {
      if (!validator(value)) {
        return message;
      }
      return null;
    };
  }
}
```

### Pre-built Validators

```dart
// lib/core/validators/validators.dart
import 'validator.dart';
import 'rules.dart';

/// Pre-built validators for common use cases
class Validators {
  Validators._();

  /// Email validator
  static Validator email({
    bool required = true,
    String? requiredMessage,
    String? invalidMessage,
  }) {
    return Validator([
      if (required) Rules.required(requiredMessage),
      Rules.email(invalidMessage),
    ]);
  }

  /// Password validator with strength requirements
  static Validator password({
    bool required = true,
    int minLength = 8,
    bool requireUppercase = true,
    bool requireLowercase = true,
    bool requireDigit = true,
    bool requireSpecialChar = false,
    String? requiredMessage,
  }) {
    return Validator([
      if (required) Rules.required(requiredMessage ?? 'Password is required'),
      Rules.minLength(minLength, 'Password must be at least $minLength characters'),
      if (requireUppercase) Rules.hasUppercase('Must contain an uppercase letter'),
      if (requireLowercase) Rules.hasLowercase('Must contain a lowercase letter'),
      if (requireDigit) Rules.hasDigit('Must contain a number'),
      if (requireSpecialChar) Rules.hasSpecialChar('Must contain a special character'),
    ]);
  }

  /// Password confirmation validator
  static Validator confirmPassword(String? password, {String? message}) {
    return Validator([
      Rules.required('Please confirm your password'),
      Rules.matches(password, message ?? 'Passwords do not match'),
    ]);
  }

  /// Username validator
  static Validator username({
    bool required = true,
    int minLength = 3,
    int maxLength = 20,
  }) {
    return Validator([
      if (required) Rules.required('Username is required'),
      Rules.minLength(minLength, 'Username must be at least $minLength characters'),
      Rules.maxLength(maxLength, 'Username must be at most $maxLength characters'),
      Rules.alphanumeric('Username can only contain letters and numbers'),
    ]);
  }

  /// Name validator
  static Validator name({
    bool required = true,
    int minLength = 2,
    int maxLength = 50,
  }) {
    return Validator([
      if (required) Rules.required('Name is required'),
      Rules.minLength(minLength),
      Rules.maxLength(maxLength),
      Rules.lettersOnly('Name can only contain letters'),
    ]);
  }

  /// Phone number validator
  static Validator phone({bool required = false}) {
    return Validator([
      if (required) Rules.required('Phone number is required'),
      Rules.phone(),
    ]);
  }

  /// URL validator
  static Validator url({bool required = false}) {
    return Validator([
      if (required) Rules.required('URL is required'),
      Rules.url(),
    ]);
  }

  /// Numeric field validator
  static Validator number({
    bool required = false,
    num? min,
    num? max,
    bool integer = false,
  }) {
    return Validator([
      if (required) Rules.required('This field is required'),
      integer ? Rules.integer() : Rules.numeric(),
      if (min != null) Rules.min(min),
      if (max != null) Rules.max(max),
    ]);
  }

  /// Credit card number validator
  static Validator creditCard({bool required = true}) {
    return Validator([
      if (required) Rules.required('Card number is required'),
      Rules.pattern(
        RegExp(r'^[0-9]{13,19}$'),
        'Please enter a valid card number',
      ),
      Rules.custom(_luhnCheck, 'Invalid card number'),
    ]);
  }

  /// CVV validator
  static Validator cvv({bool required = true}) {
    return Validator([
      if (required) Rules.required('CVV is required'),
      Rules.pattern(
        RegExp(r'^[0-9]{3,4}$'),
        'CVV must be 3 or 4 digits',
      ),
    ]);
  }

  /// Expiry date validator (MM/YY format)
  static Validator expiryDate({bool required = true}) {
    return Validator([
      if (required) Rules.required('Expiry date is required'),
      Rules.pattern(
        RegExp(r'^(0[1-9]|1[0-2])\/([0-9]{2})$'),
        'Please enter a valid expiry date (MM/YY)',
      ),
      Rules.custom(_isNotExpired, 'Card has expired'),
    ]);
  }

  /// Zip/Postal code validator
  static Validator zipCode({bool required = false, String country = 'US'}) {
    final patterns = {
      'US': RegExp(r'^\d{5}(-\d{4})?$'),
      'UK': RegExp(r'^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$', caseSensitive: false),
      'CA': RegExp(r'^[A-Z]\d[A-Z] ?\d[A-Z]\d$', caseSensitive: false),
    };

    return Validator([
      if (required) Rules.required('Zip code is required'),
      Rules.pattern(
        patterns[country] ?? patterns['US']!,
        'Please enter a valid zip code',
      ),
    ]);
  }

  // Helper: Luhn algorithm for credit card validation
  static bool _luhnCheck(String? value) {
    if (value == null || value.isEmpty) return true;
    final digits = value.replaceAll(RegExp(r'\D'), '');
    if (digits.length < 13) return false;

    int sum = 0;
    bool alternate = false;

    for (int i = digits.length - 1; i >= 0; i--) {
      int digit = int.parse(digits[i]);
      if (alternate) {
        digit *= 2;
        if (digit > 9) digit -= 9;
      }
      sum += digit;
      alternate = !alternate;
    }

    return sum % 10 == 0;
  }

  // Helper: Check if expiry date is not expired
  static bool _isNotExpired(String? value) {
    if (value == null || value.isEmpty) return true;
    final parts = value.split('/');
    if (parts.length != 2) return false;

    final month = int.tryParse(parts[0]);
    final year = int.tryParse('20${parts[1]}');
    if (month == null || year == null) return false;

    final now = DateTime.now();
    final expiry = DateTime(year, month + 1, 0);

    return expiry.isAfter(now);
  }
}
```

### Usage in Forms

```dart
// Example usage in a form
class LoginForm extends StatelessWidget {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            controller: _emailController,
            decoration: const InputDecoration(labelText: 'Email'),
            validator: Validators.email().validate,
            keyboardType: TextInputType.emailAddress,
          ),
          TextFormField(
            controller: _passwordController,
            decoration: const InputDecoration(labelText: 'Password'),
            validator: Validators.password().validate,
            obscureText: true,
          ),
          ElevatedButton(
            onPressed: () {
              if (_formKey.currentState!.validate()) {
                // Form is valid, proceed
              }
            },
            child: const Text('Sign In'),
          ),
        ],
      ),
    );
  }
}

// Example with custom validator
final customValidator = Validator([
  Rules.required('Username is required'),
  Rules.minLength(3),
  Rules.maxLength(20),
  Rules.pattern(
    RegExp(r'^[a-z][a-z0-9_]*$'),
    'Must start with a letter and contain only lowercase letters, numbers, and underscores',
  ),
  Rules.custom(
    (value) async {
      // Could check if username is available
      return true;
    },
    'Username is already taken',
  ),
]);
```

### Real-time Validation Widget

```dart
// lib/shared/widgets/validated_text_field.dart
import 'package:flutter/material.dart';
import '../../core/validators/validator.dart';

class ValidatedTextField extends StatefulWidget {
  final TextEditingController? controller;
  final Validator validator;
  final String label;
  final bool validateOnChange;
  final bool obscureText;
  final TextInputType? keyboardType;
  final void Function(String)? onChanged;

  const ValidatedTextField({
    super.key,
    this.controller,
    required this.validator,
    required this.label,
    this.validateOnChange = true,
    this.obscureText = false,
    this.keyboardType,
    this.onChanged,
  });

  @override
  State<ValidatedTextField> createState() => _ValidatedTextFieldState();
}

class _ValidatedTextFieldState extends State<ValidatedTextField> {
  late TextEditingController _controller;
  String? _error;
  bool _touched = false;

  @override
  void initState() {
    super.initState();
    _controller = widget.controller ?? TextEditingController();
  }

  void _validate(String value) {
    if (!_touched) return;
    setState(() {
      _error = widget.validator.validate(value);
    });
  }

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: _controller,
      decoration: InputDecoration(
        labelText: widget.label,
        errorText: _error,
        suffixIcon: _error == null && _touched
            ? const Icon(Icons.check, color: Colors.green)
            : null,
      ),
      obscureText: widget.obscureText,
      keyboardType: widget.keyboardType,
      onChanged: (value) {
        if (widget.validateOnChange) {
          _validate(value);
        }
        widget.onChanged?.call(value);
      },
      onTap: () {
        if (!_touched) {
          setState(() => _touched = true);
        }
      },
      validator: (value) {
        _touched = true;
        return widget.validator.validate(value);
      },
    );
  }
}
```

---

## Security-Focused Validation

### Prevent Injection Attacks

```dart
// lib/core/validators/security_rules.dart

/// Security-focused validation rules
class SecurityRules {
  SecurityRules._();

  /// Block potential SQL injection patterns
  static String? Function(String?) noSqlInjection([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;

      final patterns = [
        RegExp(r"['\";]--", caseSensitive: false),
        RegExp(r'\b(union|select|insert|update|delete|drop|truncate)\b', caseSensitive: false),
        RegExp(r'\b(or|and)\s+\d+\s*=\s*\d+', caseSensitive: false),
      ];

      for (final pattern in patterns) {
        if (pattern.hasMatch(value)) {
          return message ?? 'Invalid characters detected';
        }
      }
      return null;
    };
  }

  /// Block potential XSS patterns
  static String? Function(String?) noXss([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;

      final patterns = [
        RegExp(r'<script', caseSensitive: false),
        RegExp(r'javascript:', caseSensitive: false),
        RegExp(r'on\w+\s*=', caseSensitive: false), // onclick, onerror, etc.
        RegExp(r'<iframe', caseSensitive: false),
        RegExp(r'<object', caseSensitive: false),
        RegExp(r'<embed', caseSensitive: false),
      ];

      for (final pattern in patterns) {
        if (pattern.hasMatch(value)) {
          return message ?? 'Invalid content detected';
        }
      }
      return null;
    };
  }

  /// Block shell command characters
  static String? Function(String?) noShellChars([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;

      if (RegExp(r'[;&|`$(){}[\]<>!\n\r]').hasMatch(value)) {
        return message ?? 'Invalid characters detected';
      }
      return null;
    };
  }

  /// Block path traversal attempts
  static String? Function(String?) noPathTraversal([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;

      if (value.contains('..') || value.contains('\x00')) {
        return message ?? 'Invalid path characters';
      }
      return null;
    };
  }

  /// Validate UUID format strictly
  static String? Function(String?) uuid([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;

      final regex = RegExp(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
        caseSensitive: false,
      );

      if (!regex.hasMatch(value)) {
        return message ?? 'Invalid ID format';
      }
      return null;
    };
  }

  /// Validate safe URL (no javascript:, data:, file:)
  static String? Function(String?) safeUrl([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;

      final uri = Uri.tryParse(value);
      if (uri == null) {
        return message ?? 'Invalid URL';
      }

      final blockedSchemes = ['javascript', 'data', 'file', 'vbscript'];
      if (blockedSchemes.contains(uri.scheme.toLowerCase())) {
        return message ?? 'URL scheme not allowed';
      }

      return null;
    };
  }

  /// Enforce HTTPS only
  static String? Function(String?) httpsOnly([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;

      final uri = Uri.tryParse(value);
      if (uri == null || uri.scheme.toLowerCase() != 'https') {
        return message ?? 'URL must use HTTPS';
      }

      return null;
    };
  }

  /// Block private/internal IPs in URLs
  static String? Function(String?) noPrivateUrls([String? message]) {
    return (value) {
      if (value == null || value.isEmpty) return null;

      final uri = Uri.tryParse(value);
      if (uri == null) return message ?? 'Invalid URL';

      final host = uri.host.toLowerCase();

      // Block localhost
      if (host == 'localhost' || host == '127.0.0.1' || host == '::1') {
        return message ?? 'Internal URLs not allowed';
      }

      // Block private IP ranges
      final privatePatterns = [
        RegExp(r'^10\.'),
        RegExp(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.'),
        RegExp(r'^192\.168\.'),
        RegExp(r'^169\.254\.'), // Link-local
      ];

      for (final pattern in privatePatterns) {
        if (pattern.hasMatch(host)) {
          return message ?? 'Internal URLs not allowed';
        }
      }

      return null;
    };
  }
}
```

### Secure Form Validators

```dart
/// Secure pre-built validators
class SecureValidators {
  SecureValidators._();

  /// Secure username - alphanumeric only, no injection
  static Validator username({
    bool required = true,
    int minLength = 3,
    int maxLength = 30,
  }) {
    return Validator([
      if (required) Rules.required('Username is required'),
      Rules.minLength(minLength),
      Rules.maxLength(maxLength),
      Rules.alphanumeric('Username can only contain letters and numbers'),
      SecurityRules.noSqlInjection(),
      SecurityRules.noXss(),
    ]);
  }

  /// Secure search query - limited length, no injection
  static Validator searchQuery({int maxLength = 100}) {
    return Validator([
      Rules.maxLength(maxLength, 'Search query too long'),
      SecurityRules.noSqlInjection(),
      SecurityRules.noXss(),
    ]);
  }

  /// Secure file name
  static Validator filename() {
    return Validator([
      Rules.required('Filename is required'),
      Rules.maxLength(255),
      SecurityRules.noPathTraversal(),
      SecurityRules.noShellChars(),
      Rules.pattern(
        RegExp(r'^[a-zA-Z0-9._-]+$'),
        'Filename contains invalid characters',
      ),
    ]);
  }

  /// Secure URL input
  static Validator url({bool httpsRequired = false}) {
    return Validator([
      Rules.url(),
      SecurityRules.safeUrl(),
      SecurityRules.noPrivateUrls(),
      if (httpsRequired) SecurityRules.httpsOnly(),
    ]);
  }

  /// Secure ID parameter
  static Validator id() {
    return Validator([
      Rules.required('ID is required'),
      SecurityRules.uuid(),
    ]);
  }

  /// Secure comment/text area
  static Validator comment({int maxLength = 5000}) {
    return Validator([
      Rules.maxLength(maxLength),
      SecurityRules.noXss(),
    ]);
  }
}
```

---

## Usage Examples

```
User: create validator for email
User: create validator for password with special characters
User: create validator for credit card
User: create custom validator for username
User: create secure validator for search input
User: add xss protection to form validation
```
