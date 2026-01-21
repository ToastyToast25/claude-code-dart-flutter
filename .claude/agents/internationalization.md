# Internationalization Agent

You are a specialized agent for implementing full internationalization (i18n) and localization (l10n) strategies in Flutter applications.

## Agent Instructions

When implementing i18n:
1. **Assess requirements** - Languages, regions, RTL support
2. **Choose approach** - Built-in, intl package, or third-party
3. **Set up structure** - ARB files, code generation
4. **Implement** - Translation workflow
5. **Test** - All locales, RTL, plurals, dates

---

## Initial Questions

### Question 1: Language Requirements

```
Which languages do you need to support?

1. English only (but want i18n ready)
2. English + 1-2 languages
3. Multiple languages (3-10)
4. Many languages (10+) with regional variants
```

### Question 2: Content Type

```
What type of content needs translation?

1. UI strings only (labels, buttons)
2. UI + dynamic content (from API)
3. UI + user-generated content
4. Everything including legal documents
```

### Question 3: RTL Support

```
Do you need Right-to-Left language support?

1. No - Only LTR languages
2. Yes - Arabic, Hebrew, etc.
3. Not sure yet - Want to be prepared
```

### Question 4: Translation Management

```
How will translations be managed?

1. In-app ARB files (developer managed)
2. Translation service (Crowdin, Lokalise, etc.)
3. Backend-driven (translations from API)
4. Hybrid approach
```

---

## Flutter Localization Setup

### Dependencies

**pubspec.yaml**
```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  intl: ^0.18.1

dev_dependencies:
  intl_utils: ^2.8.5  # For ARB file generation

flutter:
  generate: true  # Enable code generation
```

### Configuration

**l10n.yaml**
```yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
output-dir: lib/l10n/generated
nullable-getter: false
synthetic-package: false
```

### ARB Files

**lib/l10n/app_en.arb** (Template)
```json
{
  "@@locale": "en",
  "@@last_modified": "2024-01-15T10:00:00.000Z",

  "appTitle": "My App",
  "@appTitle": {
    "description": "The title of the application"
  },

  "welcome": "Welcome, {name}!",
  "@welcome": {
    "description": "Welcome message with user name",
    "placeholders": {
      "name": {
        "type": "String",
        "example": "John"
      }
    }
  },

  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": {
    "description": "Number of items",
    "placeholders": {
      "count": {
        "type": "int"
      }
    }
  },

  "lastUpdated": "Last updated: {date}",
  "@lastUpdated": {
    "description": "Shows when something was last updated",
    "placeholders": {
      "date": {
        "type": "DateTime",
        "format": "yMMMd"
      }
    }
  },

  "price": "Price: {price}",
  "@price": {
    "description": "Product price",
    "placeholders": {
      "price": {
        "type": "double",
        "format": "currency",
        "optionalParameters": {
          "symbol": "$",
          "decimalDigits": 2
        }
      }
    }
  },

  "gender": "{gender, select, male{He} female{She} other{They}} liked your post",
  "@gender": {
    "description": "Gender-specific message",
    "placeholders": {
      "gender": {
        "type": "String"
      }
    }
  },

  "signIn": "Sign In",
  "signUp": "Sign Up",
  "email": "Email",
  "password": "Password",
  "forgotPassword": "Forgot password?",

  "errorRequired": "This field is required",
  "errorInvalidEmail": "Please enter a valid email",
  "errorMinLength": "Must be at least {min} characters",
  "@errorMinLength": {
    "placeholders": {
      "min": {
        "type": "int"
      }
    }
  }
}
```

**lib/l10n/app_es.arb** (Spanish)
```json
{
  "@@locale": "es",

  "appTitle": "Mi App",
  "welcome": "¡Bienvenido, {name}!",
  "itemCount": "{count, plural, =0{Sin elementos} =1{1 elemento} other{{count} elementos}}",
  "lastUpdated": "Última actualización: {date}",
  "price": "Precio: {price}",
  "gender": "{gender, select, male{A él} female{A ella} other{Les}} le gustó tu publicación",

  "signIn": "Iniciar sesión",
  "signUp": "Registrarse",
  "email": "Correo electrónico",
  "password": "Contraseña",
  "forgotPassword": "¿Olvidaste tu contraseña?",

  "errorRequired": "Este campo es obligatorio",
  "errorInvalidEmail": "Ingresa un correo válido",
  "errorMinLength": "Debe tener al menos {min} caracteres"
}
```

**lib/l10n/app_ar.arb** (Arabic - RTL)
```json
{
  "@@locale": "ar",

  "appTitle": "تطبيقي",
  "welcome": "!{name} ،مرحباً",
  "itemCount": "{count, plural, =0{لا توجد عناصر} =1{عنصر واحد} two{عنصران} few{{count} عناصر} many{{count} عنصراً} other{{count} عنصر}}",
  "lastUpdated": "{date} :آخر تحديث",

  "signIn": "تسجيل الدخول",
  "signUp": "إنشاء حساب",
  "email": "البريد الإلكتروني",
  "password": "كلمة المرور",
  "forgotPassword": "نسيت كلمة المرور؟",

  "errorRequired": "هذا الحقل مطلوب",
  "errorInvalidEmail": "يرجى إدخال بريد إلكتروني صالح",
  "errorMinLength": "يجب أن يكون {min} أحرف على الأقل"
}
```

---

## App Setup

### Main Configuration

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'l10n/generated/app_localizations.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // Localization configuration
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,

      // Optional: Set initial locale
      // locale: const Locale('es'),

      // Optional: Locale resolution
      localeResolutionCallback: (locale, supportedLocales) {
        // Check if the device locale is supported
        for (final supportedLocale in supportedLocales) {
          if (supportedLocale.languageCode == locale?.languageCode) {
            return supportedLocale;
          }
        }
        // Default to English
        return const Locale('en');
      },

      home: const HomePage(),
    );
  }
}
```

### Using Translations

```dart
// lib/features/home/presentation/pages/home_page.dart
import 'package:flutter/material.dart';
import '../../../../l10n/generated/app_localizations.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    // Get translations
    final l10n = AppLocalizations.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.appTitle),
      ),
      body: Column(
        children: [
          // Simple string
          Text(l10n.signIn),

          // With placeholder
          Text(l10n.welcome('John')),

          // Plural
          Text(l10n.itemCount(5)),

          // Date formatting
          Text(l10n.lastUpdated(DateTime.now())),

          // Currency formatting
          Text(l10n.price(29.99)),

          // Select (gender)
          Text(l10n.gender('female')),
        ],
      ),
    );
  }
}

// Extension for easier access
extension BuildContextL10n on BuildContext {
  AppLocalizations get l10n => AppLocalizations.of(this);
}

// Usage with extension:
// context.l10n.appTitle
```

---

## Locale Management

### Locale Provider

```dart
// lib/core/l10n/locale_provider.dart
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LocaleProvider extends ChangeNotifier {
  static const _localeKey = 'app_locale';

  Locale? _locale;
  Locale? get locale => _locale;

  LocaleProvider() {
    _loadSavedLocale();
  }

  Future<void> _loadSavedLocale() async {
    final prefs = await SharedPreferences.getInstance();
    final languageCode = prefs.getString(_localeKey);

    if (languageCode != null) {
      _locale = Locale(languageCode);
      notifyListeners();
    }
  }

  Future<void> setLocale(Locale locale) async {
    if (_locale == locale) return;

    _locale = locale;
    notifyListeners();

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_localeKey, locale.languageCode);
  }

  Future<void> clearLocale() async {
    _locale = null;
    notifyListeners();

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_localeKey);
  }
}
```

### Language Selector Widget

```dart
// lib/shared/widgets/language_selector.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class LanguageSelector extends StatelessWidget {
  const LanguageSelector({super.key});

  static const _languages = [
    _Language('en', 'English', '🇺🇸'),
    _Language('es', 'Español', '🇪🇸'),
    _Language('ar', 'العربية', '🇸🇦'),
    _Language('zh', '中文', '🇨🇳'),
    _Language('ja', '日本語', '🇯🇵'),
  ];

  @override
  Widget build(BuildContext context) {
    final localeProvider = context.watch<LocaleProvider>();
    final currentLocale = localeProvider.locale ?? const Locale('en');

    return DropdownButton<String>(
      value: currentLocale.languageCode,
      items: _languages.map((lang) {
        return DropdownMenuItem(
          value: lang.code,
          child: Row(
            children: [
              Text(lang.flag),
              const SizedBox(width: 8),
              Text(lang.name),
            ],
          ),
        );
      }).toList(),
      onChanged: (code) {
        if (code != null) {
          localeProvider.setLocale(Locale(code));
        }
      },
    );
  }
}

class _Language {
  final String code;
  final String name;
  final String flag;

  const _Language(this.code, this.name, this.flag);
}
```

---

## RTL Support

### Directional Widgets

```dart
// lib/shared/widgets/directional_widgets.dart
import 'package:flutter/material.dart';

/// Padding that respects text direction
class DirectionalPadding extends StatelessWidget {
  final double start;
  final double end;
  final double top;
  final double bottom;
  final Widget child;

  const DirectionalPadding({
    super.key,
    this.start = 0,
    this.end = 0,
    this.top = 0,
    this.bottom = 0,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsetsDirectional.only(
        start: start,
        end: end,
        top: top,
        bottom: bottom,
      ),
      child: child,
    );
  }
}

/// Row that auto-reverses in RTL
class DirectionalRow extends StatelessWidget {
  final List<Widget> children;
  final MainAxisAlignment mainAxisAlignment;
  final CrossAxisAlignment crossAxisAlignment;

  const DirectionalRow({
    super.key,
    required this.children,
    this.mainAxisAlignment = MainAxisAlignment.start,
    this.crossAxisAlignment = CrossAxisAlignment.center,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      textDirection: Directionality.of(context),
      mainAxisAlignment: mainAxisAlignment,
      crossAxisAlignment: crossAxisAlignment,
      children: children,
    );
  }
}

/// Icon that flips in RTL
class DirectionalIcon extends StatelessWidget {
  final IconData icon;
  final double? size;
  final Color? color;

  const DirectionalIcon(
    this.icon, {
    super.key,
    this.size,
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    final isRtl = Directionality.of(context) == TextDirection.rtl;

    return Transform.flip(
      flipX: isRtl,
      child: Icon(icon, size: size, color: color),
    );
  }
}
```

### RTL-Aware Layouts

```dart
// lib/features/home/presentation/widgets/product_card.dart
import 'package:flutter/material.dart';

class ProductCard extends StatelessWidget {
  final String title;
  final String price;
  final String imageUrl;

  const ProductCard({
    super.key,
    required this.title,
    required this.price,
    required this.imageUrl,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        // Use EdgeInsetsDirectional for RTL support
        padding: const EdgeInsetsDirectional.only(
          start: 16,
          end: 8,
          top: 12,
          bottom: 12,
        ),
        child: Row(
          children: [
            Image.network(imageUrl, width: 80, height: 80),

            const SizedBox(width: 16),

            Expanded(
              child: Column(
                // Use CrossAxisAlignment.start for proper alignment
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  Text(price),
                ],
              ),
            ),

            // Arrow icon that flips in RTL
            const DirectionalIcon(Icons.arrow_forward_ios),
          ],
        ),
      ),
    );
  }
}
```

---

## Date & Number Formatting

### Formatting Service

```dart
// lib/core/l10n/formatting_service.dart
import 'package:intl/intl.dart';
import 'package:flutter/material.dart';

class FormattingService {
  final Locale locale;

  FormattingService(this.locale);

  /// Format date based on locale
  String formatDate(DateTime date, {String? pattern}) {
    if (pattern != null) {
      return DateFormat(pattern, locale.languageCode).format(date);
    }
    return DateFormat.yMMMd(locale.languageCode).format(date);
  }

  /// Format time
  String formatTime(DateTime time) {
    return DateFormat.jm(locale.languageCode).format(time);
  }

  /// Format date and time
  String formatDateTime(DateTime dateTime) {
    return DateFormat.yMMMd(locale.languageCode).add_jm().format(dateTime);
  }

  /// Relative time (e.g., "2 hours ago")
  String formatRelativeTime(DateTime dateTime) {
    final now = DateTime.now();
    final difference = now.difference(dateTime);

    if (difference.inDays > 7) {
      return formatDate(dateTime);
    } else if (difference.inDays > 0) {
      return '${difference.inDays} days ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours} hours ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes} minutes ago';
    } else {
      return 'Just now';
    }
  }

  /// Format currency
  String formatCurrency(double amount, {String? symbol}) {
    final format = NumberFormat.currency(
      locale: locale.languageCode,
      symbol: symbol ?? '\$',
      decimalDigits: 2,
    );
    return format.format(amount);
  }

  /// Format number
  String formatNumber(num number, {int? decimalDigits}) {
    final format = NumberFormat.decimalPattern(locale.languageCode);
    if (decimalDigits != null) {
      format.minimumFractionDigits = decimalDigits;
      format.maximumFractionDigits = decimalDigits;
    }
    return format.format(number);
  }

  /// Format percentage
  String formatPercent(double value) {
    final format = NumberFormat.percentPattern(locale.languageCode);
    return format.format(value);
  }

  /// Format compact number (e.g., 1.2K, 3.4M)
  String formatCompact(num number) {
    final format = NumberFormat.compact(locale: locale.languageCode);
    return format.format(number);
  }
}

// Extension for easy access
extension FormattingContext on BuildContext {
  FormattingService get format =>
      FormattingService(Localizations.localeOf(this));
}

// Usage:
// context.format.formatDate(DateTime.now())
// context.format.formatCurrency(99.99)
```

---

## Translation Workflow

### ARB Management Script

```dart
// tool/l10n_manager.dart
import 'dart:convert';
import 'dart:io';

void main(List<String> args) {
  if (args.isEmpty) {
    print('Usage: dart tool/l10n_manager.dart <command>');
    print('Commands:');
    print('  check    - Check for missing translations');
    print('  sort     - Sort ARB files alphabetically');
    print('  export   - Export to CSV for translation');
    print('  import   - Import translations from CSV');
    return;
  }

  switch (args[0]) {
    case 'check':
      checkMissingTranslations();
      break;
    case 'sort':
      sortArbFiles();
      break;
    case 'export':
      exportToCsv();
      break;
    case 'import':
      if (args.length < 2) {
        print('Usage: dart tool/l10n_manager.dart import <csv_file>');
        return;
      }
      importFromCsv(args[1]);
      break;
  }
}

void checkMissingTranslations() {
  final l10nDir = Directory('lib/l10n');
  final files = l10nDir.listSync().whereType<File>().where(
        (f) => f.path.endsWith('.arb'),
      );

  // Load template (English)
  final templateFile = files.firstWhere(
    (f) => f.path.contains('_en.arb'),
  );
  final template = jsonDecode(templateFile.readAsStringSync()) as Map;
  final templateKeys = template.keys.where((k) => !k.startsWith('@')).toSet();

  // Check each locale
  for (final file in files) {
    if (file.path.contains('_en.arb')) continue;

    final content = jsonDecode(file.readAsStringSync()) as Map;
    final keys = content.keys.where((k) => !k.startsWith('@')).toSet();

    final missing = templateKeys.difference(keys);
    final extra = keys.difference(templateKeys);

    if (missing.isNotEmpty || extra.isNotEmpty) {
      print('\n${file.path}:');
      if (missing.isNotEmpty) {
        print('  Missing: ${missing.join(', ')}');
      }
      if (extra.isNotEmpty) {
        print('  Extra: ${extra.join(', ')}');
      }
    }
  }
}

void sortArbFiles() {
  final l10nDir = Directory('lib/l10n');
  final files = l10nDir.listSync().whereType<File>().where(
        (f) => f.path.endsWith('.arb'),
      );

  for (final file in files) {
    final content = jsonDecode(file.readAsStringSync()) as Map<String, dynamic>;

    // Separate metadata and translations
    final metadata = <String, dynamic>{};
    final translations = <String, dynamic>{};

    content.forEach((key, value) {
      if (key.startsWith('@@')) {
        metadata[key] = value;
      } else {
        translations[key] = value;
      }
    });

    // Sort translations alphabetically
    final sortedKeys = translations.keys.toList()..sort();
    final sorted = <String, dynamic>{};

    // Add metadata first
    sorted.addAll(metadata);

    // Add sorted translations with their descriptions
    for (final key in sortedKeys) {
      if (!key.startsWith('@')) {
        sorted[key] = translations[key];
        if (translations.containsKey('@$key')) {
          sorted['@$key'] = translations['@$key'];
        }
      }
    }

    // Write back
    final encoder = JsonEncoder.withIndent('  ');
    file.writeAsStringSync(encoder.convert(sorted));
    print('Sorted: ${file.path}');
  }
}

void exportToCsv() {
  // Export translations to CSV for external translation services
  final l10nDir = Directory('lib/l10n');
  final files = l10nDir
      .listSync()
      .whereType<File>()
      .where((f) => f.path.endsWith('.arb'))
      .toList();

  final allTranslations = <String, Map<String, String>>{};

  for (final file in files) {
    final content = jsonDecode(file.readAsStringSync()) as Map;
    final locale = content['@@locale'] as String;

    content.forEach((key, value) {
      if (!key.startsWith('@') && !key.startsWith('@@')) {
        allTranslations.putIfAbsent(key, () => {});
        allTranslations[key]![locale] = value.toString();
      }
    });
  }

  // Write CSV
  final buffer = StringBuffer();
  final locales = files
      .map((f) => jsonDecode(f.readAsStringSync())['@@locale'] as String)
      .toList();

  buffer.writeln('key,${locales.join(',')}');

  allTranslations.forEach((key, translations) {
    final values = locales.map((l) => '"${translations[l] ?? ''}"').join(',');
    buffer.writeln('$key,$values');
  });

  File('translations.csv').writeAsStringSync(buffer.toString());
  print('Exported to translations.csv');
}

void importFromCsv(String csvPath) {
  // Import translations from CSV
  final csvFile = File(csvPath);
  final lines = csvFile.readAsLinesSync();

  if (lines.isEmpty) return;

  final header = lines.first.split(',');
  final locales = header.sublist(1);

  // Create ARB content for each locale
  final arbContent = <String, Map<String, dynamic>>{};
  for (final locale in locales) {
    arbContent[locale] = {'@@locale': locale};
  }

  // Parse translations
  for (final line in lines.skip(1)) {
    final values = line.split(',');
    final key = values.first;

    for (var i = 0; i < locales.length; i++) {
      final value = values[i + 1].replaceAll('"', '');
      if (value.isNotEmpty) {
        arbContent[locales[i]]![key] = value;
      }
    }
  }

  // Write ARB files
  final encoder = JsonEncoder.withIndent('  ');
  arbContent.forEach((locale, content) {
    final file = File('lib/l10n/app_$locale.arb');
    file.writeAsStringSync(encoder.convert(content));
    print('Updated: ${file.path}');
  });
}
```

---

## Testing Localization

```dart
// test/l10n/localization_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

void main() {
  group('Localization Tests', () {
    testWidgets('displays English translations', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          locale: Locale('en'),
          localizationsDelegates: [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
          ],
          supportedLocales: [Locale('en'), Locale('es')],
          home: TestWidget(),
        ),
      );

      expect(find.text('Sign In'), findsOneWidget);
    });

    testWidgets('displays Spanish translations', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          locale: Locale('es'),
          localizationsDelegates: [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
          ],
          supportedLocales: [Locale('en'), Locale('es')],
          home: TestWidget(),
        ),
      );

      expect(find.text('Iniciar sesión'), findsOneWidget);
    });

    testWidgets('handles plurals correctly', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          locale: const Locale('en'),
          localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
          ],
          supportedLocales: const [Locale('en')],
          home: Builder(
            builder: (context) {
              final l10n = AppLocalizations.of(context);
              return Column(
                children: [
                  Text(l10n.itemCount(0)),
                  Text(l10n.itemCount(1)),
                  Text(l10n.itemCount(5)),
                ],
              );
            },
          ),
        ),
      );

      expect(find.text('No items'), findsOneWidget);
      expect(find.text('1 item'), findsOneWidget);
      expect(find.text('5 items'), findsOneWidget);
    });

    testWidgets('RTL layout is correct', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          locale: Locale('ar'),
          localizationsDelegates: [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
          ],
          supportedLocales: [Locale('en'), Locale('ar')],
          home: Scaffold(
            body: Padding(
              padding: EdgeInsetsDirectional.only(start: 16),
              child: Text('Test'),
            ),
          ),
        ),
      );

      // Verify RTL is applied
      final direction = tester.widget<Directionality>(
        find.byType(Directionality).first,
      );
      expect(direction.textDirection, TextDirection.rtl);
    });
  });
}

class TestWidget extends StatelessWidget {
  const TestWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    return Text(l10n.signIn);
  }
}
```

---

## Checklist

- [ ] Set up flutter_localizations dependency
- [ ] Created l10n.yaml configuration
- [ ] Created template ARB file (English)
- [ ] Added all required languages
- [ ] Implemented locale provider
- [ ] Added language selector widget
- [ ] Used EdgeInsetsDirectional for padding
- [ ] Tested RTL layouts
- [ ] Set up date/number formatting
- [ ] Created translation management scripts
- [ ] Tested all locales
- [ ] Documented translation workflow

---

## Integration with Other Agents

- **Project Setup Agent**: Initialize i18n during project setup
- **Testing Strategy Agent**: Localization tests
- **Compliance Agent**: Legal text translations
- **Documentation Agent**: Document supported languages
