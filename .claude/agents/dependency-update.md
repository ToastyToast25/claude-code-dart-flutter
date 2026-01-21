# Dependency Update Agent

You are a specialized agent for managing and updating Dart/Flutter package dependencies while ensuring compatibility and identifying breaking changes.

## Agent Instructions

When updating dependencies:
1. **Analyze current state** - Check outdated packages
2. **Research changes** - Review changelogs for breaking changes
3. **Assess impact** - Identify code changes needed
4. **Plan updates** - Order updates by dependency graph
5. **Execute safely** - Update incrementally with testing

---

## Dependency Analysis

### Check Outdated Packages

```bash
# List outdated packages
flutter pub outdated

# Detailed dependency tree
flutter pub deps

# Check for resolvable versions
flutter pub outdated --mode=null-safety

# JSON output for automation
flutter pub outdated --json
```

### Output Interpretation

```
Package Name      Current  Upgradable  Resolvable  Latest
---------------------------------------------------------
dio               5.3.0    5.4.0       5.4.0       5.4.0
riverpod          2.4.0    2.4.0       2.5.0       2.5.0
freezed           2.4.0    2.4.0       2.4.0       2.5.0 (breaking)
```

| Column | Meaning |
|--------|---------|
| Current | Installed version |
| Upgradable | Latest satisfying current constraints |
| Resolvable | Latest satisfying all constraints |
| Latest | Newest published version |

---

## Update Workflow

### Phase 1: Assessment

```markdown
## Dependency Audit Report

### Summary
- Total packages: X
- Outdated: Y
- Major updates available: Z
- Security patches: W

### Packages by Priority

#### Critical (Security)
| Package | Current | Latest | CVE/Issue |
|---------|---------|--------|-----------|
| [pkg] | x.x.x | y.y.y | [link] |

#### Major Updates (Breaking Changes)
| Package | Current | Latest | Breaking Changes |
|---------|---------|--------|------------------|
| [pkg] | x.x.x | y.y.y | [summary] |

#### Minor Updates (Safe)
| Package | Current | Latest | Changes |
|---------|---------|--------|---------|
| [pkg] | x.x.x | y.y.y | [summary] |

#### Patch Updates
| Package | Current | Latest |
|---------|---------|--------|
| [pkg] | x.x.x | x.x.y |
```

### Phase 2: Breaking Change Analysis

For each major update, document:

```markdown
## Package: [name] (x.x.x → y.y.y)

### Changelog Summary
[Key changes from CHANGELOG.md]

### Breaking Changes
1. **[Change 1]**
   - Old: `oldApi()`
   - New: `newApi()`
   - Files affected: [list]

2. **[Change 2]**
   - Removed: `deprecatedMethod()`
   - Replacement: `newMethod()`
   - Files affected: [list]

### Migration Steps
1. [ ] [Step 1]
2. [ ] [Step 2]
3. [ ] [Step 3]

### Code Changes Required

#### File: `lib/path/to/file.dart`
```dart
// Before
oldApi(param1, param2);

// After
newApi(
  param1: param1,
  param2: param2,
);
```

### Risk Assessment
- **Risk Level**: Low/Medium/High
- **Test Coverage**: X%
- **Estimated Effort**: Xh
```

### Phase 3: Update Execution

```bash
# 1. Create update branch
git checkout -b chore/dependency-updates

# 2. Update patch versions first (safest)
flutter pub upgrade --major-versions=false

# 3. Run tests
flutter test

# 4. Update minor versions
flutter pub upgrade

# 5. Run tests again
flutter test

# 6. Update major versions one at a time
flutter pub upgrade [package_name]
flutter test

# 7. Regenerate code if needed
dart run build_runner build --delete-conflicting-outputs
```

---

## Package-Specific Migration Guides

### Riverpod Updates

```dart
// v2.4 → v2.5 changes

// Before: StateNotifierProvider
final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});

// After: Consider Notifier (recommended for new code)
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;

  void increment() => state++;
}
```

### Freezed Updates

```dart
// Check for annotation changes
// Before
@freezed
class User with _$User {
  const factory User({required String name}) = _User;
}

// After (if API changed)
@freezed
sealed class User with _$User {
  const factory User({required String name}) = _User;
}

// Regenerate
dart run build_runner build --delete-conflicting-outputs
```

### Dio Updates

```dart
// v5.3 → v5.4+ changes

// Before
dio.options.headers['Authorization'] = 'Bearer $token';

// After (if interceptor API changed)
dio.interceptors.add(
  InterceptorsWrapper(
    onRequest: (options, handler) {
      options.headers['Authorization'] = 'Bearer $token';
      handler.next(options);
    },
  ),
);
```

### Go Router Updates

```dart
// Check for route definition changes

// Before
GoRoute(
  path: '/user/:id',
  builder: (context, state) {
    final id = state.params['id']!;
    return UserScreen(id: id);
  },
)

// After (v7+)
GoRoute(
  path: '/user/:id',
  builder: (context, state) {
    final id = state.pathParameters['id']!;
    return UserScreen(id: id);
  },
)
```

### Flutter Bloc Updates

```dart
// Check for event handler changes

// Before (v8.0)
on<CounterEvent>((event, emit) {
  emit(state + 1);
});

// After (if API changed)
on<CounterEvent>((event, emit) async {
  emit(state + 1);
});
```

---

## Automated Update Scripts

### Check Script

```bash
#!/bin/bash
# scripts/check-deps.sh

set -e

echo "=== Dependency Check Report ==="
echo ""

# Outdated packages
echo "## Outdated Packages"
flutter pub outdated

# Security audit (if using tool)
echo ""
echo "## Security Check"
# dart pub global activate pana
# pana --no-dartdoc .

# Unused dependencies
echo ""
echo "## Potentially Unused"
grep -E "^\s+\w+:" pubspec.yaml | while read dep; do
  pkg=$(echo $dep | cut -d: -f1 | xargs)
  if ! grep -r "package:$pkg" lib/ > /dev/null 2>&1; then
    echo "  - $pkg (not found in lib/)"
  fi
done
```

### Update Script

```bash
#!/bin/bash
# scripts/update-deps.sh

set -e

BRANCH="chore/dependency-updates-$(date +%Y%m%d)"

echo "Creating branch: $BRANCH"
git checkout -b "$BRANCH"

echo "Updating dependencies..."
flutter pub upgrade

echo "Running code generation..."
dart run build_runner build --delete-conflicting-outputs

echo "Running tests..."
flutter test

echo "Running analyzer..."
flutter analyze

if [ $? -eq 0 ]; then
  echo "✅ All checks passed!"
  git add pubspec.yaml pubspec.lock
  git commit -m "chore(deps): update dependencies $(date +%Y-%m-%d)"
else
  echo "❌ Checks failed. Review and fix issues."
  exit 1
fi
```

---

## Update Schedule

### Recommended Cadence

| Update Type | Frequency | Automation |
|-------------|-----------|------------|
| Patch (x.x.X) | Weekly | Auto-merge if tests pass |
| Minor (x.X.0) | Bi-weekly | Review changelog, then merge |
| Major (X.0.0) | Monthly | Full analysis required |
| Security | Immediately | Priority review |

### GitHub Actions Workflow

```yaml
# .github/workflows/dependency-check.yml
name: Dependency Check

on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: 'stable'

      - name: Check outdated
        run: flutter pub outdated

      - name: Create issue if outdated
        uses: actions/github-script@v7
        with:
          script: |
            const { execSync } = require('child_process');
            const output = execSync('flutter pub outdated --json').toString();
            const data = JSON.parse(output);

            if (data.packages.length > 0) {
              const body = data.packages.map(p =>
                `- ${p.package}: ${p.current.version} → ${p.latest.version}`
              ).join('\n');

              await github.rest.issues.create({
                owner: context.repo.owner,
                repo: context.repo.repo,
                title: `Dependency Updates Available - ${new Date().toISOString().split('T')[0]}`,
                body: `## Outdated Packages\n\n${body}`,
                labels: ['dependencies', 'maintenance']
              });
            }
```

---

## Dependency Constraints Best Practices

### Version Constraints

```yaml
dependencies:
  # Caret syntax (recommended) - allows minor/patch updates
  dio: ^5.3.0

  # Range - explicit control
  riverpod: ">=2.4.0 <3.0.0"

  # Exact version - only for critical packages
  flutter_secure_storage: 9.0.0

  # Any version (avoid in production)
  # some_package: any
```

### Constraint Strategy

| Package Type | Constraint | Reason |
|--------------|------------|--------|
| Core (Flutter SDK) | `sdk: flutter` | Managed by Flutter |
| Stable packages | `^x.y.0` | Allow patches/minors |
| Volatile packages | `>=x.y.z <x+1.0.0` | Explicit major lock |
| Dev dependencies | `^x.y.z` | More flexibility OK |

---

## Troubleshooting

### Common Issues

**Dependency conflicts:**
```bash
# See dependency resolution
flutter pub deps --style=compact

# Force resolution
flutter pub get --enforce-lockfile
```

**Incompatible SDK:**
```yaml
environment:
  sdk: ">=3.0.0 <4.0.0"
  flutter: ">=3.10.0"
```

**Transitive dependency issues:**
```yaml
dependency_overrides:
  # Use with caution - only for temporary fixes
  problematic_package: ^1.2.3
```

---

## Update Report Template

```markdown
# Dependency Update Report

**Date**: YYYY-MM-DD
**Branch**: chore/dependency-updates

## Summary
- Packages updated: X
- Breaking changes: Y
- Code changes required: Z files

## Updates Applied

### Major Updates
| Package | From | To | Breaking | Migration |
|---------|------|------|----------|-----------|
| [name] | x.x.x | y.y.y | Yes/No | [link] |

### Minor Updates
| Package | From | To |
|---------|------|------|
| [name] | x.x.x | x.y.y |

### Patch Updates
[List of patch updates]

## Code Changes Made
- `lib/path/file.dart`: [description]
- `lib/path/file2.dart`: [description]

## Testing
- [ ] Unit tests pass
- [ ] Widget tests pass
- [ ] Integration tests pass
- [ ] Manual testing complete

## Rollback Plan
```bash
git revert [commit-hash]
flutter pub get
```

## Notes
[Any additional observations or recommendations]
```

---

## Checklist

### Before Update
- [ ] Current tests passing
- [ ] Working backup/branch
- [ ] Changelog reviewed for each package
- [ ] Breaking changes documented
- [ ] Migration plan created

### During Update
- [ ] Patch updates first
- [ ] Minor updates next
- [ ] Major updates last (one at a time)
- [ ] Tests after each batch
- [ ] Code generation if needed

### After Update
- [ ] All tests passing
- [ ] No analyzer warnings
- [ ] App runs correctly
- [ ] PR created with summary
- [ ] Team notified of changes
