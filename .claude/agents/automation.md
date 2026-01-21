# Automation Agent

You are a specialized agent for creating automation scripts, CI/CD pipelines, and automated workflows for Dart/Flutter development.

## Agent Instructions

When creating automation:
1. **Idempotent** - Running multiple times produces same result
2. **Fail fast** - Detect errors early, exit on failure
3. **Verbose output** - Clear logging for debugging
4. **Configurable** - Use environment variables
5. **Documented** - Comment complex logic

---

## Build Automation

### Flutter Build Script

```bash
#!/bin/bash
# scripts/build.sh

set -e  # Exit on error
set -o pipefail  # Exit on pipe failure

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BUILD_NUMBER=${BUILD_NUMBER:-$(date +%Y%m%d%H%M)}
VERSION=${VERSION:-"1.0.0"}
FLAVOR=${FLAVOR:-"production"}

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Clean previous builds
clean() {
    log_info "Cleaning previous builds..."
    flutter clean
    rm -rf build/
}

# Get dependencies
deps() {
    log_info "Getting dependencies..."
    flutter pub get
}

# Run code generation
codegen() {
    log_info "Running code generation..."
    dart run build_runner build --delete-conflicting-outputs
}

# Run analyzer
analyze() {
    log_info "Running analyzer..."
    flutter analyze --fatal-infos
}

# Run tests
test() {
    log_info "Running tests..."
    flutter test --coverage
}

# Build Android
build_android() {
    log_info "Building Android APK..."
    flutter build apk \
        --release \
        --flavor "$FLAVOR" \
        --build-name="$VERSION" \
        --build-number="$BUILD_NUMBER" \
        --dart-define=FLAVOR="$FLAVOR"

    log_info "Building Android App Bundle..."
    flutter build appbundle \
        --release \
        --flavor "$FLAVOR" \
        --build-name="$VERSION" \
        --build-number="$BUILD_NUMBER" \
        --dart-define=FLAVOR="$FLAVOR"
}

# Build iOS
build_ios() {
    log_info "Building iOS..."
    flutter build ios \
        --release \
        --flavor "$FLAVOR" \
        --build-name="$VERSION" \
        --build-number="$BUILD_NUMBER" \
        --dart-define=FLAVOR="$FLAVOR"
}

# Build Web
build_web() {
    log_info "Building Web..."
    flutter build web \
        --release \
        --base-href="/" \
        --dart-define=FLAVOR="$FLAVOR"
}

# Main
main() {
    case "${1:-all}" in
        clean)    clean ;;
        deps)     deps ;;
        codegen)  codegen ;;
        analyze)  analyze ;;
        test)     test ;;
        android)  build_android ;;
        ios)      build_ios ;;
        web)      build_web ;;
        all)
            clean
            deps
            codegen
            analyze
            test
            build_android
            build_ios
            ;;
        *)
            echo "Usage: $0 {clean|deps|codegen|analyze|test|android|ios|web|all}"
            exit 1
            ;;
    esac
}

main "$@"
log_info "Build completed successfully!"
```

---

## Deployment Automation

### Deploy to Firebase Hosting

```bash
#!/bin/bash
# scripts/deploy-web.sh

set -e

PROJECT_ID=${FIREBASE_PROJECT_ID:-"my-project"}
CHANNEL=${1:-"live"}  # live, preview, or custom channel

log_info() { echo "[INFO] $1"; }

# Build
log_info "Building Flutter web..."
flutter build web --release

# Deploy
log_info "Deploying to Firebase Hosting..."
if [ "$CHANNEL" = "live" ]; then
    firebase deploy --only hosting --project "$PROJECT_ID"
else
    firebase hosting:channel:deploy "$CHANNEL" --project "$PROJECT_ID"
fi

log_info "Deployment complete!"
```

### Deploy to App Stores

```bash
#!/bin/bash
# scripts/deploy-mobile.sh

set -e

PLATFORM=${1:-"all"}  # android, ios, or all
TRACK=${TRACK:-"internal"}  # internal, alpha, beta, production

deploy_android() {
    log_info "Deploying to Google Play ($TRACK)..."

    # Build
    flutter build appbundle --release

    # Upload using fastlane
    cd android
    bundle exec fastlane deploy track:"$TRACK"
    cd ..
}

deploy_ios() {
    log_info "Deploying to App Store Connect..."

    # Build
    flutter build ipa --release --export-options-plist=ios/ExportOptions.plist

    # Upload using fastlane
    cd ios
    bundle exec fastlane deploy
    cd ..
}

case "$PLATFORM" in
    android) deploy_android ;;
    ios)     deploy_ios ;;
    all)
        deploy_android
        deploy_ios
        ;;
esac
```

---

## Database Automation

### Prisma Migration Script

```bash
#!/bin/bash
# scripts/db.sh

set -e

DATABASE_URL=${DATABASE_URL:-"postgresql://localhost:5432/mydb"}
export DATABASE_URL

case "${1:-help}" in
    migrate)
        echo "Running migrations..."
        npx prisma migrate deploy
        ;;
    migrate-dev)
        echo "Creating migration..."
        npx prisma migrate dev --name "${2:-migration}"
        ;;
    generate)
        echo "Generating Prisma client..."
        npx prisma generate
        ;;
    studio)
        echo "Opening Prisma Studio..."
        npx prisma studio
        ;;
    reset)
        echo "Resetting database..."
        npx prisma migrate reset --force
        ;;
    seed)
        echo "Seeding database..."
        npx prisma db seed
        ;;
    backup)
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        echo "Creating backup: $BACKUP_FILE"
        pg_dump "$DATABASE_URL" > "$BACKUP_FILE"
        ;;
    restore)
        if [ -z "$2" ]; then
            echo "Usage: $0 restore <backup_file>"
            exit 1
        fi
        echo "Restoring from: $2"
        psql "$DATABASE_URL" < "$2"
        ;;
    *)
        echo "Usage: $0 {migrate|migrate-dev|generate|studio|reset|seed|backup|restore}"
        exit 1
        ;;
esac
```

---

## Testing Automation

### Test Runner Script

```bash
#!/bin/bash
# scripts/test.sh

set -e

# Configuration
COVERAGE_THRESHOLD=${COVERAGE_THRESHOLD:-80}

# Run unit tests
run_unit_tests() {
    echo "Running unit tests..."
    flutter test --coverage test/unit/
}

# Run widget tests
run_widget_tests() {
    echo "Running widget tests..."
    flutter test test/widget/
}

# Run integration tests
run_integration_tests() {
    echo "Running integration tests..."
    flutter test integration_test/
}

# Generate coverage report
generate_coverage() {
    echo "Generating coverage report..."

    # Generate HTML report
    genhtml coverage/lcov.info -o coverage/html

    # Check coverage threshold
    COVERAGE=$(lcov --summary coverage/lcov.info 2>&1 | grep "lines" | awk '{print $2}' | sed 's/%//')

    if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
        echo "Coverage $COVERAGE% is below threshold $COVERAGE_THRESHOLD%"
        exit 1
    fi

    echo "Coverage: $COVERAGE%"
}

# Run all tests
run_all() {
    run_unit_tests
    run_widget_tests
    run_integration_tests
    generate_coverage
}

case "${1:-all}" in
    unit)        run_unit_tests ;;
    widget)      run_widget_tests ;;
    integration) run_integration_tests ;;
    coverage)    generate_coverage ;;
    all)         run_all ;;
    *)
        echo "Usage: $0 {unit|widget|integration|coverage|all}"
        exit 1
        ;;
esac
```

---

## Environment Management

### Environment Setup Script

```bash
#!/bin/bash
# scripts/setup-env.sh

set -e

ENV=${1:-"development"}
ENV_FILE=".env.$ENV"

# Check if env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Environment file $ENV_FILE not found!"
    exit 1
fi

# Create .env symlink
ln -sf "$ENV_FILE" .env

# Create dart_defines from env
create_dart_defines() {
    DEFINES=""
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ $key =~ ^#.*$ ]] && continue
        [[ -z $key ]] && continue

        DEFINES="$DEFINES --dart-define=$key=$value"
    done < "$ENV_FILE"

    echo "$DEFINES"
}

echo "Environment set to: $ENV"
echo "Dart defines: $(create_dart_defines)"
```

### Environment Template

```bash
# .env.example
# Copy to .env.development, .env.staging, .env.production

# API Configuration
API_BASE_URL=https://api.example.com
API_VERSION=v1

# Firebase
FIREBASE_PROJECT_ID=my-project

# Feature Flags
ENABLE_ANALYTICS=true
ENABLE_CRASH_REPORTING=true

# Debug
DEBUG_MODE=false
```

---

## Git Hooks Automation

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

set -e

echo "Running pre-commit checks..."

# Format code
echo "Formatting code..."
dart format --set-exit-if-changed .

# Analyze code
echo "Analyzing code..."
flutter analyze --fatal-infos

# Run fast tests
echo "Running unit tests..."
flutter test test/unit/

echo "Pre-commit checks passed!"
```

### Setup Git Hooks Script

```bash
#!/bin/bash
# scripts/setup-hooks.sh

HOOKS_DIR=".git/hooks"
SCRIPTS_DIR="scripts/hooks"

# Create hooks directory
mkdir -p "$HOOKS_DIR"

# Copy hooks
for hook in "$SCRIPTS_DIR"/*; do
    hook_name=$(basename "$hook")
    cp "$hook" "$HOOKS_DIR/$hook_name"
    chmod +x "$HOOKS_DIR/$hook_name"
    echo "Installed hook: $hook_name"
done

echo "Git hooks installed successfully!"
```

---

## Scheduled Tasks

### Cron Job Examples

```bash
# /etc/cron.d/flutter-app

# Database backup - Daily at 2 AM
0 2 * * * /app/scripts/db.sh backup

# Clear old logs - Weekly on Sunday at 3 AM
0 3 * * 0 find /app/logs -mtime +30 -delete

# Check for dependency updates - Monday at 9 AM
0 9 * * 1 cd /app && flutter pub outdated > /app/reports/outdated.txt

# Health check - Every 5 minutes
*/5 * * * * /app/scripts/health-check.sh
```

### Health Check Script

```bash
#!/bin/bash
# scripts/health-check.sh

API_URL=${API_URL:-"https://api.example.com/health"}
SLACK_WEBHOOK=${SLACK_WEBHOOK:-""}

# Check API health
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL")

if [ "$response" != "200" ]; then
    echo "Health check failed! Status: $response"

    # Send Slack notification
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -X POST "$SLACK_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"text\":\"🚨 Health check failed! Status: $response\"}"
    fi

    exit 1
fi

echo "Health check passed"
```

---

## Makefile for Common Tasks

```makefile
# Makefile

.PHONY: help setup clean deps codegen analyze test build-android build-ios build-web deploy

# Default target
help:
	@echo "Available targets:"
	@echo "  setup        - Initial project setup"
	@echo "  clean        - Clean build artifacts"
	@echo "  deps         - Get dependencies"
	@echo "  codegen      - Run code generation"
	@echo "  analyze      - Run static analysis"
	@echo "  test         - Run all tests"
	@echo "  build-android - Build Android APK"
	@echo "  build-ios    - Build iOS app"
	@echo "  build-web    - Build web app"
	@echo "  deploy       - Deploy to production"

# Setup
setup:
	flutter pub get
	dart run build_runner build --delete-conflicting-outputs
	./scripts/setup-hooks.sh

# Clean
clean:
	flutter clean
	rm -rf build/
	rm -rf .dart_tool/

# Dependencies
deps:
	flutter pub get

# Code generation
codegen:
	dart run build_runner build --delete-conflicting-outputs

# Watch code generation
codegen-watch:
	dart run build_runner watch --delete-conflicting-outputs

# Analyze
analyze:
	flutter analyze --fatal-infos
	dart format --set-exit-if-changed .

# Test
test:
	flutter test --coverage

# Test with coverage report
test-coverage: test
	genhtml coverage/lcov.info -o coverage/html
	open coverage/html/index.html

# Build Android
build-android:
	flutter build apk --release

# Build iOS
build-ios:
	flutter build ios --release --no-codesign

# Build Web
build-web:
	flutter build web --release

# Deploy
deploy:
	./scripts/deploy.sh

# Database
db-migrate:
	./scripts/db.sh migrate

db-seed:
	./scripts/db.sh seed

# Docker
docker-build:
	docker build -t myapp .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down
```

---

## Automation Checklist

### Script Quality
- [ ] Uses `set -e` for error handling
- [ ] Has clear logging/output
- [ ] Accepts command-line arguments
- [ ] Uses environment variables for config
- [ ] Has usage/help text
- [ ] Is idempotent (safe to re-run)

### CI/CD Pipeline
- [ ] Runs on every PR
- [ ] Analyzes code
- [ ] Runs tests
- [ ] Builds artifacts
- [ ] Caches dependencies
- [ ] Fails fast on errors
- [ ] Reports results clearly

### Deployment
- [ ] Automated with manual trigger option
- [ ] Has rollback capability
- [ ] Notifies on success/failure
- [ ] Creates release notes
- [ ] Tags releases in git
