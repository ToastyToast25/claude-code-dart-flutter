# Agent Orchestration Guide

This document defines how agents work together and hand off to each other.

---

## Agent Dependency Graph

```
                    ┌─────────────────────────┐
                    │    User Request         │
                    └───────────┬─────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│                        ENTRY POINTS                                │
├───────────────────────────────────────────────────────────────────┤
│  Project Setup    Repository Import    Debugging    Deployment    │
└─────────┬─────────────────┬──────────────────┬────────────┬──────┘
          │                 │                  │            │
          ▼                 ▼                  ▼            ▼
┌─────────────────┐ ┌─────────────────┐ ┌───────────┐ ┌────────────┐
│  Architecture   │ │  Learning Sys   │ │ Code Rev  │ │ Platform   │
│  API Design     │ │  (records all)  │ │ Test Wr   │ │ Installer  │
│  Database       │ └────────┬────────┘ └─────┬─────┘ │ Cloudflare │
└────────┬────────┘          │                │       └──────┬─────┘
         │                   │                │              │
         ▼                   ▼                ▼              ▼
┌────────────────────────────────────────────────────────────────────┐
│                       Agent Testing                                 │
│              (verifies all generated code)                         │
└────────────────────────────────────────────────────────────────────┘
```

---

## Hand-Off Protocols

### Protocol 1: New Project

```
User: "new project" / "start project"
         │
         ▼
┌─────────────────────────────────────┐
│ Project Setup Agent                  │
│ Q0: Reference repository?            │
└─────────────┬───────────────────────┘
              │
              ├── Yes ──────────────────────┐
              │                             ▼
              │                   ┌─────────────────────┐
              │                   │ Repository Import   │
              │                   │ - Clone repo        │
              │                   │ - Analyze patterns  │
              │                   │ - Extract learnings │
              │                   └─────────┬───────────┘
              │                             │
              │◄────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Project Setup Agent (continued)      │
│ Q1-Q6: Project requirements          │
│ - Create structure                   │
│ - Configure tooling                  │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Agent Testing                        │
│ - Verify generated code              │
│ - Run quality checks                 │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Learning System                      │
│ - Record decisions                   │
│ - Save patterns used                 │
└─────────────────────────────────────┘
```

### Protocol 2: Deployment

```
User: "deploy" / "set up server"
         │
         ▼
┌─────────────────────────────────────┐
│ Deployment Agent                     │
│ - Determine deployment type          │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Platform Installer Agent             │
│ - Install dependencies               │
│ - Configure services                 │
│ - Set up SSL                         │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Cloudflare Agent                     │
│ - Configure DNS                      │
│ - Set up SSL at edge                 │
│ - Create tunnels if needed           │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Security Audit Agent                 │
│ - Verify secure configuration        │
│ - Check for vulnerabilities          │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Monitoring Agent                     │
│ - Set up logging                     │
│ - Configure alerts                   │
└─────────────────────────────────────┘
```

### Protocol 3: Bug Fix

```
User: "fix bug" / "error: ..."
         │
         ▼
┌─────────────────────────────────────┐
│ Debugging Agent                      │
│ - Reproduce error                    │
│ - Identify root cause                │
│ - Apply fix                          │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Test Writer Agent                    │
│ - Write regression test              │
│ - Verify fix doesn't break others    │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Code Review Agent                    │
│ - Review the fix                     │
│ - Check for side effects             │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Learning System Agent                │
│ - Record error pattern               │
│ - Document fix for future            │
└─────────────────────────────────────┘
```

### Protocol 4: New Feature

```
User: "add feature X"
         │
         ▼
┌─────────────────────────────────────┐
│ Planning Agent                       │
│ - Break down requirements            │
│ - Identify affected areas            │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Architecture Agent                   │
│ - Design component structure         │
│ - Define interfaces                  │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ [Implementation]                     │
│ Skills: create-feature, create-bloc, │
│         create-service, etc.         │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Test Writer Agent                    │
│ - Write unit tests                   │
│ - Write widget tests                 │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Code Review Agent                    │
│ - Review implementation              │
│ - Check quality                      │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Agent Testing                        │
│ - Full verification pipeline         │
└─────────────────────────────────────┘
```

---

## Agent Categories

### Entry Agents
These agents are typically the first to be invoked:

| Agent | Triggers |
|-------|----------|
| Project Setup | New projects, empty directories |
| Repository Import | "based on", "similar to", existing repo |
| Debugging | Errors, bugs, crashes |
| Deployment | Deploy, server setup |
| Planning | Plan, design, architect |

### Core Agents
These handle primary implementation work:

| Agent | Purpose |
|-------|---------|
| Architecture | Structure and design |
| API Design | Backend endpoints |
| Database Design | Schema and migrations |
| State Management | State architecture |
| Mobile | Platform-specific features |

### Quality Agents
These ensure code quality:

| Agent | Purpose |
|-------|---------|
| Code Review | Review code changes |
| Test Writer | Write tests |
| Security Audit | Security checks |
| Agent Testing | Verify generated code |

### Infrastructure Agents
These handle deployment and operations:

| Agent | Purpose |
|-------|---------|
| Platform Installer | Install and configure |
| Cloudflare | DNS and CDN |
| Deployment | Server deployment |
| Monitoring | Logging and alerts |

### Support Agents
These provide auxiliary functions:

| Agent | Purpose |
|-------|---------|
| Learning System | Record learnings |
| Documentation | Create docs |
| Dependency Update | Update packages |
| Migration | Handle upgrades |

---

## Mandatory Hand-Offs

Certain actions MUST trigger specific agents:

| After This | MUST Trigger |
|------------|--------------|
| Code generation | Agent Testing |
| Error fixed | Learning System |
| Architecture decision | Learning System |
| Deployment | Security Audit |
| New API endpoint | Test Writer |
| Database change | Migration Agent |

---

## Cross-Agent Communication

### Shared Context
All agents share access to:
- `.claude/context.md` - Project context
- `.claude/memory/` - Persistent learnings
- `.claude/learnings/` - Repo and project knowledge
- `.claude/rules/` - Code quality rules

### Data Passing
Agents pass data via:
1. Context files (persistent)
2. Session notes (temporary)
3. Direct output (immediate)

### Learning Integration
After completing work, agents should:
1. Check if error was encountered → Record in memory/errors/
2. Check if decision was made → Record in memory/decisions/
3. Check if pattern emerged → Record in memory/patterns/

---

## Conflict Resolution

When multiple agents could apply:

1. **Check context.md** for explicit preferences
2. **Security always wins** - If security-related, Security Audit takes priority
3. **More specific wins** - API Design over Architecture for endpoint work
4. **Ask user** - When genuinely ambiguous

---

## Anti-Patterns

**DON'T:**
- Skip Agent Testing after generating code
- Skip Learning System after fixing bugs
- Deploy without Security Audit
- Generate code without reading existing patterns first

**DO:**
- Always verify generated code
- Always record learnings
- Always check quality rules
- Always consider security implications
