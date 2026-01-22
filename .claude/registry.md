# Claude Registry

Central registry of all agents and skills. Consult this file on each request to determine which agent(s) or skill(s) to load based on trigger keywords.

**Project Context**: See `context.md` for project-specific decisions, conventions, and session memory.

---

## Agent Index

| Agent | File | Trigger Keywords |
|-------|------|------------------|
| Orchestration | `agents/orchestration.md` | agent workflow, how agents work, agent handoff, which agent |
| Project Setup | `agents/project-setup.md` | new project, init project, start project, setup project, create project |
| Repository Import | `agents/repo-import.md` | import repo, clone repository, analyze github, based on repo, modify existing, build like, similar to, reference project |
| Platform Installer | `agents/platform-installer.md` | install, server setup, docker install, nginx install, cloudflared, ssl cert, android build, ios build, windows setup |
| Learning System | `agents/learning-system.md` | remember this, learn from, save pattern, what went wrong, don't do that again |
| Agent Testing | `agents/agent-testing.md` | verify code, test agent code, check quality, run verification, validate implementation |
| Dev Environment | `agents/dev-environment.md` | dev environment, setup docker, docker containers, local development, database setup, postgres setup |
| GitHub Setup | `agents/github-setup.md` | github setup, setup github, git setup, configure git, ssh keys, create repository |
| Planning | `agents/planning.md` | plan, design, architect, break down, scope |
| Code Review | `agents/code-review.md` | review, PR review, code review, check code |
| Test Writer | `agents/test-writer.md` | write tests, add tests, test coverage, unit test |
| Refactor | `agents/refactor.md` | refactor, improve, clean up, optimize code |
| Architecture | `agents/architecture.md` | architecture, structure, layers, organize |
| Automation | `agents/automation.md` | script, automate, CI/CD, pipeline, build script |
| GitHub Workflow | `agents/github-workflow.md` | deploy, push, pull, PR, git, commit, branch |
| Security Audit | `agents/security-audit.md` | security, vulnerabilities, audit, secure, OWASP |
| Database Design | `agents/database-design.md` | database, schema, migration, Prisma, tables |
| API Design | `agents/api-design.md` | API, endpoints, REST, routes, backend |
| E2E Testing | `agents/e2e-testing.md` | E2E, Playwright, browser test, integration test |
| Cloudflare | `agents/cloudflare.md` | Cloudflare, DNS, CDN, WAF, SSL, caching, domain management, cloudflare api |
| Dependency Update | `agents/dependency-update.md` | update packages, outdated, upgrade, dependencies, pub upgrade |
| Debugging | `agents/debugging.md` | error, bug, debug, fix error, exception, crash |
| Performance | `agents/performance.md` | slow, performance, optimize, profiling, memory, jank |
| Documentation | `agents/documentation.md` | document, docs, README, API docs, comments |
| SEO | `agents/seo.md` | SEO, search engine, Google, Bing, sitemap, meta tags, indexing |
| Compliance | `agents/compliance.md` | GDPR, privacy, accessibility, WCAG, terms, cookies, compliance, legal |
| Scheduled Tasks | `agents/scheduled-tasks.md` | cron, cron job, scheduled task, background job, job queue, systemd timer |
| Deployment | `agents/deployment.md` | deploy, ubuntu, linux server, nginx, production deploy, server setup |
| Monitoring | `agents/monitoring.md` | logging, metrics, Sentry, Crashlytics, error tracking, observability, alerts |
| State Management | `agents/state-management.md` | state management, provider, riverpod, bloc, cubit, getx, state |
| Testing Strategy | `agents/testing-strategy.md` | testing strategy, test coverage, test architecture, testing pyramid |
| Mobile | `agents/mobile.md` | platform channel, native code, iOS, Android, push notifications, deep links, biometrics |
| Internationalization | `agents/internationalization.md` | i18n, l10n, localization, translations, RTL, multi-language, locale |
| Migration | `agents/migration.md` | flutter upgrade, dart upgrade, migration, null safety, version upgrade |
| Repository Analyzer | `agents/repo-analyzer.md` | analyze repo, jellyflix, jellyfin, extract patterns, reference architecture, clone repos |

---

## Auto-Invoke Rules

### Single Agent Selection

When the user's request matches trigger keywords, load the corresponding agent file and follow its instructions.

```
User Request → Match Keywords → Load Agent → Execute
```

### Priority Order

If multiple agents could apply, use this priority:

1. **Project Setup** - Always first for new projects or empty directories
2. **Planning** - For new features/large tasks
3. **Security Audit** - For any security-related concerns
4. **Specific Domain** - API, Database, Cloudflare, etc.
5. **Implementation** - Refactor, Test Writer, Code Review
6. **Workflow** - GitHub, Automation

### Multi-Agent Workflows

| Scenario | Agent Sequence |
|----------|----------------|
| Fresh Dev Setup | Dev Environment → GitHub Setup → Project Setup |
| New Project | Repository Import (optional) → Project Setup → Architecture → Database Design → Automation → Agent Testing |
| New Project (Subdomains) | Repository Import (optional) → Project Setup → Architecture → API Design → Database Design → Automation → Agent Testing |
| New Project (Multi-Platform) | Repository Import → Project Setup → Platform Installer → Cloudflare → Agent Testing |
| New Feature | Planning → Architecture → Implementation → Test Writer → Code Review → Agent Testing |
| Bug Fix | Debugging → Test Writer → Code Review → GitHub Workflow → Learning System |
| Pre-Release | Security Audit → Performance → Code Review → Automation → GitHub Workflow → Agent Testing |
| New API | Planning → API Design → Database Design → Test Writer → Documentation → Agent Testing |
| Refactoring | Planning → Refactor → Test Writer → Code Review → Agent Testing |
| Infrastructure | Cloudflare → Platform Installer → Security Audit → Automation |
| Maintenance | Dependency Update → Test Writer → Code Review → GitHub Workflow |
| Performance Issue | Performance → Refactor → Test Writer → Learning System |
| Error Investigation | Debugging → Code Review → Test Writer → Learning System |
| Website Launch | SEO → Compliance → Security Audit → Performance → Cloudflare |
| App Store Submission | Compliance → Security Audit → Documentation |
| Production Deployment | Deployment → Platform Installer → Scheduled Tasks → Security Audit → Cloudflare |
| Server Setup | Dev Environment → Platform Installer → Deployment → Scheduled Tasks → Automation |
| Flutter Upgrade | Migration → Testing Strategy → Code Review → Agent Testing |
| Add Monitoring | Monitoring → Performance → Deployment |
| Mobile Feature | Mobile → Testing Strategy → Security Audit |
| Add i18n | Internationalization → Testing Strategy → Documentation |
| State Refactor | State Management → Testing Strategy → Code Review |
| Rollback | Debugging → Deployment → Monitoring → Learning System |
| Hotfix | Debugging → Test Writer → Deployment → Learning System |
| Build Similar App | Repository Import → Project Setup → Architecture → Platform Installer |
| Deploy Full Stack | Platform Installer → Cloudflare → Deployment → Monitoring |
| Build Streaming App | Repository Analyzer → Project Setup (Streaming preset) → Architecture → Platform Installer |

---

## Agent Definitions

### Repository Import Agent
**File**: `agents/repo-import.md`
**Purpose**: Import, analyze, and learn from existing GitHub repositories
**Invoke When**:
- User wants to build something similar to an existing repo
- User has a reference repo they want to heavily modify
- User mentions "build like X" or "similar to X"
- Analyzing external projects for patterns

**Question Flow**:
1. Repository source (someone else's, own, private, fresh)
2. Repository URL
3. Download location
4. Target platforms
5. Relationship to source (heavy mod, inspiration, fork, rewrite)

**Outputs**:
- Cloned repository files
- Repository analysis document
- Technology identification
- Pattern extraction
- Learnings for future reference
- Architecture recommendations

---

### Platform Installer Agent
**File**: `agents/platform-installer.md`
**Purpose**: Install and configure deployments across all platforms
**Invoke When**:
- Setting up Linux production server
- Installing Docker, Nginx, Apache
- Configuring Cloudflared tunnels
- SSL certificate setup
- Building for Android/iOS
- Windows development setup

**Covers**:
- Ubuntu server setup (Dart SDK, dependencies)
- Docker installation and Docker Compose
- Nginx reverse proxy with SSL
- Cloudflared tunnel configuration
- Let's Encrypt/Certbot SSL
- Android APK builds and installation
- iOS builds (requires Mac)
- Windows 11 development with WSL2
- Systemd service configuration
- Health checks and monitoring

**Outputs**:
- Setup scripts (bash, PowerShell)
- Docker Compose configurations
- Nginx configuration files
- Systemd service files
- SSL configuration
- Build scripts
- Update/deployment scripts

---

### Learning System Agent
**File**: `agents/learning-system.md`
**Purpose**: Manage agent learning, memory persistence, and continuous improvement
**Invoke When**:
- An error is fixed and should be remembered
- A successful pattern is discovered
- User provides feedback on agent behavior
- Decisions need to be recorded for future reference
- Session learnings need to be saved

**Memory Structure**:
- `.claude/memory/global.md` - Cross-agent learnings
- `.claude/memory/errors/` - Error patterns and fixes
- `.claude/memory/decisions/` - Architectural decisions
- `.claude/memory/patterns/` - Successful patterns
- `.claude/memory/sessions/` - Session-specific learnings

**Capabilities**:
- Record errors and their fixes
- Store architectural decisions with rationale
- Save successful code patterns
- Cross-reference related learnings
- Search memory before starting tasks
- Session start/end protocols

---

### Agent Testing Agent
**File**: `agents/agent-testing.md`
**Purpose**: Verify, test, and validate all agent-generated code before implementation
**Invoke When**:
- After any agent generates code
- Before code is committed
- Before merging changes
- User requests code verification

**Verification Pipeline**:
1. Static Analysis - Dart analyzer, lints
2. Code Quality Check - No backward compat, no dead code, no TODOs
3. Unit Tests - Generate if missing, run existing
4. Integration Tests - Check for breaking changes
5. Build Verification - All platform builds

**Outputs**:
- Quality reports
- Test results
- Breaking change analysis
- Build verification
- Pass/fail status

---

### Dev Environment Agent
**File**: `agents/dev-environment.md`
**Purpose**: Set up local development environment with Docker containers on Windows 11
**Invoke When**:
- User needs to set up Docker/containers
- Database setup for local development
- User mentions "dev environment" or "local setup"
- Starting fresh on Windows 11

**Question Flow**:
1. Current setup (fresh/have Docker/have containers/not sure)
2. Services needed (PostgreSQL/Redis/MinIO/MySQL/MongoDB)
3. Additional tools (pgAdmin/Redis Commander/Mailhog/Adminer)

**Outputs**:
- Docker Desktop installation guide
- docker-compose.yml configuration
- Database initialization scripts
- Environment variables (.env)
- Connection verification steps
- PowerShell setup scripts

**Services Provided**:
- PostgreSQL with pgAdmin
- Redis with Redis Commander
- MinIO (S3-compatible storage)
- Mailhog (email testing)
- MySQL/MongoDB alternatives

---

### GitHub Setup Agent
**File**: `agents/github-setup.md`
**Purpose**: Configure Git, GitHub authentication, and repository setup
**Invoke When**:
- User needs to set up Git
- GitHub authentication (SSH/token)
- Creating new repository
- Setting up branch protection
- Configuring GitHub Actions

**Question Flow**:
1. Current setup (fresh/have Git/have account/have repo)
2. Authentication method (SSH/HTTPS token/GitHub CLI)
3. Repository type (public/private/organization)
4. Workflow needs (basic/standard CI/full CI-CD)

**Outputs**:
- Git installation guide
- Git configuration commands
- SSH key generation and setup
- GitHub CLI setup
- Repository creation
- Branch protection rules
- GitHub Actions workflows
- Issue/PR templates
- CODEOWNERS configuration

---

### Project Setup Agent
**File**: `agents/project-setup.md`
**Purpose**: Initialize new projects with proper architecture and structure
**Invoke When**:
- User says "new project", "start project", "create project"
- Working in an empty or near-empty directory
- User asks about project structure for a new app
- User mentions needing subdomains or multi-app setup

**Question Flow**:
1. Project type (mobile/web/full-stack)
2. Subdomain architecture (independent/shared/none/extensible)
3. Which subdomains (admin/support/docs/blog/developer)
4. Backend type (Dart/external/BaaS/none)
5. Database choice

**Architecture Patterns**:
- **Single App**: Simple folder structure
- **Monorepo Shared**: Multiple apps, single deployment
- **Distributed**: Independent repos, shared packages via git
- **Extensible**: Start simple, ready for expansion

**Outputs**:
- Project structure
- Shared packages (if multi-app)
- Configuration files
- Updated context.md
- Next steps documentation

---

### Planning Agent
**File**: `agents/planning.md`
**Purpose**: Plan and orchestrate complex development tasks
**Invoke When**:
- User asks to plan, design, or architect a feature
- Task requires breaking down into subtasks
- Multiple approaches need evaluation
- Estimation or timeline discussion needed

**Outputs**:
- Task breakdown with dependencies
- Risk assessment
- Milestone definitions
- Architecture decisions

---

### Code Review Agent
**File**: `agents/code-review.md`
**Purpose**: Review code for quality, security, and best practices
**Invoke When**:
- User asks to review code or a PR
- Before merging significant changes
- After implementation is complete
- User asks "is this code good?"

**Checks**:
- Dart/Flutter best practices
- Null safety
- Error handling
- Performance
- Security vulnerabilities
- Platform-specific issues (iOS/Android)

---

### Test Writer Agent
**File**: `agents/test-writer.md`
**Purpose**: Write comprehensive tests for Dart/Flutter code
**Invoke When**:
- User asks to write or add tests
- After implementing new features
- Test coverage is mentioned
- TDD approach requested

**Outputs**:
- Unit tests
- Widget tests
- Integration tests
- Mock implementations

---

### Refactor Agent
**File**: `agents/refactor.md`
**Purpose**: Improve code structure without changing behavior
**Invoke When**:
- User asks to refactor or improve code
- Code smells are identified
- Performance optimization needed
- Technical debt reduction

**Focus**:
- Extract methods/classes
- Simplify logic
- Remove duplication
- Improve naming

---

### Architecture Agent
**File**: `agents/architecture.md`
**Purpose**: Design system structure and component organization
**Invoke When**:
- Setting up new project structure
- Major feature requiring new modules
- Questions about layers or organization
- Dependency injection setup

**Outputs**:
- Folder structure
- Layer definitions
- Dependency graphs
- Interface designs

---

### Automation Agent
**File**: `agents/automation.md`
**Purpose**: Create build scripts, CI/CD pipelines, and automated workflows
**Invoke When**:
- User asks for scripts or automation
- CI/CD pipeline needed
- Build process setup
- Deployment automation

**Outputs**:
- Shell scripts
- GitHub Actions workflows
- Makefiles
- Docker configurations

---

### GitHub Workflow Agent
**File**: `agents/github-workflow.md`
**Purpose**: Manage Git operations and GitHub workflows
**Invoke When**:
- Committing, pushing, or PR creation
- Branch management
- Release process
- Git workflow questions

**Handles**:
- Commit message formatting
- PR descriptions
- Branch naming
- GitHub Actions
- Release tagging

---

### Security Audit Agent
**File**: `agents/security-audit.md`
**Purpose**: Identify and fix security vulnerabilities
**Invoke When**:
- Security review requested
- Handling sensitive data
- Authentication/authorization code
- Before production release

**Checks**:
- OWASP vulnerabilities
- Secure storage
- API security
- Platform security (iOS/Android)
- Dependency vulnerabilities

---

### Database Design Agent
**File**: `agents/database-design.md`
**Purpose**: Design database schemas and Prisma configurations
**Invoke When**:
- Database schema design
- Prisma setup or migrations
- Data modeling questions
- Query optimization

**Outputs**:
- Prisma schema files
- Migration scripts
- Index recommendations
- Relationship definitions

---

### API Design Agent
**File**: `agents/api-design.md`
**Purpose**: Design RESTful APIs and backend services
**Invoke When**:
- API endpoint design
- Backend architecture
- Request/response modeling
- API documentation

**Outputs**:
- Endpoint definitions
- DTO models
- Error handling patterns
- Authentication middleware

---

### E2E Testing Agent
**File**: `agents/e2e-testing.md`
**Purpose**: Create end-to-end tests using Playwright
**Invoke When**:
- E2E or browser testing
- Playwright test creation
- User flow testing
- Integration testing

**Outputs**:
- Playwright test scripts
- Page object models
- Test utilities
- CI integration

---

### Cloudflare Agent
**File**: `agents/cloudflare.md`
**Purpose**: Configure Cloudflare services and manage domains programmatically
**Invoke When**:
- DNS configuration
- SSL/TLS setup
- CDN and caching
- WAF rules
- Cloudflare Workers
- Domain management via API
- Cloudflare Tunnel setup

**Capabilities**:
- Zone management (list, get, add)
- DNS record management (CRUD)
- SSL/TLS configuration
- Cache management (purge)
- Tunnel management
- Analytics retrieval
- Automatic domain setup

**Outputs**:
- DNS records
- Page rules
- Worker scripts
- Security configurations
- Dart CloudflareService class
- Tunnel configurations

**Integration**:
- Works with Platform Installer for deployment
- Automatic SSL setup
- Tunnel configuration for secure access

---

### Dependency Update Agent
**File**: `agents/dependency-update.md`
**Purpose**: Manage and update package dependencies safely
**Invoke When**:
- User asks to update or upgrade packages
- Checking for outdated dependencies
- Security patches needed
- Preparing for major version updates
- Maintenance tasks

**Workflow**:
1. Analyze current dependencies
2. Check for outdated packages
3. Research breaking changes
4. Plan update order
5. Execute updates incrementally
6. Run tests after each batch

**Outputs**:
- Dependency audit report
- Breaking change analysis
- Migration guides
- Update scripts
- PR with changes summary

---

### Debugging Agent
**File**: `agents/debugging.md`
**Purpose**: Diagnose and resolve errors in Dart/Flutter applications
**Invoke When**:
- Runtime errors or exceptions
- Build/compile errors
- Unexpected behavior
- Crash investigation
- Error messages to interpret

**Workflow**:
1. Reproduce the error
2. Isolate the source
3. Diagnose root cause
4. Apply targeted fix
5. Verify fix works
6. Add tests to prevent recurrence

---

### Performance Agent
**File**: `agents/performance.md`
**Purpose**: Analyze and optimize application performance
**Invoke When**:
- App is slow or laggy
- Memory issues suspected
- Frame drops/jank
- Build performance
- Optimization requests

**Checks**:
- Widget rebuild frequency
- Memory leaks
- Image optimization
- List performance
- State management efficiency
- Network requests

---

### Documentation Agent
**File**: `agents/documentation.md`
**Purpose**: Create and maintain project documentation
**Invoke When**:
- README updates needed
- API documentation
- Code comments
- Architecture docs
- Changelog updates

**Outputs**:
- README.md
- API documentation
- Code comments
- Architecture Decision Records
- CHANGELOG entries

---

### SEO Agent
**File**: `agents/seo.md`
**Purpose**: Optimize web applications for search engines
**Invoke When**:
- Setting up Flutter web app
- Improving search rankings
- Adding meta tags or structured data
- Creating sitemaps
- Configuring Google/Bing webmaster tools

**Covers**:
- Meta tags (title, description, Open Graph, Twitter)
- Structured data (JSON-LD, Schema.org)
- Sitemap generation
- robots.txt configuration
- Google Search Console setup
- Bing Webmaster Tools / IndexNow
- Core Web Vitals optimization
- URL structure best practices

---

### Compliance Agent
**File**: `agents/compliance.md`
**Purpose**: Ensure legal and regulatory compliance
**Invoke When**:
- Privacy policy needed
- Cookie consent implementation
- Accessibility requirements
- App store submission
- GDPR/CCPA compliance
- Terms of service drafting

**Covers**:
- GDPR (EU privacy)
- CCPA (California privacy)
- WCAG 2.1 (Accessibility)
- Apple App Store guidelines
- Google Play Store policies
- Cookie consent banners
- Age verification (COPPA)
- Data security requirements
- Privacy policy templates
- Terms of service templates

---

### Scheduled Tasks Agent
**File**: `agents/scheduled-tasks.md`
**Purpose**: Set up cron jobs, background tasks, and job queues
**Invoke When**:
- User needs scheduled/recurring tasks
- Background job processing
- Cron job setup on Linux
- Systemd timer configuration
- Job queue implementation

**Covers**:
- Linux cron jobs with proper syntax
- Systemd timers (modern alternative)
- Redis-based job queues (Dart)
- In-app schedulers
- GitHub Actions scheduled workflows
- Monitoring and alerting for jobs
- Common tasks (backups, email, cleanup)

**Outputs**:
- Cron job configurations
- Systemd timer/service files
- Dart scheduled task scripts
- Job queue implementations
- Monitoring setup

---

### Deployment Agent
**File**: `agents/deployment.md`
**Purpose**: Deploy Dart/Flutter applications to Ubuntu Linux servers
**Invoke When**:
- Deploying to production server
- Ubuntu server setup
- Nginx configuration
- SSL certificate setup
- Systemd service configuration
- CI/CD for deployment

**Covers**:
- Fresh Ubuntu server setup
- Dart SDK installation
- Nginx reverse proxy configuration
- SSL with Let's Encrypt/Certbot
- Systemd services for Dart backend
- Zero-downtime deployments
- Docker deployment option
- GitHub Actions CI/CD pipelines
- Health checks and monitoring

**Outputs**:
- Server setup scripts
- Nginx configuration files
- Systemd service files
- Deployment scripts (manual & automated)
- GitHub Actions workflows
- Docker configuration

---

### Monitoring Agent
**File**: `agents/monitoring.md`
**Purpose**: Set up logging, metrics, error tracking, and observability
**Invoke When**:
- Setting up crash reporting (Sentry, Crashlytics)
- Adding logging infrastructure
- Performance monitoring
- Alert configuration
- Metrics collection

**Covers**:
- Firebase Crashlytics (mobile)
- Sentry (cross-platform)
- Structured logging
- Performance tracing
- Health check endpoints
- Prometheus metrics (backend)
- Alert channels (Slack, email)

**Outputs**:
- Crash reporting setup
- Logger service implementation
- Performance monitoring code
- Health check endpoints
- Alert configurations

---

### State Management Agent
**File**: `agents/state-management.md`
**Purpose**: Implement and advise on state management patterns
**Invoke When**:
- Choosing state management solution
- Migrating between solutions
- State management architecture questions
- Provider/Riverpod/BLoC implementation

**Covers**:
- Provider (simple apps)
- Riverpod (type-safe, testable)
- BLoC/Cubit (event-driven)
- Best practices and patterns
- Testing state logic

**Question Flow**:
1. Current state management
2. App complexity level
3. Team preference

---

### Testing Strategy Agent
**File**: `agents/testing-strategy.md`
**Purpose**: Design comprehensive testing strategies
**Invoke When**:
- Planning test architecture
- Setting up test infrastructure
- Coverage goals discussion
- Test utilities needed

**Covers**:
- Testing pyramid (unit/widget/integration/E2E)
- Test organization and structure
- Mock generation
- Fixtures and test data
- CI/CD test integration
- Coverage thresholds

**Outputs**:
- Test folder structure
- Test utilities and helpers
- Mock classes
- Fixtures
- CI test configuration

---

### Mobile Agent
**File**: `agents/mobile.md`
**Purpose**: iOS and Android specific implementations
**Invoke When**:
- Platform channel implementation
- Push notification setup
- Deep linking configuration
- App signing for release
- Biometric authentication
- Native integrations

**Covers**:
- Platform channels (Swift/Kotlin)
- Firebase Cloud Messaging
- Universal Links / App Links
- Keystore and signing
- Face ID / Touch ID / Fingerprint
- Permissions handling

**Outputs**:
- Platform channel code (Dart + native)
- Push notification service
- Deep link handling
- Signing configuration
- Native integration code

---

### Internationalization Agent
**File**: `agents/internationalization.md`
**Purpose**: Full i18n/l10n implementation
**Invoke When**:
- Adding multi-language support
- RTL language support needed
- Translation workflow setup
- Locale-aware formatting

**Covers**:
- Flutter localization setup
- ARB file management
- RTL support
- Date/number formatting
- Translation management
- Locale switching

**Question Flow**:
1. Languages needed
2. Content type (UI/dynamic/legal)
3. RTL support needed
4. Translation management approach

**Outputs**:
- l10n.yaml configuration
- ARB files for all locales
- Locale provider
- Formatting utilities
- Translation scripts

---

### Migration Agent
**File**: `agents/migration.md`
**Purpose**: Handle Flutter/Dart upgrades and architecture migrations
**Invoke When**:
- Flutter SDK upgrade
- Dart version upgrade
- Major package upgrades
- State management migration
- Architecture refactoring
- Null safety migration

**Covers**:
- Flutter upgrade process
- Breaking changes resolution
- Provider → Riverpod migration
- BLoC version upgrades
- Architecture migrations
- Null safety migration

**Outputs**:
- Migration plan
- Breaking change fixes
- Migration scripts
- Updated code patterns
- Test verification

---

### Repository Analyzer Agent
**File**: `agents/repo-analyzer.md`
**Purpose**: Analyze external Flutter/Dart repositories to extract patterns for hybrid app development
**Invoke When**:
- Building a streaming/media app
- Need to analyze Jellyflix or Jellyfin architecture
- Extracting patterns from reference repositories
- Designing hybrid app combining multiple sources
- User mentions "analyze repo" or "extract patterns"

**Workflow**:
1. Clone reference repositories to `reference_repos/`
2. Analyze architecture, state management, API patterns
3. Document reusable components and widgets
4. Identify patterns to adopt and avoid
5. Generate architecture recommendations

**Reference Repos**:
- Jellyflix: `https://github.com/jellyflix-app/jellyflix`
- Finamp: `https://github.com/jmshrv/finamp`

**Outputs**:
- Repository analysis document
- Architecture comparison
- Reusable component list
- Pattern recommendations
- Hybrid architecture proposal

**Related Skills**:
- `skills/xtream-stalker-api.md` - IPTV API integration
- `skills/package-presets.md` - Streaming preset
- `templates/streaming-app.template` - Full project scaffold

---

## Skill Registry

| Skill | File | Trigger |
|-------|------|---------|
| Create Widget | `skills/create-widget.md` | create widget, new widget |
| Create Model | `skills/create-model.md` | create model, data class |
| Create Provider | `skills/create-provider.md` | create provider, state management |
| Create Repository | `skills/create-repository.md` | create repository, data layer |
| Create Test | `skills/create-test.md` | create test file |
| Analyze & Fix | `skills/analyze-fix.md` | analyze, fix lint, fix issues |
| Prisma Query | `skills/prisma-query.md` | prisma query, database query |
| Prisma Schema | `skills/prisma-schema.md` | prisma schema, define table |
| Playwright Test | `skills/playwright-test.md` | playwright test, e2e script |
| Gitignore | `skills/gitignore.md` | gitignore, ignore files, add package |
| Create Page | `skills/create-page.md` | create page, new page, new screen |
| Create Use Case | `skills/create-usecase.md` | create usecase, domain usecase |
| Create API Endpoint | `skills/create-api-endpoint.md` | create endpoint, api route, backend route |
| Create Migration | `skills/create-migration.md` | prisma migration, database migration |
| Add Package | `skills/add-package.md` | add package, install package, add dependency |
| Create BLoC | `skills/create-bloc.md` | create bloc, new bloc, create cubit |
| Create Service | `skills/create-service.md` | create service, new service |
| Localization | `skills/localization.md` | localization, i18n, translations, multi-language |
| Create Extension | `skills/create-extension.md` | create extension, dart extension |
| Environment Setup | `skills/env-setup.md` | env setup, environment variables, build flavors |
| API Documentation | `skills/api-documentation.md` | document api, api docs, endpoint docs |
| Create Feature | `skills/create-feature.md` | create feature, new feature, scaffold feature |
| Create DTO | `skills/create-dto.md` | create dto, data transfer object, api model |
| Create Middleware | `skills/create-middleware.md` | create middleware, backend middleware |
| Create Hook | `skills/create-hook.md` | create hook, custom hook, flutter hook |
| Create Validator | `skills/create-validator.md` | create validator, form validation, input validation |
| Generate Mocks | `skills/generate-mocks.md` | generate mocks, create mocks, test mocks |
| Versioning | `skills/versioning.md` | version bump, release, changelog, semver |
| Input Security | `skills/input-security.md` | input security, sanitize, xss, ssrf, injection, secure input |
| Project Maintenance | `skills/project-maintenance.md` | maintain project, update registry, sync files, project config |
| Package Presets | `skills/package-presets.md` | package presets, dependencies, minimal, standard, enterprise |
| Xtream/Stalker API | `skills/xtream-stalker-api.md` | xtream code, stalker portal, iptv, live tv, streaming api, m3u, epg |
| Streaming Advanced | `skills/streaming-advanced.md` | watch history, resume playback, downloads, parental controls, epg ui, tv navigation, firestick |

---

## Templates

Code templates for rapid scaffolding. Located in `templates/`.

| Template | File | Use Case |
|----------|------|----------|
| Feature Module | `templates/feature.dart.template` | Complete clean architecture feature |
| BLoC | `templates/bloc.dart.template` | State management with events/states |
| Repository | `templates/repository.dart.template` | Data layer with data sources |
| Project Structure | `templates/project-structure.template` | Directory layouts for all project patterns |
| Pubspec | `templates/pubspec.yaml.template` | Configurable pubspec with package presets |
| Analysis Options | `templates/analysis_options.yaml.template` | Strict linting configuration |
| Auth Feature | `templates/auth-feature.template` | Complete authentication scaffold |
| Streaming App | `templates/streaming-app.template` | Netflix/Jellyfin streaming app with IPTV |
| Page | `templates/page.dart.template` | Full page with BLoC integration |
| Widget | `templates/widget.dart.template` | Stateless/Stateful/Consumer variants |
| Test | `templates/test.dart.template` | Unit/BLoC/Widget/Golden tests |
| Archon CLAUDE.md | `templates/archon-claude.md.template` | CLAUDE.md for Archon MCP task management |

### Template Usage

Templates use placeholder syntax that should be replaced:
- `{{FEATURE_NAME}}` → SCREAMING_CASE
- `{{FeatureName}}` → PascalCase
- `{{feature_name}}` → snake_case
- `{{featureName}}` → camelCase

**Auto-invoke**: When creating new features, BLoCs, or pages, offer to use the appropriate template.

---

## Auto-Update Rules

### Gitignore Maintenance

**Auto-update `.gitignore` when:**
- New package is added to `pubspec.yaml`
- New tooling is introduced (Firebase, Docker, Fastlane)
- New platform target is added
- Secrets or credentials are mentioned
- Database files are created

**Trigger the `skills/gitignore.md` skill automatically for these events.**

### Dependency Maintenance

**Proactively offer dependency updates when:**
- User mentions "maintenance" or "keeping up to date"
- Starting a new development session after long break
- Before major releases or deployments
- Security vulnerabilities are mentioned
- User asks about package versions

**Trigger the `agents/dependency-update.md` agent for these events.**

**Auto-check workflow:**
1. Run `flutter pub outdated` to assess state
2. Categorize updates (patch/minor/major)
3. Highlight security-critical updates
4. Propose update plan with breaking change analysis
5. Execute updates with testing after user approval

### Context Maintenance

**Auto-update `context.md` when:**
- Architecture decisions are made
- New conventions are established
- Session work is completed
- Key files are created/moved
- External services are added

**Before starting work**, check `context.md` for:
- Project conventions
- Architecture decisions
- Known issues
- Previous session notes

### Environment Awareness

**All agents MUST understand environment differences:**

| Environment | Purpose | Behavior |
|-------------|---------|----------|
| Development | Local coding | Full logging, mock data available, relaxed security |
| Staging | Testing/QA | Production-like, but with test data |
| Production | Live users | Minimal logging, strict security, real data |

**Database considerations by environment:**
- **Development**: Can reset, use seeds, run any migration
- **Staging**: Test migrations here first, use anonymized data
- **Production**: Careful migrations, backup first, no resets

**When writing code, consider:**
1. Use `AppConfig.isDevelopment` checks for debug features
2. Never hardcode environment-specific values
3. Log levels should respect environment
4. API URLs must come from environment config
5. Feature flags may differ by environment

**When documenting:**
- Specify which environment(s) endpoints/features apply to
- Note environment-specific behaviors
- Document database differences

---

## Usage Instructions

### For Claude

1. **On each user request**, scan for trigger keywords
2. **Load the matching agent file** from `.claude/agents/`
3. **Follow the agent's instructions** to complete the task
4. **For multi-step tasks**, use Planning agent first
5. **Chain agents** when workflows require multiple steps

### Example Flows

**User**: "Plan a user authentication feature"
```
→ Detect: "plan" + "feature"
→ Load: agents/planning.md
→ Execute planning workflow
→ Output: Task breakdown, risks, milestones
```

**User**: "Review this code for security issues"
```
→ Detect: "review" + "security"
→ Load: agents/code-review.md + agents/security-audit.md
→ Execute combined review
→ Output: Issues found, recommendations
```

**User**: "Create a new user profile widget"
```
→ Detect: "create" + "widget"
→ Load: skills/create-widget.md
→ Execute widget creation
→ Output: Widget code following patterns
```

**User**: "Set up CI/CD for this project"
```
→ Detect: "CI/CD"
→ Load: agents/automation.md + agents/github-workflow.md
→ Execute automation setup
→ Output: GitHub Actions workflows, scripts
```

---

## Enhanced Matching Rules

### Fuzzy Keyword Matching

Handle common typos and variations:

| Typed | Matches |
|-------|---------|
| "riverpod", "river pod" | State Management |
| "crashalytics", "crashlytics" | Monitoring |
| "localize", "localisation" | Internationalization |
| "deploy", "deployment" | Deployment |
| "postgres", "postgresql" | Database Design, Dev Environment |

### Context-Aware Triggers

**Based on current file type:**
- `.dart` in `lib/` → Code-related agents (Refactor, Code Review)
- `.dart` in `test/` → Testing agents (Test Writer, Testing Strategy)
- `pubspec.yaml` → Dependency Update, Add Package skill
- `.github/workflows/` → Automation, GitHub Workflow
- `docker-compose.yml` → Dev Environment, Deployment

**Based on directory:**
- Empty directory → Project Setup
- `lib/features/*/` → Architecture patterns apply
- `backend/` → API Design, Middleware, Database
- `ios/` or `android/` → Mobile agent

### Agent Chaining Rules

**Auto-chain when:**
- Security-sensitive code detected → Add Security Audit
- New API endpoint created → Add Test Writer
- Database schema changed → Add Migration agent
- Performance-critical code → Add Performance agent

### Conflict Resolution

When multiple agents match equally:
1. Check `context.md` for project preferences
2. Ask user to clarify intent
3. Default to more specific agent over general

---

## Cross-Cutting Concerns

### All Agents Must Follow

**Error Handling Standards:**
```dart
// Use Either type for operations that can fail
Future<Either<Failure, T>> operation();

// Catch specific exceptions, not generic
try {
  // ...
} on NetworkException catch (e) {
  // Handle network errors
} on ValidationException catch (e) {
  // Handle validation errors
}
```

**Logging Standards:**
```dart
// Use structured logging
LoggerService.info('User signed in', data: {'userId': user.id});

// Log at appropriate levels
LoggerService.debug('...');  // Development only
LoggerService.info('...');   // Normal operations
LoggerService.warning('...'); // Potential issues
LoggerService.error('...');  // Errors
```

**Naming Conventions:**
- Classes: `PascalCase`
- Files: `snake_case.dart`
- Variables/functions: `camelCase`
- Constants: `camelCase` (not SCREAMING_CASE)
- Private: `_prefixWithUnderscore`

**Code Organization:**
- One class per file (with exceptions for small related classes)
- Group imports: dart, package, relative
- Keep files under 300 lines when possible

### Documentation Standards

Every public API should have:
- Brief description
- Parameter documentation
- Return value documentation
- Example usage (for complex APIs)

```dart
/// Authenticates a user with email and password.
///
/// Returns [Right] with [User] on success, [Left] with [Failure] on error.
///
/// Example:
/// ```dart
/// final result = await signIn('user@example.com', 'password');
/// result.fold(
///   (failure) => print('Error: ${failure.message}'),
///   (user) => print('Welcome, ${user.name}'),
/// );
/// ```
Future<Either<Failure, User>> signIn(String email, String password);
```

---

## Code Quality Rules

**All agents MUST follow the rules in `rules/code-quality.md`:**

1. **No Backward Compatibility Code** - Never write legacy/compat hacks
2. **No Dead Code** - Remove unreachable code
3. **No Unresolved TODOs** - Implement or remove
4. **No Commented-Out Code** - Delete, use git for history
5. **No Deprecated API Usage** - Use current APIs only
6. **No Magic Numbers** - Use named constants
7. **No Hardcoded Strings** - Use l10n/constants for UI
8. **Production Code Only** - No debug artifacts

**Enforcement**: Run Agent Testing verification before any commit.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Total Agents | 35 |
| Total Skills | 33 |
| Templates | 12 |
| Commands | 7 |
| Hooks | 10 |
| Multi-Agent Workflows | 25 |
| Auto-Update Rules | 4 |
| Code Quality Rules | 8 |

---

## Directory Structure

```
.claude/
├── registry.md              # This file - agent/skill index
├── context.md               # Project context and session notes
├── QUICKSTART.md            # 5-minute getting started guide
├── settings.json            # Auto-context and hook configuration
├── agents/                  # Agent definitions (35 agents)
│   ├── orchestration.md     # How agents work together
│   ├── project-setup.md
│   ├── repo-import.md
│   ├── repo-analyzer.md     # Analyze external repos (Jellyflix, Jellyfin)
│   ├── platform-installer.md
│   ├── learning-system.md
│   ├── agent-testing.md
│   └── ... (28 more)
├── skills/                  # Skill definitions (33 skills)
│   ├── create-feature.md
│   ├── create-widget.md
│   ├── versioning.md
│   ├── input-security.md
│   ├── project-maintenance.md
│   ├── package-presets.md
│   ├── xtream-stalker-api.md # IPTV streaming API integration
│   ├── streaming-advanced.md # Watch history, downloads, parental controls, TV nav
│   └── ... (25 more)
├── docs/                    # Reference documentation (3 docs)
│   ├── effective-dart.md    # Dart style guide
│   ├── flutter-patterns.md  # Flutter best practices
│   └── packages.md          # Recommended packages
├── commands/                # Slash commands (7 commands)
│   ├── project-new.md       # /project-new
│   ├── project-deploy.md    # /project-deploy
│   ├── project-test.md      # /project-test
│   ├── project-review.md    # /project-review
│   ├── project-fix-issue.md # /project-fix-issue
│   ├── project-release.md   # /project-release
│   └── project-validate.md  # /project-validate
├── templates/               # Code templates (12 templates)
│   ├── feature.dart.template
│   ├── bloc.dart.template
│   ├── repository.dart.template
│   ├── page.dart.template
│   ├── widget.dart.template
│   ├── test.dart.template
│   ├── project-structure.template
│   ├── pubspec.yaml.template
│   ├── analysis_options.yaml.template
│   ├── auth-feature.template
│   ├── streaming-app.template # Netflix/Jellyfin IPTV streaming app
│   └── archon-claude.md.template # CLAUDE.md for Archon MCP projects
├── hooks/                   # Enforcement hooks (10 hooks)
│   ├── block-secrets.py     # Block editing secret files
│   ├── block-dangerous.py   # Block dangerous commands
│   ├── format-dart.py       # Auto-format Dart files
│   ├── session-end.py       # Record session learnings
│   ├── quality-check.py     # Check code quality rules
│   ├── validate-project.py  # Validate project configuration
│   ├── security-scan.py     # Scan for security vulnerabilities
│   ├── pubspec-check.py     # Validate pubspec.yaml changes
│   ├── auto-gitignore.py    # Auto-update .gitignore
│   └── registry-sync.py     # Remind to update registry
├── rules/                   # Mandatory rules
│   └── code-quality.md
├── memory/                  # Persistent learnings
│   ├── global.md
│   ├── errors/
│   ├── decisions/
│   ├── patterns/
│   └── sessions/
└── learnings/               # Knowledge base
    ├── repos/               # External repo analysis
    └── project/             # Project-specific learnings
```
