# Project Context & Memory

This file maintains project-specific context that persists across sessions. Update this file as the project evolves.

---

## Project Info

| Field | Value |
|-------|-------|
| Name | [Project Name] |
| Type | Flutter App / Dart Package / Backend |
| Flutter Version | [e.g., 3.16.0] |
| Dart SDK | [e.g., >=3.2.0 <4.0.0] |
| State Management | Riverpod |
| Backend | [e.g., Prisma + PostgreSQL] |
| Hosting | [e.g., Cloudflare] |

---

## Environment Configuration

### Environments

| Environment | Purpose | API URL | Database |
|-------------|---------|---------|----------|
| Development | Local development | `http://localhost:3000` | Local PostgreSQL / SQLite |
| Staging | Testing & QA | `https://staging-api.example.com` | Staging PostgreSQL |
| Production | Live users | `https://api.example.com` | Production PostgreSQL |

### Environment Detection

```dart
// Automatic environment detection
enum Environment { development, staging, production }

class AppConfig {
  static late Environment environment;

  static bool get isDevelopment => environment == Environment.development;
  static bool get isStaging => environment == Environment.staging;
  static bool get isProduction => environment == Environment.production;

  // Behavior differences
  static bool get enableLogging => !isProduction;
  static bool get enableDebugBanner => isDevelopment;
  static bool get useMockData => isDevelopment && _useMocks;
  static bool get enableCrashReporting => isProduction || isStaging;
}
```

### Database Per Environment

```
Development:
  - Local PostgreSQL: postgresql://localhost:5432/myapp_dev
  - Or SQLite for simplicity: myapp_dev.db
  - Seed data: Full test dataset
  - Migrations: Run freely, can reset

Staging:
  - Cloud PostgreSQL: staging cluster
  - Seed data: Anonymized production subset
  - Migrations: Test before production

Production:
  - Cloud PostgreSQL: production cluster (replicated)
  - Real user data
  - Migrations: Careful, with rollback plan
  - Backups: Daily automated
```

### Environment-Specific Behavior

| Feature | Development | Staging | Production |
|---------|-------------|---------|------------|
| Logging | Verbose (all) | Info + Errors | Errors only |
| Analytics | Disabled | Enabled (test) | Enabled |
| Crash Reporting | Disabled | Enabled | Enabled |
| Debug Banner | Shown | Hidden | Hidden |
| Mock Data | Available | Disabled | Disabled |
| Rate Limiting | Disabled | Relaxed | Strict |
| Email Sending | Console/Mailtrap | Mailtrap | Real emails |
| Payment Processing | Sandbox | Sandbox | Live |
| SSL | Optional | Required | Required |

---

## API Endpoint Registry

### Current Endpoints

| Method | Path | Environment | Notes |
|--------|------|-------------|-------|
| POST | /auth/login | All | Rate limited in prod |
| POST | /auth/register | All | Email verification in prod |
| GET | /users | All | Paginated |
| GET | /users/:id | All | - |
| POST | /users | All | Admin only in prod |

### API Versioning

- Current version: `v1`
- Base path: `/api/v1/`
- Deprecation policy: Support N-1 version for 6 months

---

## Architecture Decisions

Record important architectural decisions here.

### ADR-001: State Management
**Date**: [Date]
**Status**: Accepted
**Context**: Need type-safe, testable state management
**Decision**: Use Riverpod
**Consequences**: Compile-time safety, no BuildContext requirement

### ADR-002: Project Structure
**Date**: [Date]
**Status**: Accepted
**Context**: Need scalable, maintainable structure
**Decision**: Feature-first with clean architecture layers
**Consequences**: Clear boundaries, testability

### ADR-003: Error Handling
**Date**: [Date]
**Status**: Accepted
**Context**: Need explicit error handling
**Decision**: Either type (fpdart) for Result pattern
**Consequences**: No exceptions for expected failures

### ADR-004: Database Strategy
**Date**: [Date]
**Status**: Accepted
**Context**: Need type-safe database access
**Decision**: Prisma ORM with PostgreSQL
**Consequences**: Easy migrations, good tooling

---

## Project Conventions

### Naming
- Files: `snake_case.dart`
- Classes: `PascalCase`
- Variables/functions: `camelCase`
- Constants: `camelCase` or `SCREAMING_SNAKE_CASE` for env vars
- Private: `_prefixed`
- Feature folders: `snake_case`
- Providers: `entityNameProvider` or `entityNameNotifierProvider`
- Use cases: `VerbNounUseCase`

### File Organization
- One public class per file
- Related private helpers in same file
- Tests mirror source structure

### State
- Use sealed classes for feature states
- Use Result pattern for repository returns
- AsyncValue for provider states

### Imports Order
1. Dart SDK
2. Flutter SDK
3. External packages
4. Project imports (relative)

### Environment Variable Naming
```
[SCOPE]_[CATEGORY]_[NAME]

Examples:
API_URL
API_KEY
DB_HOST
DB_PORT
DB_NAME
FIREBASE_PROJECT_ID
SENTRY_DSN
```

---

## Key Files

| Purpose | Path |
|---------|------|
| Dev entry point | `lib/main_development.dart` |
| Staging entry point | `lib/main_staging.dart` |
| Production entry point | `lib/main_production.dart` |
| App widget | `lib/app/app.dart` |
| Router | `lib/app/router.dart` |
| DI setup | `lib/app/di.dart` |
| Environment config | `lib/core/config/app_config.dart` |
| Environment variables | `lib/core/env/env.dart` |
| Theme | `lib/shared/presentation/theme/` |
| API client | `lib/shared/data/api_client.dart` |
| Database schema | `prisma/schema.prisma` |

---

## External Services

| Service | Purpose | Dev Config | Staging Config | Prod Config |
|---------|---------|------------|----------------|-------------|
| PostgreSQL | Database | localhost:5432 | staging-db-url | prod-db-url |
| Firebase | Auth/Analytics | firebase-dev | firebase-staging | firebase-prod |
| Sentry | Error tracking | Disabled | DSN-staging | DSN-prod |
| Stripe | Payments | Sandbox key | Sandbox key | Live key |
| SendGrid | Email | Console log | Mailtrap | Real sending |

---

## Known Issues & Tech Debt

Track issues to address later.

- [ ] [Issue description] - [Priority: Low/Medium/High]

---

## Team Conventions

### Code Review
- Require approval from 1 reviewer
- All tests must pass
- No analyzer warnings

### Git
- Branch naming: `feature/`, `fix/`, `chore/`
- Commit format: `type(scope): message`
- Squash merge PRs

### Release
- Semantic versioning
- Changelog in CHANGELOG.md
- Tag releases

---

## Session Notes

Use this section for notes during development sessions.

### Session: 2026-01-21
**Focus**: Enhanced agent/skill system with new capabilities
**Completed**:
- Created 33 agents for development workflows (up from 18)
- Created 27 skills for common operations (up from 21)
- Added Repository Import Agent - analyze GitHub repos before building
- Added Platform Installer Agent - full deployment for Linux/Android/iOS/Windows
- Added Learning System Agent - agents learn from mistakes
- Added Agent Testing Agent - verify code before implementation
- Enhanced Cloudflare Agent with full API management
- Enhanced Project Setup with platform detection and repo import
- Added Code Quality Rules (no backward compat, no dead code, etc.)
- Created memory directory structure for persistent learnings
- Created learnings directory for repo analysis and project knowledge

**New Agents Added**:
- Repository Import (`agents/repo-import.md`)
- Platform Installer (`agents/platform-installer.md`)
- Learning System (`agents/learning-system.md`)
- Agent Testing (`agents/agent-testing.md`)

**Directory Structure Added**:
```
.claude/
├── memory/
│   ├── global.md
│   ├── errors/
│   ├── decisions/
│   ├── patterns/
│   └── sessions/
├── learnings/
│   ├── repos/
│   └── project/
└── rules/
    └── code-quality.md
```

**Next**:
- Set up actual environment files for the project
- Configure Firebase per environment
- Create initial database migrations
- Document existing API endpoints
- Test new agent workflows

**Blockers**:
- None

---

## Quick Reference

### Run Commands

```bash
# Development
flutter run -t lib/main_development.dart

# Staging
flutter run --flavor staging -t lib/main_staging.dart

# Production build
flutter build apk --flavor production -t lib/main_production.dart

# Generate code
dart run build_runner build --delete-conflicting-outputs

# Database migrations (development)
npx prisma migrate dev --name [migration_name]

# Database migrations (production)
npx prisma migrate deploy
```

### Environment Checklist

Before deploying to a new environment:
- [ ] Environment variables configured
- [ ] Database created and migrated
- [ ] Firebase project configured
- [ ] SSL certificates in place
- [ ] Monitoring/logging enabled
- [ ] Backup strategy confirmed
