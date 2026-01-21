# Release Command

Prepare and execute a new release with version bump, changelog, and git operations.

## Usage

```
/project:release [version_type]
```

## Arguments

`$ARGUMENTS` can be:
- `major` - Breaking changes (1.0.0 → 2.0.0)
- `minor` - New features (1.0.0 → 1.1.0)
- `patch` - Bug fixes (1.0.0 → 1.0.1)
- `1.2.3` - Specific version number
- (empty) - Will ask which type

## Workflow

### Step 1: Determine Version

If no argument provided, ask:
```
What type of release is this?

1. MAJOR (breaking changes) - Current: 1.2.3 → 2.0.0
2. MINOR (new features) - Current: 1.2.3 → 1.3.0
3. PATCH (bug fixes) - Current: 1.2.3 → 1.2.4
4. Specific version - Enter manually
```

### Step 2: Pre-Release Checks

Run these checks before proceeding:

```bash
# Check git status
git status

# Run tests
flutter test

# Run analyzer
flutter analyze

# Check formatting
dart format --set-exit-if-changed .
```

**If any check fails, stop and report the issue.**

### Step 3: Review Changes for Changelog

```bash
# Show commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Show changed files
git diff $(git describe --tags --abbrev=0) --stat
```

Categorize changes into:
- **Added**: New features
- **Changed**: Changes to existing features
- **Fixed**: Bug fixes
- **Removed**: Removed features
- **Security**: Security fixes

### Step 4: Update Files

1. **pubspec.yaml** - Bump version
2. **CHANGELOG.md** - Move Unreleased to new version section
3. **lib/core/version.dart** - Update if exists

### Step 5: Commit and Tag

```bash
# Commit version bump
git add .
git commit -m "chore: release v${VERSION}"

# Create annotated tag
git tag -a v${VERSION} -m "Release v${VERSION}

${CHANGELOG_SUMMARY}"
```

### Step 6: Push and Create Release

```bash
# Push with tags
git push origin main --tags

# Create GitHub release
gh release create v${VERSION} \
  --title "v${VERSION}" \
  --notes "${RELEASE_NOTES}" \
  --latest
```

## Example Session

```
User: /project:release minor

Claude:
📋 Pre-Release Checks
✅ Tests pass (42 tests)
✅ No analyzer warnings
✅ Code formatted

📝 Changes since v1.2.0:
- feat(auth): add biometric login
- feat(profile): add avatar upload
- fix(cart): resolve quantity update bug
- chore(deps): update riverpod to 2.4.0

📦 Version: 1.2.0 → 1.3.0

I'll update:
1. pubspec.yaml (version: 1.3.0+24)
2. CHANGELOG.md (add v1.3.0 section)

Proceed with release? [Yes/No]
```

## Post-Release

After release:
1. Monitor crash reports
2. Check app store processing (if applicable)
3. Announce release (if applicable)
4. Start new development cycle

## Related

- **Skill**: `skills/versioning.md`
- **Agent**: `agents/github-workflow.md`
- **File**: `CHANGELOG.md`
