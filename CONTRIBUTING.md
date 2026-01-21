# Contributing

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Install dependencies**: `flutter pub get`
4. **Create a branch** for your changes: `git checkout -b feature/your-feature-name`

## Development Setup

### Prerequisites

- Dart SDK 3.0+
- Flutter SDK 3.0+
- Claude Code CLI (optional, for using agents/skills)
- Python 3.8+ (for hooks)

### Running Locally

```bash
# Install dependencies
flutter pub get

# Run code generation (if applicable)
dart run build_runner build --delete-conflicting-outputs

# Run the app
flutter run

# Run tests
flutter test
```

## Code Style

This project follows Dart/Flutter best practices:

- **Formatting**: Run `dart format .` before committing
- **Analysis**: Ensure `flutter analyze` shows no issues
- **Testing**: Add tests for new features

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files | snake_case | `user_repository.dart` |
| Classes | PascalCase | `UserRepository` |
| Variables | camelCase | `userName` |
| Constants | camelCase or SCREAMING_SNAKE | `maxRetries`, `API_URL` |

### File Organization

- One public class per file
- Related private helpers can stay in the same file
- Tests mirror the source file structure

## Pull Request Process

### Before Submitting

1. **Run tests**: `flutter test`
2. **Run analyzer**: `flutter analyze`
3. **Format code**: `dart format .`
4. **Update documentation** if needed

### PR Guidelines

- **Title**: Use conventional commit format
  - `feat: add user authentication`
  - `fix: resolve login crash on iOS`
  - `docs: update README with setup instructions`
  - `refactor: simplify state management`
  - `test: add unit tests for UserRepository`

- **Description**: Include
  - What changes were made
  - Why the changes were needed
  - How to test the changes
  - Screenshots for UI changes

### Review Process

1. Submit your PR
2. Wait for CI checks to pass
3. Address reviewer feedback
4. Once approved, your PR will be merged

## Adding Agents or Skills

If contributing to the Claude Code agent/skill system:

### Adding an Agent

1. Create file in `.claude/agents/your-agent.md`
2. Follow the existing agent format
3. Add entry to `.claude/registry.md`
4. Test the agent workflow

### Adding a Skill

1. Create file in `.claude/skills/your-skill.md`
2. Add YAML frontmatter with:
   ```yaml
   ---
   description: "Brief description"
   globs: ["lib/**/relevant/*.dart"]
   alwaysApply: false
   ---
   ```
3. Add entry to `.claude/registry.md`

## Reporting Issues

### Bug Reports

Include:
- Flutter/Dart version (`flutter doctor`)
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces
- Screenshots if applicable

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative solutions considered

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the [Contributor Covenant](https://www.contributor-covenant.org/)

## Questions?

- Open an issue for questions
- Check existing issues/discussions first
- Be patient - maintainers are volunteers

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
