---
name: ascii-diagram
description: Validate and fix ASCII/Unicode diagram alignment in markdown. Detects misaligned borders, pipe characters, row width mismatches. Auto-fix mode. TRIGGERS - diagram alignment, ASCII art, box-drawing diagrams, fix diagram.
allowed-tools: Bash, Read, Glob, Edit
---

# ASCII Diagram Validator & Fixer

Validate and auto-fix alignment issues in ASCII/Unicode box-drawing diagrams. Accounts for CJK/fullwidth character widths.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Overview

ASCII diagrams using box-drawing characters (─│┌┐└┘├┤┬┴┼, ═║╔╗╚╝╠╣╦╩╬, ━┃┏┓┗┛, ╭╮╰╯) require precise column alignment. This skill provides:

1. **Validation** - Detects misaligned characters with file:line:column locations
2. **Auto-fix** - Corrects alignment issues in-place (`--fix` mode)
3. **Unicode-aware** - Correctly handles CJK, Vietnamese diacritics, fullwidth characters

## When to Use This Skill

Invoke when:

- Creating or editing ASCII architecture diagrams in markdown
- Reviewing documentation with box-drawing diagrams
- Fixing "diagram looks wrong" or "spacing is off" complaints
- Before committing files with diagrams
- When user mentions "ASCII alignment", "diagram alignment", "box drawing", "fix diagram"

## Quick Start

### Validate

```bash
python skills/ascii-diagram/scripts/check_ascii_alignment.py docs/FILE.md
```

### Validate + Fix

```bash
python skills/ascii-diagram/scripts/check_ascii_alignment.py docs/FILE.md --fix
```

### Preview Fix (dry-run)

```bash
python skills/ascii-diagram/scripts/check_ascii_alignment.py docs/FILE.md --fix --dry-run
```

### Validate Directory

```bash
python skills/ascii-diagram/scripts/check_ascii_alignment.py docs/ --verbose
```

## Validation Checks

| Check | Description | Severity |
|-------|-------------|----------|
| Vertical alignment | `│` must connect to matching char above/below | error |
| Corner connections | `┌┐└┘` must connect right/down/left/up properly | error |
| Pipe alignment | `│` at same index must be at same column across rows | error |
| Row width | Each row in box must have same display width | warning/error |
| Horizontal continuity | `─` must terminate at valid endpoint | error |

## Auto-Fix Capabilities

The `--fix` mode automatically corrects:

- **Row width mismatches** - Adds/removes padding to match box width
- **Border trimming** - Removes extra `─` from borders wider than content
- **Pipe misalignment** - Moves `│` to correct column

Use `--dry-run` to preview changes before applying.

## Output Format

```
docs/FILE.md:45:12: error: vertical connector '│' at column 12 has no matching character above
  → Suggestion: Add '│', '├', '┤', '┬', or '┼' at line 44, column 12

docs/FILE.md:20:1: warning: row display width 68 differs from box width 69
  → Suggestion: Add 1 space(s) of padding
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No issues found (or fixes applied) |
| 1 | Errors detected |
| 2 | Warnings only |

## Supported Characters

Single: `┌┐└┘─│├┤┬┴┼` · Double: `╔╗╚╝═║╠╣╦╩╬` · Heavy: `┏┓┗┛━┃┣┫┳┻╋` · Rounded: `╭╮╰╯`

## Integration Workflow

1. After creating/editing a diagram, run validation:
   ```bash
   python skills/ascii-diagram/scripts/check_ascii_alignment.py docs/FILE.md
   ```
2. If errors found, apply auto-fix:
   ```bash
   python skills/ascii-diagram/scripts/check_ascii_alignment.py docs/FILE.md --fix
   ```
3. Re-run validation until clean
4. For uncertain cases, preview first:
   ```bash
   python skills/ascii-diagram/scripts/check_ascii_alignment.py docs/FILE.md --fix --dry-run
   ```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| False pipe misalignment | Header row has different pipe count than content | Expected - header borders vs table separators |
| Row width warning with CJK | CJK chars render at 2 columns | Script accounts for this; check content padding |
| Mixed ASCII not detected | Using `+---+` style | Script validates Unicode box-drawing chars only |
| Tab characters | Tabs cause false positives | Convert tabs to spaces first |

## Bundled Scripts

| Script | Purpose |
|--------|---------|
| `scripts/check_ascii_alignment.py` | Main validation & fix script |
