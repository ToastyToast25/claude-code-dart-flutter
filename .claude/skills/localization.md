---
description: "Adds internationalization (i18n) and localization (l10n) support"
globs: ["lib/l10n/**/*.arb", "l10n.yaml", "lib/**/localization/**/*.dart"]
alwaysApply: false
---

# Localization Skill

Add internationalization (i18n) and localization (l10n) support to Flutter apps.

## Trigger Keywords
- localization
- internationalization
- i18n
- l10n
- translations
- multi-language

---

## Setup with flutter_localizations

### 1. Add Dependencies

```yaml
# pubspec.yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  intl: ^0.19.0

flutter:
  generate: true
```

### 2. Configure l10n.yaml

```yaml
# l10n.yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
nullable-getter: false
```

### 3. Create ARB Files

```json
// lib/l10n/app_en.arb
{
  "@@locale": "en",
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
  "greeting": "{gender, select, male{Mr.} female{Ms.} other{Dear}} {name}",
  "@greeting": {
    "description": "Gender-specific greeting",
    "placeholders": {
      "gender": {
        "type": "String"
      },
      "name": {
        "type": "String"
      }
    }
  },
  "lastLogin": "Last login: {date}",
  "@lastLogin": {
    "description": "Last login date",
    "placeholders": {
      "date": {
        "type": "DateTime",
        "format": "yMMMd"
      }
    }
  },
  "price": "Price: {amount}",
  "@price": {
    "description": "Product price",
    "placeholders": {
      "amount": {
        "type": "double",
        "format": "currency",
        "optionalParameters": {
          "symbol": "$"
        }
      }
    }
  }
}
```

```json
// lib/l10n/app_es.arb
{
  "@@locale": "es",
  "appTitle": "Mi Aplicación",
  "welcome": "¡Bienvenido, {name}!",
  "itemCount": "{count, plural, =0{Sin artículos} =1{1 artículo} other{{count} artículos}}",
  "greeting": "{gender, select, male{Sr.} female{Sra.} other{Estimado/a}} {name}",
  "lastLogin": "Último acceso: {date}",
  "price": "Precio: {amount}"
}
```

### 4. Configure MaterialApp

```dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',

      // Localization delegates
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],

      // Supported locales
      supportedLocales: const [
        Locale('en'),
        Locale('es'),
        Locale('fr'),
        Locale('de'),
        Locale('pt', 'BR'), // Portuguese (Brazil)
        Locale('zh', 'CN'), // Chinese (Simplified)
      ],

      // Optional: Force specific locale
      // locale: const Locale('es'),

      // Optional: Locale resolution
      localeResolutionCallback: (locale, supportedLocales) {
        // Check if device locale is supported
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

### 5. Generate Localizations

```bash
flutter gen-l10n
```

### 6. Use Translations

```dart
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.appTitle),
      ),
      body: Column(
        children: [
          // Simple string
          Text(l10n.appTitle),

          // With placeholder
          Text(l10n.welcome('John')),

          // Plural
          Text(l10n.itemCount(5)),

          // Gender select
          Text(l10n.greeting('male', 'Smith')),

          // Date formatting
          Text(l10n.lastLogin(DateTime.now())),

          // Currency formatting
          Text(l10n.price(29.99)),
        ],
      ),
    );
  }
}
```

---

## Language Switcher

### Locale Provider

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

final localeProvider = StateNotifierProvider<LocaleNotifier, Locale>((ref) {
  return LocaleNotifier();
});

class LocaleNotifier extends StateNotifier<Locale> {
  LocaleNotifier() : super(const Locale('en')) {
    _loadSavedLocale();
  }

  static const _key = 'app_locale';

  Future<void> _loadSavedLocale() async {
    final prefs = await SharedPreferences.getInstance();
    final savedLocale = prefs.getString(_key);
    if (savedLocale != null) {
      state = Locale(savedLocale);
    }
  }

  Future<void> setLocale(Locale locale) async {
    state = locale;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, locale.languageCode);
  }
}
```

### App with Locale Provider

```dart
class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final locale = ref.watch(localeProvider);

    return MaterialApp(
      locale: locale,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      home: const HomePage(),
    );
  }
}
```

### Language Selector Widget

```dart
class LanguageSelector extends ConsumerWidget {
  const LanguageSelector({super.key});

  static const _supportedLocales = [
    (locale: Locale('en'), name: 'English', flag: '🇺🇸'),
    (locale: Locale('es'), name: 'Español', flag: '🇪🇸'),
    (locale: Locale('fr'), name: 'Français', flag: '🇫🇷'),
    (locale: Locale('de'), name: 'Deutsch', flag: '🇩🇪'),
  ];

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final currentLocale = ref.watch(localeProvider);

    return DropdownButton<Locale>(
      value: currentLocale,
      items: _supportedLocales.map((item) {
        return DropdownMenuItem(
          value: item.locale,
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(item.flag),
              const SizedBox(width: 8),
              Text(item.name),
            ],
          ),
        );
      }).toList(),
      onChanged: (locale) {
        if (locale != null) {
          ref.read(localeProvider.notifier).setLocale(locale);
        }
      },
    );
  }
}
```

---

## ARB Syntax Reference

### Simple String
```json
{
  "title": "Hello World",
  "@title": {
    "description": "Simple greeting"
  }
}
```

### Placeholder
```json
{
  "greeting": "Hello, {name}!",
  "@greeting": {
    "placeholders": {
      "name": {"type": "String"}
    }
  }
}
```

### Plural
```json
{
  "items": "{count, plural, =0{No items} =1{One item} other{{count} items}}",
  "@items": {
    "placeholders": {
      "count": {"type": "int"}
    }
  }
}
```

### Select (Gender/Choice)
```json
{
  "pronoun": "{gender, select, male{he} female{she} other{they}}",
  "@pronoun": {
    "placeholders": {
      "gender": {"type": "String"}
    }
  }
}
```

### Date Formatting
```json
{
  "dateMessage": "Today is {date}",
  "@dateMessage": {
    "placeholders": {
      "date": {
        "type": "DateTime",
        "format": "yMMMEd"
      }
    }
  }
}
```

### Number Formatting
```json
{
  "percentage": "Progress: {value}",
  "@percentage": {
    "placeholders": {
      "value": {
        "type": "double",
        "format": "percentPattern"
      }
    }
  }
}
```

### Currency
```json
{
  "price": "{amount}",
  "@price": {
    "placeholders": {
      "amount": {
        "type": "double",
        "format": "currency",
        "optionalParameters": {
          "symbol": "€",
          "decimalDigits": 2
        }
      }
    }
  }
}
```

---

## File Structure

```
lib/
├── l10n/
│   ├── app_en.arb          # English (base)
│   ├── app_es.arb          # Spanish
│   ├── app_fr.arb          # French
│   ├── app_de.arb          # German
│   ├── app_pt_BR.arb       # Portuguese (Brazil)
│   └── app_zh_CN.arb       # Chinese (Simplified)
└── l10n.yaml               # Configuration
```

---

## Testing Localizations

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

void main() {
  testWidgets('displays translated text', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        locale: const Locale('es'),
        localizationsDelegates: AppLocalizations.localizationsDelegates,
        supportedLocales: AppLocalizations.supportedLocales,
        home: const MyWidget(),
      ),
    );

    expect(find.text('¡Bienvenido!'), findsOneWidget);
  });

  testWidgets('pluralization works correctly', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        localizationsDelegates: AppLocalizations.localizationsDelegates,
        supportedLocales: AppLocalizations.supportedLocales,
        home: Builder(
          builder: (context) {
            final l10n = AppLocalizations.of(context);
            return Text(l10n.itemCount(1));
          },
        ),
      ),
    );

    expect(find.text('1 item'), findsOneWidget);
  });
}
```

---

## Checklist

- [ ] `flutter_localizations` added to dependencies
- [ ] `l10n.yaml` configured
- [ ] Base ARB file created (template)
- [ ] Translation ARB files for each language
- [ ] `flutter: generate: true` in pubspec.yaml
- [ ] MaterialApp configured with delegates
- [ ] Supported locales defined
- [ ] Language switcher implemented
- [ ] Locale persistence (SharedPreferences)
- [ ] All user-facing strings externalized
- [ ] Pluralization handled correctly
- [ ] Date/number formatting uses locale
