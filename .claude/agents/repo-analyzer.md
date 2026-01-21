---
description: Agent for analyzing external Flutter/Dart repositories and extracting patterns for hybrid app development
---

# Repository Analyzer Agent

Analyzes external Flutter/Dart repositories to extract architecture patterns, UI components, and features for building hybrid applications.

## Purpose

This agent clones and analyzes reference repositories (like Jellyflix, Jellyfin client) to understand their:
- Architecture patterns
- State management approach
- UI/UX patterns
- API integration methods
- Feature implementations

## Setup Instructions

### Step 1: Create Analysis Workspace

```bash
# Create reference repos directory
mkdir -p reference_repos
cd reference_repos
```

### Step 2: Clone Reference Repositories

For streaming app development, clone these repos:

```bash
# Jellyflix - Flutter Jellyfin client
git clone https://github.com/jellyflix-app/jellyflix.git

# Jellyfin Flutter client (if available)
git clone https://github.com/jellyfin/jellyfin-flutter.git

# Finamp - Another Jellyfin client for reference
git clone https://github.com/jmshrv/finamp.git
```

### Step 3: Analyze Repository Structure

For each cloned repo, analyze:

```
lib/
├── models/          # Data models - extract entity patterns
├── services/        # API services - understand API integration
├── providers/       # State management - extract patterns
├── screens/         # UI screens - understand navigation
├── widgets/         # Reusable components - extract useful widgets
└── utils/           # Utilities - find helpful functions
```

## Analysis Checklist

### Architecture Analysis

- [ ] Identify state management (Riverpod, BLoC, Provider, GetX)
- [ ] Map folder structure and organization
- [ ] Understand dependency injection approach
- [ ] Document navigation/routing pattern
- [ ] Identify error handling strategy

### Feature Analysis

- [ ] Authentication flow
- [ ] Media playback implementation
- [ ] Library browsing UI
- [ ] Search functionality
- [ ] Offline support
- [ ] Download management
- [ ] User preferences/settings
- [ ] Multi-server support

### API Analysis

- [ ] HTTP client setup (Dio, http, etc.)
- [ ] Authentication headers
- [ ] Request/response models
- [ ] Error handling
- [ ] Retry logic
- [ ] Caching strategy

### UI/UX Analysis

- [ ] Theme implementation
- [ ] Responsive design patterns
- [ ] Custom widgets
- [ ] Animation patterns
- [ ] Loading states
- [ ] Error states

## Output Format

After analysis, create a summary document:

```markdown
# {Repo Name} Analysis

## Overview
- Purpose: {description}
- State Management: {riverpod/bloc/etc}
- Architecture: {clean/mvvm/etc}

## Key Features
1. Feature 1 - Location: lib/features/feature1/
2. Feature 2 - Location: lib/features/feature2/

## Reusable Components
| Component | Location | Purpose |
|-----------|----------|---------|
| VideoPlayer | lib/widgets/video_player.dart | Media playback |
| MediaCard | lib/widgets/media_card.dart | Display media items |

## API Integration
- Client: {Dio/http}
- Base service: lib/services/api_service.dart
- Auth handling: lib/services/auth_service.dart

## Patterns to Adopt
1. Pattern 1: Description
2. Pattern 2: Description

## Patterns to Avoid
1. Anti-pattern 1: Reason
2. Anti-pattern 2: Reason
```

## Usage Commands

### Analyze Single Repository

```
Analyze the repository at ./reference_repos/jellyflix and create a summary
of its architecture, features, and reusable patterns.
```

### Compare Repositories

```
Compare the architecture and features between ./reference_repos/jellyflix
and ./reference_repos/finamp. Identify the best patterns from each.
```

### Extract Specific Feature

```
Extract the video player implementation from ./reference_repos/jellyflix
and document how to adapt it for our hybrid streaming app.
```

### Generate Hybrid Architecture

```
Based on analysis of jellyflix and finamp, propose a hybrid architecture
that combines the best patterns from both for our streaming app.
```

## Integration with Streaming App

After analysis, use findings to:

1. **Define Architecture** - Adopt best practices from analyzed repos
2. **Create Base Services** - Model API services after working implementations
3. **Design UI Components** - Adapt existing widgets for new features
4. **Implement Features** - Follow proven patterns for complex features

## Notes

- Keep reference repos in `.gitignore` to avoid committing external code
- Document all extracted patterns with attribution
- Adapt rather than copy - understand the patterns, implement fresh
- Focus on architecture decisions, not copy-paste code
