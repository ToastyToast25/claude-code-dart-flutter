---
description: "Manages semantic versioning, changelogs, and release preparation"
globs: ["pubspec.yaml", "CHANGELOG.md", "lib/**/version.dart"]
alwaysApply: false
---

# Versioning Skill

Manage semantic versioning, changelogs, and release preparation.

## Trigger Keywords
- version bump
- release
- changelog
- new version
- prepare release

---

## Semantic Versioning

### Version Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
1.0.0
2.1.3
1.0.0-alpha.1
1.0.0-beta.2
1.0.0-rc.1
1.0.0+build.123
```

### When to Bump

| Change | Bump | Example |
|--------|------|---------|
| Breaking API change | MAJOR | 1.0.0 → 2.0.0 |
| New feature (backward compatible) | MINOR | 1.0.0 → 1.1.0 |
| Bug fix | PATCH | 1.0.0 → 1.0.1 |
| Documentation | PATCH | 1.0.0 → 1.0.1 |
| Refactoring (no API change) | PATCH | 1.0.0 → 1.0.1 |

---

## Files to Update

### 1. pubspec.yaml

```yaml
name: my_app
version: 1.2.3+45  # version+buildNumber

# For apps: version is display version, build number for stores
# For packages: version only (no build number)
```

### 2. CHANGELOG.md

```markdown
## [Unreleased]

### Added
- New feature X

### Changed
- Updated feature Y

### Fixed
- Bug fix Z

## [1.2.3] - 2026-01-21

### Added
- Feature A
- Feature B

### Fixed
- Issue #123
```

### 3. lib/core/version.dart (Optional)

```dart
/// App version information.
///
/// This file is auto-generated. Do not edit manually.
/// Run `dart run tool/update_version.dart` to update.
class AppVersion {
  AppVersion._();

  /// Current version string (e.g., "1.2.3")
  static const String version = '1.2.3';

  /// Build number for app stores
  static const int buildNumber = 45;

  /// Full version string (e.g., "1.2.3+45")
  static const String fullVersion = '$version+$buildNumber';

  /// Git commit hash (set during CI build)
  static const String gitHash = String.fromEnvironment(
    'GIT_HASH',
    defaultValue: 'development',
  );

  /// Build date
  static const String buildDate = String.fromEnvironment(
    'BUILD_DATE',
    defaultValue: 'unknown',
  );

  /// Whether this is a release build
  static const bool isRelease = bool.fromEnvironment('dart.vm.product');
}
```

---

## Version Bump Process

### Manual Process

```bash
# 1. Decide version type
# MAJOR: Breaking changes
# MINOR: New features
# PATCH: Bug fixes

# 2. Update pubspec.yaml
# version: 1.2.3+45 → 1.3.0+46

# 3. Update CHANGELOG.md
# Move [Unreleased] items to new version section

# 4. Update version.dart (if exists)

# 5. Commit
git add .
git commit -m "chore: bump version to 1.3.0"

# 6. Tag
git tag -a v1.3.0 -m "Release 1.3.0"

# 7. Push
git push origin main --tags
```

### Automated Script

```dart
// tool/bump_version.dart
import 'dart:io';
import 'package:yaml/yaml.dart';
import 'package:yaml_edit/yaml_edit.dart';

enum BumpType { major, minor, patch }

Future<void> main(List<String> args) async {
  if (args.isEmpty) {
    print('Usage: dart run tool/bump_version.dart <major|minor|patch>');
    exit(1);
  }

  final bumpType = BumpType.values.firstWhere(
    (t) => t.name == args[0],
    orElse: () {
      print('Invalid bump type: ${args[0]}');
      exit(1);
    },
  );

  // Read pubspec.yaml
  final pubspecFile = File('pubspec.yaml');
  final pubspecContent = await pubspecFile.readAsString();
  final pubspec = loadYaml(pubspecContent);

  // Parse current version
  final currentVersion = pubspec['version'] as String;
  final versionParts = currentVersion.split('+');
  final version = versionParts[0];
  final buildNumber = int.parse(versionParts.length > 1 ? versionParts[1] : '0');

  final semverParts = version.split('.').map(int.parse).toList();

  // Bump version
  switch (bumpType) {
    case BumpType.major:
      semverParts[0]++;
      semverParts[1] = 0;
      semverParts[2] = 0;
    case BumpType.minor:
      semverParts[1]++;
      semverParts[2] = 0;
    case BumpType.patch:
      semverParts[2]++;
  }

  final newVersion = semverParts.join('.');
  final newBuildNumber = buildNumber + 1;
  final fullVersion = '$newVersion+$newBuildNumber';

  // Update pubspec.yaml
  final editor = YamlEditor(pubspecContent);
  editor.update(['version'], fullVersion);
  await pubspecFile.writeAsString(editor.toString());

  // Update version.dart if exists
  final versionFile = File('lib/core/version.dart');
  if (await versionFile.exists()) {
    var content = await versionFile.readAsString();
    content = content.replaceAll(
      RegExp(r"static const String version = '[^']+';"),
      "static const String version = '$newVersion';",
    );
    content = content.replaceAll(
      RegExp(r"static const int buildNumber = \d+;"),
      "static const int buildNumber = $newBuildNumber;",
    );
    await versionFile.writeAsString(content);
  }

  print('✓ Bumped version: $currentVersion → $fullVersion');
  print('');
  print('Next steps:');
  print('  1. Update CHANGELOG.md');
  print('  2. git add .');
  print('  3. git commit -m "chore: bump version to $newVersion"');
  print('  4. git tag -a v$newVersion -m "Release $newVersion"');
  print('  5. git push origin main --tags');
}
```

---

## Changelog Format

### Categories

Use these standard categories:

- **Added**: New features
- **Changed**: Changes to existing features
- **Deprecated**: Features to be removed in future
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

### Good Changelog Entries

```markdown
### Added
- Add user profile page with avatar upload (#123)
- Add dark mode support across all screens
- Add offline caching for frequently accessed data

### Changed
- Improve loading performance by 40% through lazy loading
- Update minimum iOS version to 14.0
- Redesign onboarding flow for better conversion

### Fixed
- Fix crash when rotating device during video playback (#456)
- Fix incorrect date formatting in user settings
- Fix memory leak in image gallery component
```

### Bad Changelog Entries

```markdown
### Changed
- Updated stuff  ❌ (too vague)
- Fixed bug      ❌ (which bug?)
- Changes        ❌ (no description)
- v1.2.3         ❌ (just version number)
```

---

## Release Checklist

### Pre-Release

```markdown
- [ ] All tests pass: `flutter test`
- [ ] No analyzer warnings: `flutter analyze`
- [ ] Code formatted: `dart format .`
- [ ] Documentation updated
- [ ] CHANGELOG.md updated with all changes
- [ ] Version bumped in pubspec.yaml
- [ ] Version bumped in version.dart (if applicable)
- [ ] Build succeeds for all platforms
- [ ] Manual testing completed
```

### Release

```markdown
- [ ] Create release commit
- [ ] Create git tag
- [ ] Push to remote with tags
- [ ] Create GitHub release with changelog
- [ ] Upload artifacts (APK, IPA, etc.) if applicable
- [ ] Update documentation site if applicable
- [ ] Announce release (if applicable)
```

### Post-Release

```markdown
- [ ] Verify release artifacts
- [ ] Monitor crash reports
- [ ] Update [Unreleased] section in CHANGELOG
- [ ] Close related GitHub milestones
```

---

## GitHub Release Template

```markdown
## What's New in v1.2.3

### Highlights
- 🚀 New feature X makes Y 40% faster
- 🐛 Fixed critical bug affecting Z users
- 📱 Added support for iOS 17

### Full Changelog
See [CHANGELOG.md](./CHANGELOG.md#123---2026-01-21)

### Installation
```bash
flutter pub add my_package:^1.2.3
```

### Upgrade Notes
- Minimum iOS version is now 14.0
- API `oldMethod()` is deprecated, use `newMethod()` instead

### Contributors
- @contributor1
- @contributor2
```

---

## Automated Versioning (CI/CD)

### GitHub Actions

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Extract version from tag
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Setup Flutter
        uses: subosito/flutter-action@v2

      - name: Build
        run: |
          flutter build apk --release \
            --dart-define=GIT_HASH=${{ github.sha }} \
            --dart-define=BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            build/app/outputs/flutter-apk/app-release.apk
          body_path: CHANGELOG.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Usage Examples

```
User: bump version to prepare for release
→ Claude bumps PATCH version, updates files, provides commit/tag commands

User: we added a new feature, what version should this be?
→ Claude recommends MINOR bump, explains reasoning

User: update changelog for release 2.0.0
→ Claude moves Unreleased items, adds version header with date

User: create release checklist
→ Claude provides full pre-release, release, post-release checklist
```
