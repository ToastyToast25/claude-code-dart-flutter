# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial Claude Code agent/skill system
- 34 specialized agents for Dart/Flutter development
- 27 skills with auto-activation
- 6 code templates
- 5 slash commands
- Enforcement hooks for code quality

### Changed
- Nothing yet

### Deprecated
- Nothing yet

### Removed
- Nothing yet

### Fixed
- Nothing yet

### Security
- Nothing yet

---

## [0.1.0] - 2026-01-21

### Added
- Initial release
- Project structure with `.claude/` directory
- Agent system for development workflows
- Skill system for code patterns
- Template system for scaffolding
- Hook system for enforcement
- Memory system for learnings
- Documentation (README, CONTRIBUTING, LICENSE)

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 0.1.0 | 2026-01-21 | Initial release |

---

## Versioning Guidelines

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

### Pre-release Labels
- `alpha`: Early testing, unstable
- `beta`: Feature complete, testing
- `rc`: Release candidate, final testing

Example: `1.0.0-beta.1`, `2.0.0-rc.1`

### When to Bump Versions

| Change Type | Version Bump |
|-------------|--------------|
| Breaking API change | MAJOR |
| New feature | MINOR |
| Bug fix | PATCH |
| Documentation only | PATCH |
| Dependency update (compatible) | PATCH |
| Dependency update (breaking) | MINOR or MAJOR |

---

## Release Checklist

Before releasing a new version:

- [ ] All tests pass (`flutter test`)
- [ ] No analyzer warnings (`flutter analyze`)
- [ ] CHANGELOG.md updated
- [ ] Version bumped in `pubspec.yaml`
- [ ] Version bumped in `lib/core/version.dart` (if applicable)
- [ ] Documentation updated
- [ ] Git tag created (`git tag v1.0.0`)
- [ ] GitHub release created (if applicable)

---

[Unreleased]: https://github.com/username/repo/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/username/repo/releases/tag/v0.1.0
