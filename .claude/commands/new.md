# Start New Project

Initialize a new Dart/Flutter project with the full agent workflow.

## Usage
```
/project:new [project-name]
```

## Workflow

Execute the following steps:

1. **Check for Reference Repository**
   - Ask: "Are you building upon or inspired by an existing GitHub repository?"
   - If yes, invoke Repository Import Agent first

2. **Gather Requirements**
   - Project type (mobile/web/full-stack)
   - Target platforms (Android, iOS, Web, Desktop)
   - Subdomain architecture (if web)
   - Backend needs
   - Database choice

3. **Create Project Structure**
   - Based on answers, select architecture pattern
   - Generate folder structure
   - Create configuration files

4. **Verify Setup**
   - Run Agent Testing verification
   - Ensure code compiles
   - Check for any issues

5. **Document Decisions**
   - Update `.claude/context.md`
   - Record in Learning System

## Arguments

- `$ARGUMENTS` - Optional project name

## Example

```
/project:new my-app
```

This will start the interactive project setup workflow.
