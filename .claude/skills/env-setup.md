---
description: "Configures environment variables, build flavors, and secrets management"
globs: [".env*", "config/*.json", "lib/**/env/*.dart", "lib/**/config/*.dart"]
alwaysApply: false
---

# Environment Setup Skill

Configure environment variables and build configurations for Flutter apps.

## Trigger Keywords
- env setup
- environment variables
- environment configuration
- config setup
- build flavors

---

## Option 1: Dart Define (Simple)

### Pass Variables at Build Time

```bash
# Development
flutter run --dart-define=API_URL=https://dev-api.example.com --dart-define=ENV=development

# Staging
flutter run --dart-define=API_URL=https://staging-api.example.com --dart-define=ENV=staging

# Production
flutter build apk --dart-define=API_URL=https://api.example.com --dart-define=ENV=production
```

### Access in Dart

```dart
class Environment {
  static const String apiUrl = String.fromEnvironment(
    'API_URL',
    defaultValue: 'https://dev-api.example.com',
  );

  static const String env = String.fromEnvironment(
    'ENV',
    defaultValue: 'development',
  );

  static const bool isProduction = env == 'production';
  static const bool isDevelopment = env == 'development';
}
```

### Define File (flutter run --dart-define-from-file)

```json
// config/dev.json
{
  "API_URL": "https://dev-api.example.com",
  "ENV": "development",
  "ENABLE_LOGGING": "true"
}
```

```bash
flutter run --dart-define-from-file=config/dev.json
```

---

## Option 2: envied Package (Recommended)

### Setup

```bash
flutter pub add envied
flutter pub add --dev envied_generator
flutter pub add --dev build_runner
```

### Create .env Files

```bash
# .env (development - not committed)
API_URL=https://dev-api.example.com
API_KEY=dev_secret_key_123
ENABLE_LOGGING=true

# .env.staging
API_URL=https://staging-api.example.com
API_KEY=staging_secret_key_456
ENABLE_LOGGING=true

# .env.production
API_URL=https://api.example.com
API_KEY=prod_secret_key_789
ENABLE_LOGGING=false
```

### Create Env Class

```dart
// lib/core/env/env.dart
import 'package:envied/envied.dart';

part 'env.g.dart';

@Envied(path: '.env')
abstract class Env {
  @EnviedField(varName: 'API_URL')
  static const String apiUrl = _Env.apiUrl;

  @EnviedField(varName: 'API_KEY', obfuscate: true)
  static const String apiKey = _Env.apiKey;

  @EnviedField(varName: 'ENABLE_LOGGING', defaultValue: 'false')
  static const String enableLogging = _Env.enableLogging;

  static bool get isLoggingEnabled => enableLogging == 'true';
}
```

### Generate

```bash
dart run build_runner build --delete-conflicting-outputs
```

### Update .gitignore

```gitignore
# Environment files
.env
.env.local
*.env

# Keep example
!.env.example

# Generated env files
lib/core/env/env.g.dart
```

---

## Option 3: Flutter Flavors (Full)

### Android Configuration

```groovy
// android/app/build.gradle
android {
    flavorDimensions "environment"

    productFlavors {
        development {
            dimension "environment"
            applicationIdSuffix ".dev"
            versionNameSuffix "-dev"
            resValue "string", "app_name", "MyApp Dev"
        }
        staging {
            dimension "environment"
            applicationIdSuffix ".staging"
            versionNameSuffix "-staging"
            resValue "string", "app_name", "MyApp Staging"
        }
        production {
            dimension "environment"
            resValue "string", "app_name", "MyApp"
        }
    }
}
```

### iOS Configuration

```ruby
# ios/Podfile
project 'Runner', {
  'Debug-development' => :debug,
  'Debug-staging' => :debug,
  'Debug-production' => :debug,
  'Release-development' => :release,
  'Release-staging' => :release,
  'Release-production' => :release,
}
```

Create schemes in Xcode for each flavor.

### Launch Configurations

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Development",
      "request": "launch",
      "type": "dart",
      "program": "lib/main_development.dart",
      "args": ["--flavor", "development"]
    },
    {
      "name": "Staging",
      "request": "launch",
      "type": "dart",
      "program": "lib/main_staging.dart",
      "args": ["--flavor", "staging"]
    },
    {
      "name": "Production",
      "request": "launch",
      "type": "dart",
      "program": "lib/main_production.dart",
      "args": ["--flavor", "production"]
    }
  ]
}
```

### Entry Points

```dart
// lib/main_development.dart
import 'package:my_app/app.dart';
import 'package:my_app/core/config/app_config.dart';

void main() {
  AppConfig.init(
    environment: Environment.development,
    apiUrl: 'https://dev-api.example.com',
    enableLogging: true,
  );
  runApp(const MyApp());
}

// lib/main_staging.dart
import 'package:my_app/app.dart';
import 'package:my_app/core/config/app_config.dart';

void main() {
  AppConfig.init(
    environment: Environment.staging,
    apiUrl: 'https://staging-api.example.com',
    enableLogging: true,
  );
  runApp(const MyApp());
}

// lib/main_production.dart
import 'package:my_app/app.dart';
import 'package:my_app/core/config/app_config.dart';

void main() {
  AppConfig.init(
    environment: Environment.production,
    apiUrl: 'https://api.example.com',
    enableLogging: false,
  );
  runApp(const MyApp());
}
```

### App Config Class

```dart
// lib/core/config/app_config.dart
enum Environment { development, staging, production }

class AppConfig {
  AppConfig._();

  static late Environment environment;
  static late String apiUrl;
  static late bool enableLogging;

  static bool get isDevelopment => environment == Environment.development;
  static bool get isStaging => environment == Environment.staging;
  static bool get isProduction => environment == Environment.production;

  static void init({
    required Environment environment,
    required String apiUrl,
    required bool enableLogging,
  }) {
    AppConfig.environment = environment;
    AppConfig.apiUrl = apiUrl;
    AppConfig.enableLogging = enableLogging;
  }
}
```

### Run Commands

```bash
# Development
flutter run --flavor development -t lib/main_development.dart

# Staging
flutter run --flavor staging -t lib/main_staging.dart

# Production
flutter build apk --flavor production -t lib/main_production.dart
```

---

## Firebase Environment Config

### Multiple Firebase Projects

```
android/app/
├── src/
│   ├── development/
│   │   └── google-services.json
│   ├── staging/
│   │   └── google-services.json
│   └── production/
│       └── google-services.json

ios/
├── config/
│   ├── development/
│   │   └── GoogleService-Info.plist
│   ├── staging/
│   │   └── GoogleService-Info.plist
│   └── production/
│       └── GoogleService-Info.plist
```

### iOS Build Phase Script

```bash
# Copy GoogleService-Info.plist based on flavor
cp "${PROJECT_DIR}/config/${CONFIGURATION}/GoogleService-Info.plist" "${PROJECT_DIR}/Runner/GoogleService-Info.plist"
```

---

## Secrets Management

### For CI/CD (GitHub Actions)

```yaml
# .github/workflows/build.yml
name: Build

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Create .env file
        run: |
          echo "API_URL=${{ secrets.API_URL }}" >> .env
          echo "API_KEY=${{ secrets.API_KEY }}" >> .env

      - name: Build
        run: flutter build apk --dart-define-from-file=.env
```

### Local Secrets

```dart
// lib/core/secrets/secrets.dart (git-ignored)
class Secrets {
  static const String apiKey = 'your-secret-key';
  static const String firebaseKey = 'firebase-key';
}

// lib/core/secrets/secrets.example.dart (committed)
class Secrets {
  static const String apiKey = 'YOUR_API_KEY_HERE';
  static const String firebaseKey = 'YOUR_FIREBASE_KEY_HERE';
}
```

---

## .env.example Template

```bash
# .env.example
# Copy this file to .env and fill in your values

# API Configuration
API_URL=https://api.example.com
API_KEY=your_api_key_here

# Feature Flags
ENABLE_LOGGING=true
ENABLE_ANALYTICS=true
ENABLE_CRASH_REPORTING=true

# Third-Party Services
SENTRY_DSN=your_sentry_dsn
FIREBASE_PROJECT_ID=your_project_id
```

---

## File Structure

```
project/
├── .env                    # Local dev (git-ignored)
├── .env.example            # Template (committed)
├── config/
│   ├── dev.json           # Dart define files
│   ├── staging.json
│   └── prod.json
├── lib/
│   ├── main_development.dart
│   ├── main_staging.dart
│   ├── main_production.dart
│   └── core/
│       ├── config/
│       │   └── app_config.dart
│       └── env/
│           ├── env.dart
│           └── env.g.dart  # Generated (git-ignored)
└── android/
    └── app/
        └── src/
            ├── development/
            ├── staging/
            └── production/
```

---

## Checklist

- [ ] .env files in .gitignore
- [ ] .env.example committed with placeholders
- [ ] Secrets obfuscated (envied obfuscate option)
- [ ] Different API URLs per environment
- [ ] Feature flags configurable per environment
- [ ] Firebase configs per environment
- [ ] CI/CD secrets configured
- [ ] Launch configurations for each environment
- [ ] Build commands documented
