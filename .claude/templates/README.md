# Code Templates

Boilerplate templates for common Dart/Flutter patterns.

## Available Templates

| Template | Description | Use Case |
|----------|-------------|----------|
| `feature.dart.template` | Complete feature module | New feature with clean architecture |
| `bloc.dart.template` | BLoC pattern with events/states | State management |
| `repository.dart.template` | Repository + data sources | Data access layer |
| `page.dart.template` | Full page with BLoC integration | Screen/route with state |
| `widget.dart.template` | Stateless/Stateful/Consumer | Reusable UI component |
| `test.dart.template` | Unit/BLoC/Widget/Golden tests | Testing patterns |

## Usage

Templates use placeholder syntax:

- `{{FEATURE_NAME}}` - SCREAMING_CASE name
- `{{FeatureName}}` - PascalCase name
- `{{feature_name}}` - snake_case name
- `{{featureName}}` - camelCase name

### Example

To create a "User Profile" feature:

1. Copy `feature.dart.template`
2. Replace placeholders:
   - `{{FEATURE_NAME}}` → `USER_PROFILE`
   - `{{FeatureName}}` → `UserProfile`
   - `{{feature_name}}` → `user_profile`
3. Split into separate files

Or ask Claude: "Create a user profile feature using the template"

## Template Variables

When asking Claude to use a template, provide:

```
Create a [feature_name] feature with:
- Entity fields: id, name, email, createdAt
- API endpoint: /api/v1/users
- State management: BLoC
```

Claude will use the appropriate template and customize it for your needs.
