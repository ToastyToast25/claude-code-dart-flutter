# /project:validate - Validate Project Configuration

Validate that all Claude Code configuration files are consistent and up to date.

## Usage

```
/project:validate
```

## What This Command Does

1. **Count Verification** - Ensures registry.md counts match actual files
2. **Cross-Reference Check** - Verifies all referenced files exist
3. **Settings Validation** - Confirms hooks and patterns are properly configured
4. **Skill Integrity** - Validates skill frontmatter and required sections

## Execution Steps

### Step 1: Count All Configuration Files

```bash
# Count agents
find .claude/agents -name "*.md" -not -name "README.md" | wc -l

# Count skills
find .claude/skills -name "*.md" -not -name "README.md" | wc -l

# Count commands
find .claude/commands -name "*.md" -not -name "README.md" | wc -l

# Count templates
find .claude/templates -name "*.md" -not -name "README.md" | wc -l

# Count hooks
find .claude/hooks -name "*.py" | wc -l
```

### Step 2: Read Registry and Compare

Read `.claude/registry.md` and extract the documented counts from the Summary section.
Compare with actual file counts from Step 1.

### Step 3: Validate Settings.json

Check `.claude/settings.json`:
- All hooks in `PreToolUse`, `PostToolUse`, `Stop` reference existing files
- All `onFileMatch` patterns reference existing skill files
- All `autoLoad` files exist

### Step 4: Validate Skill Files

For each skill in `.claude/skills/`:
- Has valid YAML frontmatter with `description`
- Has either `globs` or `alwaysApply` defined
- Contains required sections (When to Use, Implementation, etc.)

### Step 5: Check for Orphaned Files

- Find files not listed in registry
- Find registry entries pointing to non-existent files

## Output Format

```
=== Project Validation Report ===

✅ Agents: 34 (registry: 34)
✅ Skills: 29 (registry: 29)
✅ Commands: 7 (registry: 7)
✅ Templates: 6 (registry: 6)
✅ Hooks: 5 (all wired)

Settings Validation:
✅ All hook files exist
✅ All autoLoad files exist
✅ All onFileMatch skills exist

Skill Validation:
✅ All skills have valid frontmatter
✅ All skills have required sections

Issues Found: 0

=== Validation Complete ===
```

## If Issues Are Found

Report each issue with:
- File path
- Issue type (missing, mismatch, invalid)
- Suggested fix

Example:
```
❌ Skills: 30 (registry says: 29)
   → Update registry.md Summary section

❌ Hook not found: .claude/hooks/missing-hook.py
   → Remove from settings.json or create the file

❌ Skill missing frontmatter: .claude/skills/broken-skill.md
   → Add YAML frontmatter with description and globs
```

## Auto-Fix Option

After reporting issues, offer to auto-fix:
- Update registry counts
- Remove references to missing files
- Add missing frontmatter templates

## When to Run

Run `/project:validate` after:
- Adding new agents, skills, or commands
- Modifying settings.json
- Before committing changes
- After pulling updates from remote
