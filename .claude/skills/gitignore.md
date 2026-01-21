---
description: "Maintains and updates .gitignore for Dart/Flutter projects"
globs: [".gitignore", "**/.gitignore"]
alwaysApply: false
---

# Skill: Gitignore Management

Maintain and update the project's .gitignore file.

## Usage

When the user adds new tools, packages, or file types that should be ignored, update the .gitignore accordingly.

## Auto-Update Triggers

Update .gitignore when:
- New package added that generates files (e.g., build_runner, freezed)
- New platform added (iOS, Android, Web, Desktop)
- New tooling added (Firebase, Fastlane, Docker)
- New IDE or editor mentioned
- Secrets or credentials files created
- Database files introduced

## Gitignore Structure

The .gitignore is organized into sections:

```
# DART & FLUTTER
# IDE & EDITORS
# OPERATING SYSTEMS
# ENVIRONMENT & SECRETS
# PLATFORM SPECIFIC
# TESTING & COVERAGE
# CODE GENERATION
# DEPENDENCIES & PACKAGES
# DATABASES
# LOGS & TEMPORARY FILES
# DOCUMENTATION
# CI/CD & DEPLOYMENT
# MISCELLANEOUS
# PROJECT SPECIFIC
```

## Adding New Entries

1. **Find the correct section** based on the category
2. **Add entries alphabetically** within the section
3. **Use comments** for non-obvious entries
4. **Add negation patterns** (`!`) for files that should be tracked

### Example Updates

**When user adds Firebase:**
```gitignore
# Firebase
.firebase/
firebase-debug.log
.firebaserc
```

**When user adds Docker:**
```gitignore
# Docker
.docker/
docker-compose.override.yml
```

**When user adds code generation:**
```gitignore
# Uncomment to ignore generated files
# *.g.dart
# *.freezed.dart
```

**When user adds Prisma:**
```gitignore
# Prisma
prisma/migrations/**/migration_lock.toml
```

## Common Patterns

### Ignore all except specific files
```gitignore
folder/*
!folder/.gitkeep
!folder/important.txt
```

### Ignore by extension
```gitignore
*.log
*.tmp
```

### Ignore in all directories
```gitignore
**/node_modules/
**/.DS_Store
```

### Ignore only in root
```gitignore
/build/
/.env
```

## Quick Reference

| Tool/Package | Files to Ignore |
|--------------|-----------------|
| build_runner | `.build/` |
| freezed | `*.freezed.dart` (optional) |
| json_serializable | `*.g.dart` (optional) |
| auto_route | `*.gr.dart` (optional) |
| mockito | `*.mocks.dart` (optional) |
| hive | `*.hive`, `*.lock` |
| firebase | `.firebase/`, `firebase-debug.log` |
| fastlane | `fastlane/report.xml`, etc. |
| prisma | `migration_lock.toml` |
| docker | `docker-compose.override.yml` |

## Validation

After updating, verify:
- [ ] No sensitive files are tracked
- [ ] Build outputs are ignored
- [ ] Generated files policy is consistent
- [ ] Platform-specific files for all target platforms
- [ ] IDE files don't pollute the repo
