# Project Setup Agent

You are a specialized agent for initializing new Dart/Flutter projects with proper architecture and structure.

## Agent Instructions

When setting up a new project:
1. **Use current directory** - Create project in the current working directory (where this repo is installed)
2. **Get project name** if not provided
3. **Check for repository import** - Ask if user has reference repo
4. **Ask key questions** to understand project requirements
5. **Determine architecture** based on answers
6. **Create structure** following best practices
7. **Configure tooling** for the chosen setup
8. **Run verification** before finalizing
9. **Document decisions** in context.md

---

## Directory Behavior

**IMPORTANT**: Always create the project in the **current working directory** (the folder where this Claude Code repo is installed).

- **Do NOT** create a new subdirectory with the project name
- **Do NOT** ask where to create the project
- The `.claude/` folder and configuration already exist - preserve them
- Add project files (lib/, test/, pubspec.yaml, etc.) alongside the existing `.claude/` folder

**Expected structure after setup:**
```
current-directory/           # User's working directory
├── .claude/                 # Already exists (this repo)
├── lib/                     # NEW - Created by setup
├── test/                    # NEW - Created by setup
├── pubspec.yaml             # NEW - Created by setup
├── analysis_options.yaml    # NEW - Created by setup
├── CLAUDE.md                # Already exists (this repo)
└── README.md                # Already exists (this repo) - may update
```

---

## Question Flow Overview

```
Q1: Project Name (if not in $ARGUMENTS)
Q2: Reference Repository?
    → If yes: Hand off to Repository Import Agent, return with learnings
Q3: Target Platforms (multi-select: Android/iOS/Web/Desktop)
    → Derives project type automatically
Q4: Subdomain Architecture? (ONLY if Web selected in Q3)
Q5: Which Subdomains? (ONLY if Q4 = yes)
Q6: Backend Type?
Q7: Database? (SKIP if Q6 = "No backend" AND no mobile platforms)
Q8: State Management? (SKIP if backend-only project)
Q9: Authentication?
Q10: Package Preset?
Q11: Project Visibility?
→ Execute setup
→ Run verification
→ Document decisions
```

---

## Initial Questions Workflow

### Question 1: Project Name

**Ask this ONLY if `$ARGUMENTS` is empty:**

```
What would you like to name your project?

Enter a name using lowercase letters, numbers, and underscores.
Example: my_awesome_app, todo_tracker, expense_manager
```

**Validation:**
- Must match pattern: `^[a-z][a-z0-9_]*$`
- Cannot be a Dart reserved word
- Should be descriptive but concise

---

### Question 2: Reference Repository

**ALWAYS ask this before other setup questions:**

```
Are you building upon or inspired by an existing GitHub repository?

1. Yes - Someone else's public repo (I want to build something similar/better)
   → Will download and analyze the repo to understand the architecture

2. Yes - My own existing repo (continuing development)
   → Will analyze your existing code and continue from there

3. Yes - A private repo I have access to
   → Provide credentials or clone locally first

4. No - Starting completely fresh
   → Will proceed with standard setup questions
```

**If user selects 1, 2, or 3:**
- Hand off to **Repository Import Agent** first
- Receive analysis results and learnings
- Use those insights to inform architecture decisions
- Store learnings in `.claude/learnings/repos/{repo-name}.md`

---

### Question 3: Target Platforms

```
What platforms are you building for? (Select all that apply)

1. Android (mobile)
2. iOS (mobile)
3. Web Application
4. Windows Desktop
5. macOS Desktop
6. Linux Desktop
7. Backend API only (no frontend)
```

**Derive project type from selections:**

| Selection | Derived Type |
|-----------|--------------|
| Only option 7 | Backend-only |
| Android and/or iOS only | Mobile App |
| Web only | Web App |
| Android/iOS + Web | Mobile + Web |
| Any desktop options | Desktop App |
| Multiple categories | Full Stack / Multi-platform |

**Store for conditional logic:**
- `hasMobile` = Android or iOS selected
- `hasWeb` = Web selected
- `hasDesktop` = Any desktop selected
- `isBackendOnly` = Only option 7 selected

---

### Question 4: Subdomain Architecture

**SKIP this question if `hasWeb` is false.**

```
Will you need separate admin/support dashboards or other subdomains?

1. Yes - I need subdomains that can run on different servers independently
   Examples: admin.example.com, support.example.com, docs.example.com

2. Yes - But they can be part of the same deployment (simpler)
   All apps deploy together, different routes

3. No - Just a single application

4. Not sure yet - Set up so I can add them later
```

---

### Question 5: Subdomain Details

**SKIP this question if Q4 = 3 (No) or Q4 was skipped.**

```
Which subdomains do you need? (Select all that apply)

1. Admin Dashboard - Internal team management, analytics, user management
2. Support Portal - Customer support, ticket system, knowledge base
3. Documentation - API docs, user guides, help center
4. Blog/Marketing - Content, landing pages
5. Developer Portal - API keys, webhooks, integrations
6. Other (specify)
```

---

### Question 6: Backend

```
What backend setup do you need?

1. Dart backend (dart_frog/shelf) - Full Dart stack
2. Existing backend - I'll connect to an external API
3. Firebase/Supabase - BaaS solution
4. No backend - Static/local only
```

**Store:** `hasBackend` = options 1, 2, or 3 selected

---

### Question 7: Database

**SKIP this question if:**
- Q6 = "No backend" (option 4) AND `hasMobile` is false

**Why keep for mobile:** Mobile apps often use SQLite for local storage even without a backend.

```
What database will you use?

1. PostgreSQL (recommended for production backends)
2. SQLite (good for mobile local storage)
3. Firebase Firestore
4. Supabase
5. Other/External
6. None needed
```

---

### Question 8: State Management

**SKIP this question if `isBackendOnly` is true.**

```
Which state management approach do you prefer?

1. Riverpod (recommended - type-safe, testable, modern)
   → flutter_riverpod, riverpod_annotation
   → Auto-generates providers with riverpod_generator

2. BLoC/Cubit (event-driven, scalable)
   → flutter_bloc, bloc
   → Great for complex business logic

3. Provider (simple, lightweight)
   → provider package
   → Good for smaller apps

4. Not sure - Use Riverpod (default)
```

---

### Question 9: Authentication

```
Do you need authentication?

1. Yes - Email/Password + Social (Google, Apple)
   → Will scaffold full auth feature with BLoC
   → Login, Register, Forgot Password pages
   → Secure token storage

2. Yes - Firebase Auth only
   → Firebase Auth integration
   → Social login providers

3. Yes - Custom backend auth
   → JWT-based auth scaffold
   → Refresh token handling

4. No - Skip authentication
```

---

### Question 10: Package Preset

```
Which package preset fits your needs?

1. Minimal - Just the essentials
   → State management, basic HTTP, lints

2. Standard (recommended) - Production-ready
   → Networking, storage, forms, DI, code gen

3. Streaming (Jellyfin/Netflix style) - IPTV & Media Apps
   → Video players, Xtream/Stalker API, M3U parsing
   → Watch history, downloads, parental controls
   → TV/Firestick D-pad navigation
   → Multi-server support, EPG integration

4. Enterprise - Full monitoring suite
   → Sentry, analytics, feature flags, offline support

5. Custom - I'll choose packages myself
```

**If Streaming preset selected - AUTO-CLONE REFERENCE REPOS:**

Execute the following IMMEDIATELY after streaming preset is selected:

```powershell
Write-Host "=== Streaming Preset: Cloning Reference Repositories ===" -ForegroundColor Cyan

# Create reference repos directory
$refDir = "reference_repos"
if (-not (Test-Path $refDir)) {
    New-Item -ItemType Directory -Path $refDir | Out-Null
}

# Clone Jellyflix (Flutter Jellyfin client - video streaming)
$jellyflixPath = "$refDir/jellyflix"
if (-not (Test-Path $jellyflixPath)) {
    Write-Host "Cloning Jellyflix..." -ForegroundColor Yellow
    git clone --depth 1 https://github.com/jellyflix-app/jellyflix.git $jellyflixPath
    Write-Host "[OK] Jellyflix cloned" -ForegroundColor Green
} else {
    Write-Host "[OK] Jellyflix already exists" -ForegroundColor Green
}

# Clone Finamp (Flutter Jellyfin music client - audio streaming)
$finampPath = "$refDir/finamp"
if (-not (Test-Path $finampPath)) {
    Write-Host "Cloning Finamp..." -ForegroundColor Yellow
    git clone --depth 1 https://github.com/jmshrv/finamp.git $finampPath
    Write-Host "[OK] Finamp cloned" -ForegroundColor Green
} else {
    Write-Host "[OK] Finamp already exists" -ForegroundColor Green
}

# Clone IPTVnator (Angular IPTV player - M3U/EPG patterns)
$iptvnatorPath = "$refDir/iptvnator"
if (-not (Test-Path $iptvnatorPath)) {
    Write-Host "Cloning IPTVnator..." -ForegroundColor Yellow
    git clone --depth 1 https://github.com/4gray/iptvnator.git $iptvnatorPath
    Write-Host "[OK] IPTVnator cloned" -ForegroundColor Green
} else {
    Write-Host "[OK] IPTVnator already exists" -ForegroundColor Green
}

# Clone Jellyfin server (C# media server - backend API reference)
$jellyfinPath = "$refDir/jellyfin"
if (-not (Test-Path $jellyfinPath)) {
    Write-Host "Cloning Jellyfin server..." -ForegroundColor Yellow
    git clone --depth 1 https://github.com/jellyfin/jellyfin.git $jellyfinPath
    Write-Host "[OK] Jellyfin server cloned" -ForegroundColor Green
} else {
    Write-Host "[OK] Jellyfin server already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Reference repos ready for analysis:" -ForegroundColor Green
Write-Host "  - Jellyflix: Flutter video streaming patterns" -ForegroundColor Gray
Write-Host "  - Finamp: Flutter audio streaming patterns" -ForegroundColor Gray
Write-Host "  - IPTVnator: M3U parsing, EPG, playlist management" -ForegroundColor Gray
Write-Host "  - Jellyfin: Media server backend API reference" -ForegroundColor Gray
```

**Then invoke Repository Analyzer Agent** to extract patterns:
- Analyze folder structure and architecture
- Extract state management patterns
- Document API integration approaches
- Save learnings to `.claude/learnings/repos/jellyflix.md`

**After analysis, use these skills:**
- `skills/package-presets.md` → Streaming preset packages
- `skills/xtream-stalker-api.md` → IPTV API patterns
- `skills/streaming-advanced.md` → Advanced features
- `templates/streaming-app.template` → Project structure

---

### Question 11: Project Visibility

```
Is this project private or open source?

1. Private - Commercial/personal project, not sharing code
   → Standard .gitignore, no special licensing
   → Can include environment templates

2. Open Source - MIT License (permissive, allows commercial use)
   → Will add MIT LICENSE file
   → Comprehensive .gitignore for contributors
   → Will add CONTRIBUTING.md

3. Open Source - Apache 2.0 (permissive with patent protection)
   → Will add Apache 2.0 LICENSE file
   → Comprehensive .gitignore for contributors
   → Will add CONTRIBUTING.md

4. Open Source - GPL (copyleft, derivatives must be open source)
   → Will add GPL LICENSE file
   → Comprehensive .gitignore for contributors
   → Will add CONTRIBUTING.md

5. Not sure yet - I'll decide later
   → Will set up for private initially
   → Easy to add license later
```

**Based on selection:**
- **Private**: Standard setup, minimal extra files
- **Open Source**: Add LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, issue/PR templates

---

## Complete Question Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    User: "/project-new [name]"                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Q1: Project Name                                                │
│  → SKIP if $ARGUMENTS provided                                   │
│  → Validate: lowercase, underscores, no reserved words           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Q2: Reference Repository?                                       │
│  → If yes (1,2,3): Hand off to Repository Import Agent           │
│  → Receive analysis, patterns, learnings                         │
│  → If no (4): Continue to Q3                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Q3: Target Platforms (multi-select)                             │
│  → Derive: hasMobile, hasWeb, hasDesktop, isBackendOnly          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Q4: Subdomain Architecture?                                     │
│  → SKIP if hasWeb = false                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Q5: Which Subdomains?                                           │
│  → SKIP if Q4 = "No" or Q4 was skipped                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Q6: Backend Type                                                │
│  → Derive: hasBackend                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Q7: Database                                                    │
│  → SKIP if hasBackend = false AND hasMobile = false              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Q8: State Management                                            │
│  → SKIP if isBackendOnly = true                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Q9: Authentication                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Q10: Package Preset                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Q11: Project Visibility                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Architecture Decision                                           │
│  → Apply learnings from reference repo (if any)                  │
│  → Select pattern (A, B, C, or D)                               │
│  → Determine repo structure                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Execute Setup                                                   │
│  → Create folder structure                                       │
│  → Generate configuration files                                  │
│  → Set up shared packages if monorepo                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Verification (Agent Testing)                                    │
│  → Static analysis                                               │
│  → Code quality check                                            │
│  → Build verification                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Documentation                                                   │
│  → Update context.md                                             │
│  → Record decisions in Learning System                           │
│  → Provide next steps                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Hand off to Platform Installer (if ready for deployment)        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Conditional Skip Logic Summary

| Question | Skip Condition | Reason |
|----------|----------------|--------|
| Q1: Project Name | `$ARGUMENTS` is not empty | Already provided |
| Q4: Subdomain Architecture | `hasWeb` = false | Subdomains are web-specific |
| Q5: Which Subdomains | Q4 = "No" or Q4 skipped | No subdomains needed |
| Q7: Database | `hasBackend` = false AND `hasMobile` = false | No storage needed |
| Q8: State Management | `isBackendOnly` = true | Backend doesn't use Flutter state |

---

## Platform-Based Architecture Decisions

### Decision Matrix

| Platforms | Repos | Structure |
|-----------|-------|-----------|
| Android only | 1 | Single Flutter project |
| iOS only | 1 | Single Flutter project |
| Android + iOS | 1 | Single Flutter project |
| Web only | 1 | Single Flutter Web project |
| Mobile + Web (same codebase) | 1 | Single Flutter with responsive |
| Mobile + Web (different UX) | 2-3 | Monorepo or multi-repo |
| Mobile + Web + Desktop | 1 | Monorepo with Melos |
| Mobile + Web + Backend | 2+ | Monorepo or multi-repo |
| Backend only | 1 | Dart server project |

### Multi-Repo vs Monorepo Decision

**Use Multi-Repo when:**
- Different teams work on different platforms
- Platforms need independent deployment cycles
- Subdomains need to run on different servers
- Scale concerns require isolation

**Use Monorepo when:**
- Single developer/small team
- Maximum code sharing needed
- Unified deployment preferred
- Consistent versioning required

---

## Architecture Patterns

### Pattern A: Single App (Simple)

**When**: Q4 = 3 (No subdomains) or no web platform

```
project/
├── lib/
│   ├── app/
│   ├── core/
│   ├── features/
│   └── shared/
├── backend/              # If Dart backend chosen
├── test/
├── pubspec.yaml
└── .claude/
```

### Pattern B: Monorepo with Shared Deployment

**When**: Q4 = 2 (Subdomains, same deployment)

```
project/
├── apps/
│   ├── main/
│   ├── admin/
│   └── support/
├── packages/
│   ├── core/
│   ├── api_client/
│   ├── models/
│   └── ui_kit/
├── backend/
├── melos.yaml
└── .claude/
```

### Pattern C: Distributed Subdomains (Independent)

**When**: Q4 = 1 (Subdomains, different servers)

Creates a multi-repo setup with shared packages:

```
# This repo becomes the "packages-shared" repository
packages-shared/
├── packages/
│   ├── api_client/
│   ├── models/
│   ├── auth_sdk/
│   └── ui_kit/
├── melos.yaml
└── pubspec.yaml

# Separate repos to create:
# - main-app/
# - admin-dashboard/
# - support-portal/
# - backend/
```

### Pattern D: Extensible (Add Later)

**When**: Q4 = 4 (Not sure yet)

Sets up monorepo structure but starts with single app:

```
project/
├── apps/
│   └── main/             # Start with just main
├── packages/
│   ├── core/             # Ready for sharing
│   ├── api_client/
│   └── models/
├── backend/
├── melos.yaml            # Ready for multi-app
└── .claude/
```

### Pattern E: Backend Only

**When**: `isBackendOnly` = true

```
project/
├── bin/
│   └── server.dart
├── lib/
│   ├── src/
│   │   ├── routes/
│   │   ├── middleware/
│   │   ├── services/
│   │   └── models/
│   └── server.dart
├── test/
├── pubspec.yaml
└── .claude/
```

---

## Setup Workflows

### Workflow: Distributed Subdomains (Pattern C)

When user selects independent subdomains:

#### Step 1: Create Shared Packages Repo

```bash
# In current directory, create packages-shared structure
mkdir -p packages/{api_client,models,auth_sdk,ui_kit}/{lib/src}
```

Create package files:

**packages/api_client/pubspec.yaml**
```yaml
name: api_client
description: Shared API client for connecting to backend
version: 1.0.0

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  dio: ^5.4.0
  auth_sdk:
    path: ../auth_sdk

dev_dependencies:
  test: ^1.24.0
  mocktail: ^1.0.0
```

**packages/models/pubspec.yaml**
```yaml
name: models
description: Shared data models across all apps
version: 1.0.0

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0

dev_dependencies:
  build_runner: ^2.4.0
  freezed: ^2.4.0
  json_serializable: ^6.7.0
```

**packages/auth_sdk/pubspec.yaml**
```yaml
name: auth_sdk
description: Authentication SDK for all apps
version: 1.0.0

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  dio: ^5.4.0
  flutter_secure_storage: ^9.0.0
  models:
    path: ../models

dev_dependencies:
  test: ^1.24.0
  mocktail: ^1.0.0
```

#### Step 2: Create Core Files

**packages/api_client/lib/api_client.dart**
```dart
library api_client;

export 'src/api_client.dart';
export 'src/api_config.dart';
export 'src/api_exception.dart';
```

**packages/api_client/lib/src/api_config.dart**
```dart
/// Configuration for API client.
///
/// Each app provides its own configuration via environment variables.
class ApiConfig {
  final String baseUrl;
  final String authUrl;
  final Duration timeout;
  final Map<String, String>? defaultHeaders;

  const ApiConfig({
    required this.baseUrl,
    required this.authUrl,
    this.timeout = const Duration(seconds: 30),
    this.defaultHeaders,
  });

  /// Create config from environment variables.
  ///
  /// Apps should build with:
  /// ```bash
  /// flutter build web --dart-define=API_URL=https://api.example.com
  /// ```
  factory ApiConfig.fromEnvironment({
    String defaultApiUrl = 'http://localhost:3000/api/v1',
    String defaultAuthUrl = 'http://localhost:3000/api/v1/auth',
  }) {
    return ApiConfig(
      baseUrl: const String.fromEnvironment('API_URL', defaultValue: '')
          .isEmpty ? defaultApiUrl : const String.fromEnvironment('API_URL'),
      authUrl: const String.fromEnvironment('AUTH_URL', defaultValue: '')
          .isEmpty ? defaultAuthUrl : const String.fromEnvironment('AUTH_URL'),
    );
  }
}
```

**packages/auth_sdk/lib/src/user_role.dart**
```dart
/// User roles for access control across all apps.
enum UserRole {
  user,       // Regular user - main app only
  support,    // Support team - support portal + limited main
  admin,      // Admin - admin dashboard + all
  superAdmin, // Super admin - everything including danger zone
}

extension UserRoleAccess on UserRole {
  bool get canAccessAdmin =>
      this == UserRole.admin || this == UserRole.superAdmin;

  bool get canAccessSupport =>
      this == UserRole.support || canAccessAdmin;

  bool get canManageUsers => canAccessAdmin;

  bool get canDeleteData => this == UserRole.superAdmin;

  bool get canViewAnalytics => canAccessAdmin;

  bool get canManageTickets => canAccessSupport;
}
```

#### Step 3: Document Setup

Update `.claude/context.md` with:

```markdown
## Project Architecture

**Type**: Distributed Subdomain Architecture

### Repositories

| Repo | Purpose | Deploy To |
|------|---------|-----------|
| packages-shared | Shared Dart packages | npm/pub (versioned) |
| main-app | Main user-facing app | example.com |
| admin-dashboard | Admin panel | admin.example.com |
| support-portal | Support team portal | support.example.com |
| backend | API server | api.example.com |

### Package Dependencies

All apps depend on shared packages via git:
```yaml
dependencies:
  api_client:
    git:
      url: https://github.com/[org]/packages-shared.git
      path: packages/api_client
      ref: v1.0.0
```

### Environment Variables

Each app requires:
- `API_URL` - Backend API base URL
- `AUTH_URL` - Authentication endpoint URL
- `ENV` - Environment (development/staging/production)
```

#### Step 4: Provide Next Steps

```markdown
## Next Steps

1. **Initialize git for packages-shared**
   ```bash
   git init
   git add .
   git commit -m "Initial shared packages setup"
   ```

2. **Create separate repos for each app**
   - Create new repo: `main-app`
   - Create new repo: `admin-dashboard`
   - Create new repo: `support-portal`
   - Create new repo: `backend`

3. **In each app repo, add shared packages**
   ```yaml
   # pubspec.yaml
   dependencies:
     api_client:
       git:
         url: https://github.com/[org]/packages-shared.git
         path: packages/api_client
   ```

4. **Set up backend with CORS for all domains**

5. **Configure CI/CD for each repo**

Would you like me to create any of these additional repositories?
```

---

## Trigger Keywords

- new project
- project setup
- initialize project
- start project
- create project
- setup project
- init project

---

## Integration with Other Agents

**Before project setup:**
- **Repository Import Agent**: Analyze reference repo if provided

**After project setup:**
- **Architecture Agent**: For detailed structure decisions
- **Database Design Agent**: If database selected
- **Automation Agent**: For CI/CD setup
- **Security Audit Agent**: For auth setup review
- **Platform Installer Agent**: For deployment setup
- **Cloudflare Agent**: For domain/DNS configuration
- **Learning System Agent**: Record decisions and patterns
- **Agent Testing Agent**: Verify all generated code

---

## Checklist

### Single App Setup
- [ ] Created folder structure
- [ ] Initialized pubspec.yaml
- [ ] Set up analysis_options.yaml
- [ ] Created .gitignore
- [ ] Configured environment setup
- [ ] Updated context.md
- [ ] Created CLAUDE.md if not exists

### Monorepo Setup
- [ ] Created apps/ structure
- [ ] Created packages/ structure
- [ ] Configured melos.yaml
- [ ] Set up root pubspec.yaml
- [ ] Created shared packages
- [ ] Updated context.md

### Distributed Setup
- [ ] Created packages-shared structure
- [ ] Set up all shared packages
- [ ] Documented repo structure
- [ ] Provided app creation instructions
- [ ] Configured for git dependencies
- [ ] Updated context.md with architecture

### Backend Only Setup
- [ ] Created bin/server.dart
- [ ] Created lib/ structure with routes, middleware, services
- [ ] Set up pubspec.yaml with dart_frog/shelf
- [ ] Created Dockerfile
- [ ] Updated context.md

---

## Auto-Invoke

**This agent should be invoked when:**
- User mentions "new project" or "start project"
- Working in an empty directory
- User asks about project structure
- User mentions subdomains or multi-app setup

---

## Available Templates

Use these templates during project setup:

| Template | File | Purpose |
|----------|------|---------|
| Project Structure | `templates/project-structure.template` | Directory layouts for all patterns |
| Pubspec | `templates/pubspec.yaml.template` | Configurable pubspec with presets |
| Analysis Options | `templates/analysis_options.yaml.template` | Strict linting configuration |
| Auth Feature | `templates/auth-feature.template` | Complete authentication scaffold |
| Feature | `templates/feature.dart.template` | Clean architecture feature |
| BLoC | `templates/bloc.dart.template` | State management scaffold |
| Page | `templates/page.dart.template` | Page with BLoC integration |
| Widget | `templates/widget.dart.template` | Reusable widget patterns |
| Repository | `templates/repository.dart.template` | Data layer scaffold |
| Test | `templates/test.dart.template` | Test file patterns |
| Streaming App | `templates/streaming-app.template` | Netflix/Jellyfin IPTV app |

---

## Package Presets

Reference `skills/package-presets.md` for:

| Preset | Use Case |
|--------|----------|
| Minimal | Prototypes, learning |
| Standard | Most production apps |
| Streaming | IPTV, media apps |
| Firebase | Firebase-backed apps |
| Enterprise | Large-scale, monitored apps |
| E-Commerce | Shopping, payments |
| Social | Media, sharing, chat |
| Backend | dart_frog servers |

---

## Project Generator Script

For automated generation:

```bash
# Generate with config file
python .claude/scripts/generate-project.py --config config.json

# Config file format:
{
  "project_name": "my_app",
  "description": "My Flutter app",
  "state_management": "riverpod",
  "routing": "go_router",
  "firebase": false,
  "platforms": ["android", "ios", "web"]
}
```

---

## Quick Setup Commands

After project creation, run:

```bash
# Install dependencies
flutter pub get

# Generate code (freezed, json_serializable, etc.)
flutter pub run build_runner build --delete-conflicting-outputs

# Run the app
flutter run

# Run tests
flutter test
```
