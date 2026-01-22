# Fix GitHub Issue

Analyze and fix a GitHub issue.

## Usage
```
/project-fix-issue [issue-number]
```

## Arguments

- `$ARGUMENTS` - GitHub issue number (e.g., `123` or `#123`)

## Workflow

1. **Fetch Issue Details**
   ```bash
   gh issue view $ARGUMENTS
   ```

2. **Analyze Issue**
   - Read issue description
   - Check labels and priority
   - Identify related code
   - Look for reproduction steps

3. **Investigate**
   - Search codebase for related files
   - Understand the current behavior
   - Identify root cause

4. **Plan Fix**
   - Determine scope of changes
   - Identify files to modify
   - Consider test requirements

5. **Implement Fix**
   - Make necessary code changes
   - Add or update tests
   - Verify fix works

6. **Verify**
   - Run tests
   - Run analyzer
   - Manual verification if possible

7. **Create PR**
   - Commit changes with reference to issue
   - Create pull request
   - Link to issue

## Example

```
# Fix issue #42
/project-fix-issue 42

# With full URL
/project-fix-issue https://github.com/owner/repo/issues/42
```

## Commit Message Format

```
fix(scope): brief description

Fixes #42

- Detailed change 1
- Detailed change 2
```

## Related Agents

- Debugging Agent
- Test Writer Agent
- Code Review Agent
- GitHub Workflow Agent
