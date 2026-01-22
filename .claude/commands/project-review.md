# Code Review

Perform a comprehensive code review of changes.

## Usage
```
/project-review [scope]
```

## Arguments

- `$ARGUMENTS` - Optional: `staged`, `branch`, `file path`, or PR number

## Workflow

1. **Identify Changes**
   ```bash
   # Staged changes
   git diff --cached

   # Branch changes
   git diff main...HEAD

   # Specific file
   git diff path/to/file.dart
   ```

2. **Run Automated Checks**
   - `flutter analyze` - Static analysis
   - `dart format --set-exit-if-changed .` - Format check
   - Test execution

3. **Code Review Checklist**
   - [ ] Code compiles without errors
   - [ ] No analyzer warnings
   - [ ] Tests pass
   - [ ] No hardcoded secrets
   - [ ] No TODO/FIXME comments
   - [ ] No dead code
   - [ ] Follows project patterns
   - [ ] Error handling is appropriate
   - [ ] No security vulnerabilities

4. **Security Review**
   - Check for OWASP vulnerabilities
   - Verify input validation
   - Check authentication/authorization

5. **Generate Report**
   - List issues found
   - Categorize by severity
   - Suggest fixes

## Review Levels

| Level | Scope |
|-------|-------|
| Quick | Syntax, formatting, obvious issues |
| Standard | + Logic, patterns, tests |
| Deep | + Security, performance, architecture |

## Examples

```
# Review staged changes
/project-review staged

# Review current branch vs main
/project-review branch

# Review specific file
/project-review lib/features/auth/auth_service.dart

# Review GitHub PR
/project-review #123
```

## Related Agents

- Code Review Agent
- Security Audit Agent
- Agent Testing Agent
