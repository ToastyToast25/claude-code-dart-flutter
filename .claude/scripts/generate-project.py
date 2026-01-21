#!/usr/bin/env python3
"""
Project Generator Script
Generates a new Dart/Flutter project based on configuration

Usage:
  python generate-project.py --config project-config.json
  python generate-project.py --interactive
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Project templates
MAIN_DART_TEMPLATE = '''import 'package:flutter/material.dart';
{imports}

void main() async {{
  WidgetsFlutterBinding.ensureInitialized();
  {init_code}
  runApp(const App());
}}
'''

APP_DART_TEMPLATE = '''import 'package:flutter/material.dart';
{imports}

class App extends StatelessWidget {{
  const App({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return {wrapper_start}MaterialApp.router(
      title: '{app_name}',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.system,
      routerConfig: appRouter,
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
    ){wrapper_end};
  }}
}}
'''

GITIGNORE_TEMPLATE = '''# Dependencies
.packages
.pub/
pubspec.lock
build/
.dart_tool/

# Generated files
*.g.dart
*.freezed.dart
*.mocks.dart
*.config.dart
lib/generated/

# IDE
.idea/
*.iml
.vscode/
*.swp
*.swo

# macOS
.DS_Store
*.pem

# Android
**/android/**/gradle-wrapper.jar
**/android/.gradle
**/android/captures/
**/android/gradlew
**/android/gradlew.bat
**/android/local.properties
**/android/**/GeneratedPluginRegistrant.*
**/android/key.properties
*.jks
*.keystore

# iOS/XCode
**/ios/**/*.mode1v3
**/ios/**/*.mode2v3
**/ios/**/*.moved-aside
**/ios/**/*.pbxuser
**/ios/**/*.perspectivev3
**/ios/**/*sync/
**/ios/**/.sconsign.dblite
**/ios/**/.tags*
**/ios/**/.vagrant/
**/ios/**/DerivedData/
**/ios/**/Icon?
**/ios/**/Pods/
**/ios/**/.symlinks/
**/ios/**/profile
**/ios/**/xcuserdata
**/ios/.generated/
**/ios/Flutter/.last_build_id
**/ios/Flutter/App.framework
**/ios/Flutter/Flutter.framework
**/ios/Flutter/Flutter.podspec
**/ios/Flutter/Generated.xcconfig
**/ios/Flutter/ephemeral
**/ios/Flutter/app.flx
**/ios/Flutter/app.zip
**/ios/Flutter/flutter_assets/
**/ios/Flutter/flutter_export_environment.sh
**/ios/ServiceDefinitions.json
**/ios/Runner/GeneratedPluginRegistrant.*

# Web
lib/generated_plugin_registrant.dart

# Exceptions to above rules
!**/ios/**/default.mode1v3
!**/ios/**/default.mode2v3
!**/ios/**/default.pbxuser
!**/ios/**/default.perspectivev3

# Environment
.env
.env.*
!.env.example

# Secrets
*.pem
*.p12
*.key
google-services.json
GoogleService-Info.plist
firebase_options.dart

# Coverage
coverage/
*.lcov

# Test
test/.test_coverage.dart

# Logs
*.log
logs/

# Temp
tmp/
temp/
'''

ENV_EXAMPLE_TEMPLATE = '''# Environment Configuration
# Copy this to .env and fill in values

# App Configuration
APP_NAME={app_name}
APP_ENV=development

# API Configuration
API_BASE_URL=http://localhost:3000/api/v1
API_TIMEOUT=30000

# Authentication
AUTH_URL=http://localhost:3000/api/v1/auth
JWT_SECRET=your-secret-key-here

# Database (if backend)
DATABASE_URL=postgresql://user:password@localhost:5432/{db_name}

# Firebase (if used)
# FIREBASE_PROJECT_ID=
# FIREBASE_API_KEY=

# Sentry (if used)
# SENTRY_DSN=

# Feature Flags
ENABLE_ANALYTICS=false
ENABLE_CRASH_REPORTING=false
'''

README_TEMPLATE = '''# {app_name}

{description}

## Getting Started

### Prerequisites

- Flutter SDK {flutter_version}+
- Dart SDK {dart_version}+
{additional_prerequisites}

### Installation

```bash
# Clone the repository
git clone {repo_url}
cd {project_name}

# Install dependencies
flutter pub get

# Generate code
flutter pub run build_runner build --delete-conflicting-outputs

# Run the app
flutter run
```

### Environment Setup

1. Copy `.env.example` to `.env`
2. Fill in the required values
3. Run the app

## Project Structure

```
lib/
├── app/           # App configuration and routing
├── core/          # Core utilities and constants
├── features/      # Feature modules
├── shared/        # Shared components
└── main.dart      # Entry point
```

## Architecture

This project follows Clean Architecture with:
- **Presentation Layer**: BLoC/Riverpod for state management
- **Domain Layer**: Use cases and entities
- **Data Layer**: Repositories and data sources

## Testing

```bash
# Run unit tests
flutter test

# Run with coverage
flutter test --coverage

# Run integration tests
flutter test integration_test
```

## Building

```bash
# Android APK
flutter build apk --release

# iOS
flutter build ios --release

# Web
flutter build web --release
```

## License

{license}
'''

def create_directory_structure(base_path: Path, structure: dict):
    """Recursively create directory structure."""
    for name, content in structure.items():
        path = base_path / name
        if isinstance(content, dict):
            path.mkdir(parents=True, exist_ok=True)
            create_directory_structure(path, content)
        elif isinstance(content, str):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')


def generate_pubspec(config: dict) -> str:
    """Generate pubspec.yaml content."""
    deps = ['flutter:\n    sdk: flutter']
    dev_deps = ['flutter_test:\n    sdk: flutter', 'flutter_lints: ^3.0.1']

    # State management
    if config.get('state_management') == 'riverpod':
        deps.extend(['flutter_riverpod: ^2.4.9', 'riverpod_annotation: ^2.3.3'])
        dev_deps.append('riverpod_generator: ^2.3.9')
    elif config.get('state_management') == 'bloc':
        deps.extend(['flutter_bloc: ^8.1.3', 'bloc: ^8.1.2'])
        dev_deps.append('bloc_test: ^9.1.5')
    elif config.get('state_management') == 'provider':
        deps.append('provider: ^6.1.1')

    # Routing
    if config.get('routing') == 'go_router':
        deps.append('go_router: ^13.0.1')
    elif config.get('routing') == 'auto_route':
        deps.append('auto_route: ^7.8.4')
        dev_deps.append('auto_route_generator: ^7.3.2')

    # Common dependencies
    deps.extend([
        'dio: ^5.4.0',
        'freezed_annotation: ^2.4.1',
        'json_annotation: ^4.8.1',
        'equatable: ^2.0.5',
        'dartz: ^0.10.1',
        'get_it: ^7.6.4',
        'injectable: ^2.3.2',
        'flutter_secure_storage: ^9.0.0',
        'intl: ^0.18.1',
    ])

    dev_deps.extend([
        'build_runner: ^2.4.8',
        'freezed: ^2.4.6',
        'json_serializable: ^6.7.1',
        'injectable_generator: ^2.4.1',
        'mocktail: ^1.0.1',
    ])

    # Firebase
    if config.get('firebase'):
        deps.extend([
            'firebase_core: ^2.24.2',
            'firebase_auth: ^4.16.0',
        ])
        if config.get('firebase_crashlytics'):
            deps.append('firebase_crashlytics: ^3.4.9')

    # Format dependencies
    deps_str = '\n  '.join(deps)
    dev_deps_str = '\n  '.join(dev_deps)

    return f'''name: {config['project_name']}
description: {config.get('description', 'A new Flutter project')}
version: 1.0.0+1
publish_to: none

environment:
  sdk: ">=3.0.0 <4.0.0"
  flutter: ">=3.16.0"

dependencies:
  {deps_str}

dev_dependencies:
  {dev_deps_str}

flutter:
  uses-material-design: true
  generate: true

  assets:
    - assets/images/
    - assets/icons/
'''


def main():
    """Main entry point."""
    print("Project Generator")
    print("=" * 50)

    # Default config for testing
    config = {
        'project_name': 'my_app',
        'description': 'A new Flutter application',
        'state_management': 'riverpod',
        'routing': 'go_router',
        'firebase': False,
        'platforms': ['android', 'ios', 'web'],
    }

    # Read config from stdin if available
    if not sys.stdin.isatty():
        try:
            config.update(json.load(sys.stdin))
        except:
            pass

    print(f"Generating project: {config['project_name']}")

    base_path = Path(config.get('output_path', '.')) / config['project_name']

    # Create basic structure
    structure = {
        'lib': {
            'app': {
                'app.dart': '// App widget\n',
                'router': {
                    'app_router.dart': '// Router configuration\n',
                },
            },
            'core': {
                'constants': {},
                'errors': {},
                'extensions': {},
                'services': {},
                'utils': {},
            },
            'features': {},
            'shared': {
                'data': {},
                'domain': {'entities': {}},
                'presentation': {
                    'widgets': {},
                    'theme': {},
                },
            },
            'main.dart': '// Entry point\n',
            'injection.dart': '// Dependency injection\n',
        },
        'test': {
            'helpers': {},
            'fixtures': {},
        },
        'assets': {
            'images': {'.gitkeep': ''},
            'icons': {'.gitkeep': ''},
            'fonts': {'.gitkeep': ''},
        },
        '.claude': {
            'context.md': f'# {config["project_name"]} Context\n\nCreated: {datetime.now().isoformat()}\n',
        },
        'pubspec.yaml': generate_pubspec(config),
        '.gitignore': GITIGNORE_TEMPLATE,
        '.env.example': ENV_EXAMPLE_TEMPLATE.format(
            app_name=config['project_name'],
            db_name=config['project_name'].replace('-', '_'),
        ),
        'README.md': README_TEMPLATE.format(
            app_name=config['project_name'],
            description=config.get('description', ''),
            flutter_version='3.16',
            dart_version='3.0',
            additional_prerequisites='',
            repo_url=config.get('repo_url', 'https://github.com/user/repo'),
            project_name=config['project_name'],
            license='MIT',
        ),
    }

    create_directory_structure(base_path, structure)

    print(f"Project created at: {base_path}")
    print("\nNext steps:")
    print(f"  cd {config['project_name']}")
    print("  flutter pub get")
    print("  flutter pub run build_runner build")
    print("  flutter run")


if __name__ == '__main__':
    main()
