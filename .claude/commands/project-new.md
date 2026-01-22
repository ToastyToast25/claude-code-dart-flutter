---
name: project-new
description: Start a new Dart/Flutter project with guided setup workflow
argument-hint: "[project-name]"
---

# Start New Project

Initialize a new Dart/Flutter project with the full agent workflow.

## Usage
```
/project-new [project-name]
```

## Arguments

- `$ARGUMENTS` - Optional project name (lowercase, underscores allowed)

## Workflow

Execute the following steps using the **Project Setup Agent** (`agents/project-setup.md`):

### Phase 1: Gather Information

1. **Q1: Project Name** (skip if `$ARGUMENTS` provided)
   - Validate: lowercase, underscores, no reserved words

2. **Q2: Reference Repository**
   - Ask if building upon existing GitHub repo
   - If yes → Hand off to Repository Import Agent first

3. **Q3: Target Platforms** (multi-select)
   - Android, iOS, Web, Desktop, Backend-only
   - Derives: `hasMobile`, `hasWeb`, `hasDesktop`, `isBackendOnly`

4. **Q4: Subdomain Architecture** (skip if no web)
   - Independent servers vs shared deployment vs none

5. **Q5: Which Subdomains** (skip if Q4 = no)
   - Admin, Support, Docs, Blog, Developer Portal

6. **Q6: Backend Type**
   - Dart backend, External API, Firebase/Supabase, None

7. **Q7: Database** (skip if no backend AND no mobile)
   - PostgreSQL, SQLite, Firestore, Supabase, None

8. **Q8: State Management** (skip if backend-only)
   - Riverpod, BLoC, Provider

9. **Q9: Authentication**
   - Full auth, Firebase Auth, Custom JWT, None

10. **Q10: Package Preset**
    - Minimal, Standard, Streaming, Enterprise, Custom

11. **Q11: Project Visibility**
    - Private, MIT, Apache 2.0, GPL

### Phase 2: Execute Setup

1. **Select Architecture Pattern**
   - Pattern A: Single App
   - Pattern B: Monorepo Shared
   - Pattern C: Distributed Subdomains
   - Pattern D: Extensible
   - Pattern E: Backend Only

2. **Create Project Structure**
   - Generate folder structure
   - Create configuration files
   - Set up shared packages if needed

3. **Apply Templates**
   - Use appropriate templates from `templates/`
   - Configure based on selected preset

### Phase 3: Verify & Document

1. **Run Verification**
   - Invoke Agent Testing for quality check
   - Ensure code compiles
   - Check for any issues

2. **Document Decisions**
   - Update `.claude/context.md`
   - Record in Learning System

3. **Provide Next Steps**
   - Commands to run
   - What to do next

## Conditional Skip Logic

| Question | Skip When |
|----------|-----------|
| Q1: Project Name | `$ARGUMENTS` provided |
| Q4: Subdomains | `hasWeb` = false |
| Q5: Which Subdomains | Q4 = "No" |
| Q7: Database | No backend AND no mobile |
| Q8: State Management | Backend-only project |

## Examples

```bash
# Start with project name
/project-new my_app

# Start without name (will prompt)
/project-new
```

## Related Agents

- **Repository Import Agent** - Analyze reference repos
- **Architecture Agent** - Detailed structure decisions
- **Database Design Agent** - Schema setup
- **Automation Agent** - CI/CD configuration
- **Platform Installer Agent** - Deployment setup
- **Agent Testing Agent** - Verify generated code
