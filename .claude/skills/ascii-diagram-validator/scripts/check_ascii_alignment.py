#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
ASCII Diagram Alignment Validator & Fixer

Validates alignment of box-drawing characters in enclosed box diagrams.
Skips file tree structures (├── patterns) and handles arrow characters.
Supports auto-fix mode to correct alignment issues in-place.

Usage:
    uv run check_ascii_alignment.py <file_or_directory> [options]

Examples:
    uv run check_ascii_alignment.py docs/ARCHITECTURE.md
    uv run check_ascii_alignment.py docs/*.md --fix
    uv run check_ascii_alignment.py docs/ --verbose
    uv run check_ascii_alignment.py docs/ --fix --dry-run
"""
import argparse
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# ─── Unicode Width Detection ────────────────────────────────────────────────

def _is_wide_char(cp: int) -> bool:
    """Check if a codepoint has display width 2 (CJK, fullwidth, etc.)."""
    return ((0xFF01 <= cp <= 0xFF60) or (0xFFE0 <= cp <= 0xFFE6) or
            (0x3000 <= cp <= 0x303F) or (0x2E80 <= cp <= 0x9FFF) or
            (0xAC00 <= cp <= 0xD7AF) or (0xF900 <= cp <= 0xFAFF) or
            (0xFE30 <= cp <= 0xFE4F) or (0xFF01 <= cp <= 0xFF5E) or
            (0x1F300 <= cp <= 0x1F9FF) or (0x20000 <= cp <= 0x2FA1F))


def display_width(line: str) -> int:
    """Calculate display width of a string, accounting for wide characters."""
    w = 0
    for ch in line:
        w += 2 if _is_wide_char(ord(ch)) else 1
    return w


def iter_display_cols(line: str):
    """Yield (display_col, char, char_index) for each character in line."""
    dcol = 0
    for idx, ch in enumerate(line):
        yield dcol, ch, idx
        dcol += 2 if _is_wide_char(ord(ch)) else 1


def char_index_at_dcol(line: str, target_dcol: int) -> int | None:
    """Map display column to character index. Returns None if out of bounds."""
    dcol = 0
    for idx, ch in enumerate(line):
        if dcol == target_dcol:
            return idx
        dcol += 2 if _is_wide_char(ord(ch)) else 1
    return None


def char_at_dcol(line: str, target_dcol: int) -> str | None:
    """Get character at display column. Returns None if out of bounds."""
    idx = char_index_at_dcol(line, target_dcol)
    return line[idx] if idx is not None else None


def replace_at_dcol(line: str, target_dcol: int, replacement: str) -> str:
    """Replace character at display column with replacement string."""
    dcol = 0
    for idx, ch in enumerate(line):
        if dcol == target_dcol:
            return line[:idx] + replacement + line[idx + 1:]
        dcol += 2 if _is_wide_char(ord(ch)) else 1
    return line


def pad_to_width(line: str, target_width: int, pad_char: str = ' ') -> str:
    """Pad or truncate line to target display width.
    For border lines, removes ─ characters instead of truncating at the end."""
    current = display_width(line)
    if current < target_width:
        return line + pad_char * (target_width - current)
    elif current > target_width:
        diff = current - target_width
        chars = list(line)
        removed = 0
        i = len(chars) - 1
        while removed < diff and i >= 0:
            ch = chars[i]
            if ch in HORIZONTAL:
                chars.pop(i)
                removed += 1
                i -= 1
            else:
                i -= 1
        if removed < diff:
            new_line = ''
            dcol = 0
            for ch in line:
                cw = 2 if _is_wide_char(ord(ch)) else 1
                if dcol + cw <= target_width:
                    new_line += ch
                    dcol += cw
                else:
                    break
            return new_line
        return ''.join(chars)
    return line


# ─── Box-Drawing Character Sets ─────────────────────────────────────────────

SINGLE_HORIZONTAL = set('─')
SINGLE_VERTICAL = set('│')
DOUBLE_HORIZONTAL = set('═')
DOUBLE_VERTICAL = set('║')
HEAVY_HORIZONTAL = set('━')
HEAVY_VERTICAL = set('┃')

HORIZONTAL = SINGLE_HORIZONTAL | DOUBLE_HORIZONTAL | HEAVY_HORIZONTAL
VERTICAL = SINGLE_VERTICAL | DOUBLE_VERTICAL | HEAVY_VERTICAL

CORNER_TL_LIGHT = set('┌')
CORNER_TR_LIGHT = set('┐')
CORNER_BL_LIGHT = set('└')
CORNER_BR_LIGHT = set('┘')
CORNER_TL_DOUBLE = set('╔')
CORNER_TR_DOUBLE = set('╗')
CORNER_BL_DOUBLE = set('╚')
CORNER_BR_DOUBLE = set('╝')
CORNER_TL_HEAVY = set('┏')
CORNER_TR_HEAVY = set('┓')
CORNER_BL_HEAVY = set('┗')
CORNER_BR_HEAVY = set('┛')
CORNER_TL_ROUNDED = set('╭')
CORNER_TR_ROUNDED = set('╮')
CORNER_BL_ROUNDED = set('╰')
CORNER_BR_ROUNDED = set('╯')

CORNER_TL = CORNER_TL_LIGHT | CORNER_TL_DOUBLE | CORNER_TL_HEAVY | CORNER_TL_ROUNDED
CORNER_TR = CORNER_TR_LIGHT | CORNER_TR_DOUBLE | CORNER_TR_HEAVY | CORNER_TR_ROUNDED
CORNER_BL = CORNER_BL_LIGHT | CORNER_BL_DOUBLE | CORNER_BL_HEAVY | CORNER_BL_ROUNDED
CORNER_BR = CORNER_BR_LIGHT | CORNER_BR_DOUBLE | CORNER_BR_HEAVY | CORNER_BR_ROUNDED
CORNERS = CORNER_TL | CORNER_TR | CORNER_BL | CORNER_BR

T_LEFT_LIGHT = set('├')
T_RIGHT_LIGHT = set('┤')
T_TOP_LIGHT = set('┬')
T_BOTTOM_LIGHT = set('┴')
T_LEFT_DOUBLE = set('╠╞╟')
T_RIGHT_DOUBLE = set('╣╡╢')
T_TOP_DOUBLE = set('╦╤╥')
T_BOTTOM_DOUBLE = set('╩╧╨')
T_LEFT_HEAVY = set('┣┡┢┝┞┟┠')
T_RIGHT_HEAVY = set('┫┥┦┧┨┩┪')
T_TOP_HEAVY = set('┳┭┮┯┰┱┲')
T_BOTTOM_HEAVY = set('┻┵┶┷┸┹┺')

T_LEFT = T_LEFT_LIGHT | T_LEFT_DOUBLE | T_LEFT_HEAVY
T_RIGHT = T_RIGHT_LIGHT | T_RIGHT_DOUBLE | T_RIGHT_HEAVY
T_TOP = T_TOP_LIGHT | T_TOP_DOUBLE | T_TOP_HEAVY
T_BOTTOM = T_BOTTOM_LIGHT | T_BOTTOM_DOUBLE | T_BOTTOM_HEAVY
T_JUNCTIONS = T_LEFT | T_RIGHT | T_TOP | T_BOTTOM

CROSSES = set('┼╬╪╫╋')

ARROWS = set('▶▷►▻▸▹→⟶⟹▼▽▾▿↓⇓◀◁◄◅◂◃←⟵⟸▲△▴▵↑⇑∨∧<>')
BLOCK_ELEMENTS = set('▐▌▀▄█░▒▓')
ELLIPSIS_CHARS = set('⋮⋯…')
VALID_TERMINATORS = ARROWS | BLOCK_ELEMENTS | ELLIPSIS_CHARS

ALL_BOX_CHARS = HORIZONTAL | VERTICAL | CORNERS | T_JUNCTIONS | CROSSES

CONNECTS_UP = VERTICAL | CORNER_BL | CORNER_BR | T_LEFT | T_RIGHT | T_BOTTOM | CROSSES
CONNECTS_DOWN = VERTICAL | CORNER_TL | CORNER_TR | T_LEFT | T_RIGHT | T_TOP | CROSSES
CONNECTS_LEFT = HORIZONTAL | CORNER_TR | CORNER_BR | T_TOP | T_BOTTOM | T_RIGHT | CROSSES
CONNECTS_RIGHT = HORIZONTAL | CORNER_TL | CORNER_BL | T_TOP | T_BOTTOM | T_LEFT | CROSSES

FILE_TREE_PATTERN = re.compile(r'[├└]── ')


# ─── Data Models ─────────────────────────────────────────────────────────────

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    file: str
    line: int
    column: int
    severity: Severity
    message: str
    suggestion: str | None = None
    fix_type: str | None = None
    fix_expected: str | None = None

    def __str__(self) -> str:
        base = f"{self.file}:{self.line}:{self.column}: {self.severity.value}: {self.message}"
        if self.suggestion:
            base += f"\n  → Suggestion: {self.suggestion}"
        return base


# ─── Block Detection ─────────────────────────────────────────────────────────

def is_file_tree_block(lines: list[str]) -> bool:
    tree_line_count = 0
    for line in lines:
        if FILE_TREE_PATTERN.search(line):
            tree_line_count += 1
    return tree_line_count > len(lines) * 0.2


def _find_corner_in_line(line: str):
    """Find first corner character and its display column in a line.
    Handles leading whitespace (indented boxes)."""
    dcol = 0
    for ch in line:
        if ch in CORNERS:
            return dcol, ch
        dcol += 2 if _is_wide_char(ord(ch)) else 1
    return None, None


def is_enclosed_box_diagram(lines: list[str]) -> bool:
    has_tl = False
    has_tr = False
    has_bl = False
    has_br = False
    for line in lines:
        dcol = 0
        for ch in line:
            if ch in CORNER_TL:
                has_tl = True
            elif ch in CORNER_TR:
                has_tr = True
            elif ch in CORNER_BL:
                has_bl = True
            elif ch in CORNER_BR:
                has_br = True
            dcol += 2 if _is_wide_char(ord(ch)) else 1
    return (has_tl and has_br) or (has_tr and has_bl) or (has_tl and has_tr and has_bl and has_br)


# ─── Box Parsing (indent-aware) ─────────────────────────────────────────────

@dataclass
class Box:
    lines: list[str]          # raw lines (with leading whitespace preserved)
    rel_rows: list[int]       # relative row indices in the block
    indent: int               # display column of the first corner (left padding)
    target_width: int         # expected display width (from top border)
    style: str                # 'single', 'double', 'heavy', 'rounded', 'mixed'


def _detect_border_style(line: str) -> str:
    """Detect box-drawing style of a border line."""
    styles = set()
    for ch in line:
        if ch in SINGLE_HORIZONTAL | SINGLE_VERTICAL | CORNER_TL_LIGHT | CORNER_TR_LIGHT | CORNER_BL_LIGHT | CORNER_BR_LIGHT | T_LEFT_LIGHT | T_RIGHT_LIGHT | T_TOP_LIGHT | T_BOTTOM_LIGHT:
            styles.add('single')
        elif ch in DOUBLE_HORIZONTAL | DOUBLE_VERTICAL | CORNER_TL_DOUBLE | CORNER_TR_DOUBLE | CORNER_BL_DOUBLE | CORNER_BR_DOUBLE | T_LEFT_DOUBLE | T_RIGHT_DOUBLE | T_TOP_DOUBLE | T_BOTTOM_DOUBLE:
            styles.add('double')
        elif ch in HEAVY_HORIZONTAL | HEAVY_VERTICAL | CORNER_TL_HEAVY | CORNER_TR_HEAVY | CORNER_BL_HEAVY | CORNER_BR_HEAVY | T_LEFT_HEAVY | T_RIGHT_HEAVY | T_TOP_HEAVY | T_BOTTOM_HEAVY:
            styles.add('heavy')
        elif ch in CORNER_TL_ROUNDED | CORNER_TR_ROUNDED | CORNER_BL_ROUNDED | CORNER_BR_ROUNDED:
            styles.add('rounded')
    if len(styles) == 0:
        return 'unknown'
    if len(styles) == 1:
        return styles.pop()
    return 'mixed'


def parse_boxes(lines: list[str]) -> list[Box]:
    """Parse lines into individual boxes. Handles nested and adjacent boxes.
    Returns list of Box objects with their line ranges."""
    boxes = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        first_dcol, first_ch = _find_corner_in_line(line)

        if first_ch in CORNER_TL:
            has_t_junction = any(ch in (T_JUNCTIONS | CROSSES) for ch in line)
            if has_t_junction:
                i += 1
                continue
            box_lines = [line]
            box_rows = [i]
            corner_dcol = first_dcol
            border_style = _detect_border_style(line)
            target_w = display_width(line)
            i += 1

            while i < n:
                cline = lines[i]
                cfirst_dcol, cfirst_ch = _find_corner_in_line(cline)
                box_lines.append(cline)
                box_rows.append(i)
                if cfirst_ch in CORNER_BL:
                    break
                i += 1

            boxes.append(Box(
                lines=box_lines,
                rel_rows=box_rows,
                indent=corner_dcol,
                target_width=target_w,
                style=border_style,
            ))
        i += 1

    return boxes


# ─── Validation Functions ────────────────────────────────────────────────────

def get_char_at(lines: list[str], row: int, col: int) -> str | None:
    """Get character at display column `col` in `lines[row]`."""
    if row < 0 or row >= len(lines):
        return None
    return char_at_dcol(lines[row], col)


def find_box_chars_in_line(line: str) -> list[tuple[int, str]]:
    """Find all box-drawing characters in a line with their display column positions."""
    results = []
    for dcol, ch, _idx in iter_display_cols(line):
        if ch in ALL_BOX_CHARS:
            results.append((dcol, ch))
    return results


def check_vertical_alignment(
    lines: list[str], row: int, dcol: int, char: str, file: str
) -> list[Issue]:
    issues = []

    if char in CONNECTS_UP:
        above = get_char_at(lines, row - 1, dcol)
        if above is not None and above not in CONNECTS_DOWN and above not in ' \t' and above not in VALID_TERMINATORS and above not in HORIZONTAL:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"vertical connector '{char}' at column {dcol + 1} has no matching character above (found '{above}')",
                suggestion=f"Add '│', '├', '┤', '┬', or '┼' at line {row}, column {dcol + 1}",
            ))

    if char in CONNECTS_DOWN:
        below = get_char_at(lines, row + 1, dcol)
        if below is not None and below not in CONNECTS_UP and below not in ' \t' and below not in VALID_TERMINATORS and below not in HORIZONTAL:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"vertical connector '{char}' at column {dcol + 1} has no matching character below (found '{below}')",
                suggestion=f"Add '│', '├', '┤', '┴', or '┼' at line {row + 2}, column {dcol + 1}",
            ))

    return issues


def check_horizontal_alignment(
    lines: list[str], row: int, dcol: int, char: str, file: str
) -> list[Issue]:
    issues = []
    line = lines[row]

    if char in CONNECTS_LEFT:
        left = get_char_at(lines, row, dcol - 1)
        if dcol > 0 and left is not None and left not in CONNECTS_RIGHT and left not in ' \t' and left not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"horizontal connector '{char}' has no matching character to the left (found '{left}')",
                suggestion=f"Add '─', '┌', '└', '┬', '┴', or '┼' at column {dcol}",
            ))

    if char in CONNECTS_RIGHT:
        right = get_char_at(lines, row, dcol + 1)
        line_dw = display_width(line)
        if dcol < line_dw - 1 and right is not None and right not in CONNECTS_LEFT and right not in ' \t' and right not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"horizontal connector '{char}' has no matching character to the right (found '{right}')",
                suggestion=f"Add '─', '┐', '┘', '┬', '┴', or '┼' at column {dcol + 2}",
            ))

    return issues


def check_corner_connections(
    lines: list[str], row: int, dcol: int, char: str, file: str
) -> list[Issue]:
    issues = []

    if char in CORNER_TL:
        right = get_char_at(lines, row, dcol + 1)
        below = get_char_at(lines, row + 1, dcol)
        if right is not None and right not in CONNECTS_LEFT and right not in ' \t\n' and right not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"top-left corner '{char}' not connected to the right",
                suggestion="Add horizontal line '─' or '═' after the corner",
            ))
        if below is not None and below not in CONNECTS_UP and below not in ' \t\n' and below not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"top-left corner '{char}' not connected below",
                suggestion=f"Add vertical line '│' or '║' at line {row + 2}, column {dcol + 1}",
            ))

    if char in CORNER_TR:
        left = get_char_at(lines, row, dcol - 1)
        below = get_char_at(lines, row + 1, dcol)
        if left is not None and left not in CONNECTS_RIGHT and left not in ' \t\n' and left not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"top-right corner '{char}' not connected to the left",
                suggestion="Add horizontal line '─' or '═' before the corner",
            ))
        if below is not None and below not in CONNECTS_UP and below not in ' \t\n' and below not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"top-right corner '{char}' not connected below",
                suggestion=f"Add vertical line '│' or '║' at line {row + 2}, column {dcol + 1}",
            ))

    if char in CORNER_BL:
        right = get_char_at(lines, row, dcol + 1)
        above = get_char_at(lines, row - 1, dcol)
        if right is not None and right not in CONNECTS_LEFT and right not in ' \t\n' and right not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"bottom-left corner '{char}' not connected to the right",
                suggestion="Add horizontal line '─' or '═' after the corner",
            ))
        if above is not None and above not in CONNECTS_DOWN and above not in ' \t\n' and above not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"bottom-left corner '{char}' not connected above",
                suggestion=f"Add vertical line '│' or '║' at line {row}, column {dcol + 1}",
            ))

    if char in CORNER_BR:
        left = get_char_at(lines, row, dcol - 1)
        above = get_char_at(lines, row - 1, dcol)
        if left is not None and left not in CONNECTS_RIGHT and left not in ' \t\n' and left not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"bottom-right corner '{char}' not connected to the left",
                suggestion="Add horizontal line '─' or '═' before the corner",
            ))
        if above is not None and above not in CONNECTS_DOWN and above not in ' \t\n' and above not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file, line=row + 1, column=dcol + 1,
                severity=Severity.ERROR,
                message=f"bottom-right corner '{char}' not connected above",
                suggestion=f"Add vertical line '│' or '║' at line {row}, column {dcol + 1}",
            ))

    return issues


def check_box_row_widths(box: Box, file_path: str, block_start: int) -> list[Issue]:
    """Check that every row in a box has the same display width."""
    issues = []
    target = box.target_width

    for i, line in enumerate(box.lines):
        row_num = block_start + box.rel_rows[i] + 1
        w = display_width(line)

        if w != target:
            severity = Severity.ERROR if i == 0 or i == len(box.lines) - 1 else Severity.WARNING
            msg = f"row display width {w} differs from box width {target}"
            if w < target:
                suggestion = f"Add {target - w} space(s) of padding"
            else:
                suggestion = f"Remove {w - target} character(s) or adjust content"
            issues.append(Issue(
                file=file_path, line=row_num, column=1,
                severity=severity, message=msg, suggestion=suggestion,
                fix_type='row_width', fix_expected=str(target),
            ))

    return issues


def check_vertical_pipe_alignment(box: Box, file_path: str, block_start: int) -> list[Issue]:
    """Check that vertical pipes (│) at the same index position are aligned across rows.
    Only compares rows that have the same number of pipes (header vs content)."""
    issues = []
    pipe_cols_per_row: list[list[int]] = []

    for line in box.lines:
        cols = []
        for dcol, ch, _idx in iter_display_cols(line):
            if ch in SINGLE_VERTICAL:
                cols.append(dcol)
        pipe_cols_per_row.append(cols)

    if not pipe_cols_per_row:
        return issues

    from collections import Counter
    count_groups = Counter(len(c) for c in pipe_cols_per_row)

    for group_size, group_count in count_groups.items():
        if group_count < 2 or group_size < 2:
            continue

        group_rows = [i for i, c in enumerate(pipe_cols_per_row) if len(c) == group_size]

        for pipe_idx in range(group_size):
            positions = []
            for row_i in group_rows:
                positions.append((row_i, pipe_cols_per_row[row_i][pipe_idx]))

            col_values = [p for _, p in positions]
            unique_cols = sorted(set(col_values))
            if len(unique_cols) > 1:
                from collections import Counter as ColCounter
                expected = ColCounter(col_values).most_common(1)[0][0]
                for row_i, actual_col in positions:
                    if actual_col != expected:
                        row_num = block_start + box.rel_rows[row_i] + 1
                        issues.append(Issue(
                            file=file_path, line=row_num, column=actual_col + 1,
                            severity=Severity.ERROR,
                            message=f"pipe #{pipe_idx + 1} at display column {actual_col + 1} is misaligned (expected column {expected + 1})",
                            suggestion=f"Move pipe to column {expected + 1} or adjust padding",
                            fix_type='pipe_align', fix_expected=str(expected),
                        ))

    return issues


# ─── Code Block Extraction ───────────────────────────────────────────────────

def extract_code_blocks(content: str) -> list[tuple[int, list[str]]]:
    blocks = []
    lines = content.split('\n')
    in_block = False
    block_start = 0
    block_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('```'):
            if in_block:
                blocks.append((block_start, block_lines))
                block_lines = []
                in_block = False
            else:
                in_block = True
                block_start = i + 1
        elif in_block:
            block_lines.append(line)

    return blocks


# ─── Block Validation ────────────────────────────────────────────────────────

def validate_block(block_lines: list[str], block_start: int, file_path: str, verbose: bool) -> list[Issue]:
    issues = []

    has_box_chars = any(
        any(c in ALL_BOX_CHARS for c in line)
        for line in block_lines
    )
    if not has_box_chars:
        return issues

    if is_file_tree_block(block_lines):
        if verbose:
            print(f"    Skipping file tree structure at line {block_start + 1}")
        return issues

    if not is_enclosed_box_diagram(block_lines):
        if verbose:
            print(f"    Skipping non-enclosed diagram at line {block_start + 1}")
        return issues

    boxes = parse_boxes(block_lines)

    if verbose:
        print(f"    Found {len(boxes)} box(es) at line {block_start + 1}")

    for box in boxes:
        box_row_issues = check_box_row_widths(box, file_path, block_start)
        issues.extend(box_row_issues)

        pipe_issues = check_vertical_pipe_alignment(box, file_path, block_start)
        issues.extend(pipe_issues)

    for rel_row, line in enumerate(block_lines):
        box_chars = find_box_chars_in_line(line)

        for dcol, char in box_chars:
            vert_issues = check_vertical_alignment(block_lines, rel_row, dcol, char, file_path)
            for issue in vert_issues:
                issues.append(Issue(
                    file=issue.file, line=block_start + issue.line,
                    column=issue.column, severity=issue.severity,
                    message=issue.message, suggestion=issue.suggestion,
                ))

            horiz_issues = check_horizontal_alignment(block_lines, rel_row, dcol, char, file_path)
            for issue in horiz_issues:
                issues.append(Issue(
                    file=issue.file, line=block_start + issue.line,
                    column=issue.column, severity=issue.severity,
                    message=issue.message, suggestion=issue.suggestion,
                ))

            if char in CORNERS:
                corner_issues = check_corner_connections(block_lines, rel_row, dcol, char, file_path)
                for issue in corner_issues:
                    issues.append(Issue(
                        file=issue.file, line=block_start + issue.line,
                        column=issue.column, severity=issue.severity,
                        message=issue.message, suggestion=issue.suggestion,
                    ))

    return issues


# ─── File Validation ─────────────────────────────────────────────────────────

def validate_file(file_path: Path, verbose: bool = False) -> list[Issue]:
    issues = []

    try:
        content = file_path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as e:
        issues.append(Issue(
            file=str(file_path), line=0, column=0,
            severity=Severity.ERROR, message=f"Could not read file: {e}",
        ))
        return issues

    code_blocks = extract_code_blocks(content)

    if verbose:
        print(f"  Found {len(code_blocks)} code block(s) in {file_path}")

    for block_start, block_lines in code_blocks:
        block_issues = validate_block(block_lines, block_start, str(file_path), verbose)
        issues.extend(block_issues)

    return issues


def validate_path(path: Path, verbose: bool = False) -> list[Issue]:
    issues = []

    if path.is_file():
        if verbose:
            print(f"Validating: {path}")
        issues.extend(validate_file(path, verbose))
    elif path.is_dir():
        for md_file in sorted(path.rglob('*.md')):
            if verbose:
                print(f"Validating: {md_file}")
            issues.extend(validate_file(md_file, verbose))
    else:
        issues.append(Issue(
            file=str(path), line=0, column=0,
            severity=Severity.ERROR, message=f"Path does not exist: {path}",
        ))

    return issues


# ─── Auto-Fix Engine ─────────────────────────────────────────────────────────

def _group_lines_by_box(lines: list[str]) -> list[tuple[int, list[int]]]:
    """Group lines into visual box units.
    Strategy: find outermost box (first ┌ to matching └), then group remaining
    lines into secondary boxes using the same depth approach.
    Returns list of (absolute_start, [line_indices])."""
    groups = []

    first_tl = None
    for i, line in enumerate(lines):
        first_dcol, first_ch = _find_corner_in_line(line)
        if first_ch in CORNER_TL:
            first_tl = i
            break

    if first_tl is None:
        for i in range(len(lines)):
            if any(c in ALL_BOX_CHARS for c in lines[i]):
                groups.append((i, [i]))
        return groups

    depth = 0
    last_br = first_tl
    for i in range(first_tl, len(lines)):
        first_dcol, first_ch = _find_corner_in_line(lines[i])
        if first_ch in CORNER_TL:
            depth += 1
        if first_ch in CORNER_BL:
            depth -= 1
            if depth == 0:
                last_br = i
                break

    outer_indices = list(range(first_tl, last_br + 1))
    groups.append((first_tl, outer_indices))

    remaining = lines[last_br + 1:]
    if remaining:
        sub_groups = _group_lines_by_box_simple(remaining)
        for sub_start, sub_indices in sub_groups:
            abs_start = last_br + 1 + sub_start
            groups.append((abs_start, [last_br + 1 + idx for idx in sub_indices]))

    return groups


def _group_lines_by_box_simple(lines: list[str]) -> list[tuple[int, list[int]]]:
    """Simple box grouping for remaining lines after outer box.
    Groups lines into box units, splitting when width changes significantly."""
    groups = []
    i = 0
    n = len(lines)

    while i < n:
        if not any(c in ALL_BOX_CHARS for c in lines[i]):
            i += 1
            continue

        group_indices = [i]
        base_dw = display_width(lines[i])
        i += 1

        while i < n:
            if not any(c in ALL_BOX_CHARS for c in lines[i]):
                break
            curr_dw = display_width(lines[i])
            if abs(curr_dw - base_dw) > 2:
                break
            first_dcol, first_ch = _find_corner_in_line(lines[i])
            if first_ch in CORNER_BL:
                group_indices.append(i)
                i += 1
                break
            group_indices.append(i)
            i += 1

        groups.append((group_indices[0], group_indices))

    return groups


def _fix_content_row(line: str, target_w: int) -> str:
    """Fix a content row (│ ... │) to match target width.
    Pads spaces between last content pipe and right border pipe."""
    dw = display_width(line)
    if dw == target_w:
        return line

    right_pipe_dcol = None
    right_pipe_idx = None
    for dcol, ch, idx in iter_display_cols(line):
        if ch in SINGLE_VERTICAL:
            right_pipe_dcol = dcol
            right_pipe_idx = idx

    if right_pipe_dcol is None or right_pipe_idx is None:
        return pad_to_width(line, target_w)

    if right_pipe_dcol == target_w - 1:
        return line

    if right_pipe_dcol < target_w - 1:
        content_part = line[:right_pipe_idx]
        right_part = line[right_pipe_idx:]
        needed = target_w - display_width(content_part) - 1  # 1 for the pipe itself
        if needed > 0:
            return content_part + ' ' * needed + right_part
        elif needed < 0:
            return pad_to_width(line, target_w)
    else:
        return pad_to_width(line, target_w)

    return line


def _fix_border_row(line: str, target_w: int) -> str:
    """Fix a border row (┌─┐, └─┘, ├─┤) to match target width."""
    dw = display_width(line)
    if dw == target_w:
        return line
    return pad_to_width(line, target_w)


def _fix_pipe_alignment(lines: list[str], indices: list[int]) -> list[str]:
    """Align pipes across rows that have the same pipe count."""
    fixed = list(lines)

    pipe_groups: dict[int, list[int]] = {}
    for i in indices:
        cols = []
        for dcol, ch, _idx in iter_display_cols(fixed[i]):
            if ch in SINGLE_VERTICAL:
                cols.append(dcol)
        if cols:
            pipe_groups.setdefault(len(cols), []).append(i)

    for group_size, row_indices in pipe_groups.items():
        if len(row_indices) < 2 or group_size < 2:
            continue

        for pipe_idx in range(group_size):
            positions = []
            for row_i in row_indices:
                cols = []
                for dcol, ch, _idx in iter_display_cols(fixed[row_i]):
                    if ch in SINGLE_VERTICAL:
                        cols.append(dcol)
                if pipe_idx < len(cols):
                    positions.append((row_i, cols[pipe_idx]))

            if len(positions) < 2:
                continue

            col_vals = [p for _, p in positions]
            unique = sorted(set(col_vals))
            if len(unique) > 1:
                from collections import Counter as ColCounter
                expected = ColCounter(col_vals).most_common(1)[0][0]
                for row_i, actual in positions:
                    if actual != expected:
                        idx = char_index_at_dcol(fixed[row_i], actual)
                        if idx is not None:
                            fixed[row_i] = fixed[row_i][:idx] + '│' + fixed[row_i][idx + 1:]

    return fixed


def _fix_single_box_group(all_lines: list[str], indices: list[int]) -> list[str]:
    """Fix a group of lines forming a box. Returns fixed lines for those indices."""
    if len(indices) < 2:
        return list(all_lines[i] for i in indices)

    widths = [display_width(all_lines[i]) for i in indices]
    from collections import Counter
    most_common_w = Counter(widths).most_common(1)[0][0]

    top_dw = display_width(all_lines[indices[0]])
    bottom_dw = display_width(all_lines[indices[-1]])
    target_w = max(top_dw, bottom_dw, most_common_w)

    fixed_lines = [list(all_lines[i]) for i in indices]
    fixed_strs = [all_lines[i] for i in indices]

    for pos, idx in enumerate(indices):
        line = fixed_strs[pos]
        dw = display_width(line)
        if dw == target_w:
            continue

        stripped = line.strip()
        is_border = False
        if stripped.startswith(('┌', '╔', '┏', '╭')) and (stripped.endswith(('┐', '╗', '┓', '╮')) or '─' in stripped or '═' in stripped or '━' in stripped):
            is_border = True
        if stripped.startswith(('└', '╚', '┗', '╰')) and (stripped.endswith(('┘', '╝', '┛', '╯')) or '─' in stripped or '═' in stripped or '━' in stripped):
            is_border = True
        if stripped.startswith(('├', '╠', '┣')) or stripped.startswith(('┤', '╣', '┫')):
            is_border = True

        if is_border:
            fixed_strs[pos] = _fix_border_row(line, target_w)
        else:
            first_dcol, first_ch = _find_corner_in_line(line)
            if first_ch in VERTICAL:
                fixed_strs[pos] = _fix_content_row(line, target_w)
            elif line.lstrip() and line.lstrip()[0] in VERTICAL:
                fixed_strs[pos] = _fix_content_row(line, target_w)
            else:
                fixed_strs[pos] = pad_to_width(line, target_w)

    fixed_strs = _fix_pipe_alignment(fixed_strs, list(range(len(fixed_strs))))

    return fixed_strs


def _fix_block(block_lines: list[str]) -> list[str]:
    """Fix alignment issues in a single code block. Returns fixed lines."""
    if not is_enclosed_box_diagram(block_lines):
        return block_lines

    groups = _group_lines_by_box(block_lines)
    fixed = list(block_lines)

    for start, indices in groups:
        has_box = any(any(c in ALL_BOX_CHARS for c in block_lines[i]) for i in indices)
        has_corner = any(any(c in CORNERS for c in block_lines[i]) for i in indices)
        if not has_box or not has_corner:
            continue
        if len(indices) < 2:
            continue

        fixed_group = _fix_single_box_group(block_lines, indices)
        for pos, idx in enumerate(indices):
            if fixed_group[pos] != block_lines[idx]:
                fixed[idx] = fixed_group[pos]

    return fixed


def fix_file(file_path: Path, dry_run: bool = False, verbose: bool = False) -> tuple[int, str | None]:
    """Fix alignment issues in a file. Returns (fix_count, diff_or_none)."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return 0, None

    lines = content.split('\n')
    fixed_lines = list(lines)
    total_fixes = 0

    code_blocks = extract_code_blocks(content)
    for block_start, block_lines in code_blocks:
        if not is_enclosed_box_diagram(block_lines):
            continue
        if is_file_tree_block(block_lines):
            continue

        fixed_block = _fix_block(block_lines)
        for i, (old, new) in enumerate(zip(block_lines, fixed_block)):
            if old != new:
                line_idx = block_start + i
                if line_idx < len(fixed_lines):
                    fixed_lines[line_idx] = new
                    total_fixes += 1
                    if verbose:
                        print(f"  Fixed line {line_idx + 1}:")
                        print(f"    - {repr(old)}")
                        print(f"    + {repr(new)}")

    if total_fixes == 0:
        return 0, None

    new_content = '\n'.join(fixed_lines)

    if dry_run:
        old_lines = lines
        new_lines = fixed_lines
        diff_parts = []
        for i, (old, new) in enumerate(zip(old_lines, new_lines)):
            if old != new:
                diff_parts.append(f"  L{i + 1}:")
                diff_parts.append(f"  - {old}")
                diff_parts.append(f"  + {new}")
        return total_fixes, '\n'.join(diff_parts)
    else:
        file_path.write_text(new_content, encoding='utf-8')
        return total_fixes, None


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Validate and fix ASCII box-drawing diagram alignment in markdown files',
    )
    parser.add_argument(
        'paths', nargs='+', type=Path,
        help='Files or directories to validate',
    )
    parser.add_argument(
        '--warn-only', action='store_true',
        help='Exit 0 even if warnings found (still exit 1 on errors)',
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Print verbose progress information',
    )
    parser.add_argument(
        '--fix', action='store_true',
        help='Auto-fix alignment issues in-place',
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what --fix would change without modifying files',
    )

    args = parser.parse_args()

    if args.dry_run and not args.fix:
        parser.error('--dry-run requires --fix')

    if args.fix:
        total_fixed = 0
        for path in args.paths:
            if path.is_file():
                fixes, diff = fix_file(path, dry_run=args.dry_run, verbose=args.verbose)
                total_fixed += fixes
                if fixes > 0:
                    if args.dry_run and diff:
                        print(f"\n{path}: {fixes} fix(es) would be applied:")
                        print(diff)
                    else:
                        print(f"{path}: {fixes} fix(es) applied")
                elif args.verbose:
                    print(f"{path}: no fixes needed")
            elif path.is_dir():
                for md_file in sorted(path.rglob('*.md')):
                    fixes, diff = fix_file(md_file, dry_run=args.dry_run, verbose=args.verbose)
                    total_fixed += fixes
                    if fixes > 0:
                        if args.dry_run and diff:
                            print(f"\n{md_file}: {fixes} fix(es) would be applied:")
                            print(diff)
                        else:
                            print(f"{md_file}: {fixes} fix(es) applied")

        if total_fixed > 0:
            print(f"\nTotal: {total_fixed} fix(es) {'would be applied' if args.dry_run else 'applied'}")
        else:
            print("No fixes needed")
        sys.exit(0)

    all_issues: list[Issue] = []
    for path in args.paths:
        all_issues.extend(validate_path(path, args.verbose))

    seen = set()
    unique_issues = []
    for issue in all_issues:
        key = (issue.file, issue.line, issue.column, issue.message)
        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    unique_issues.sort(key=lambda i: (i.file, i.line, i.column))

    for issue in unique_issues:
        print(issue)

    error_count = sum(1 for i in unique_issues if i.severity == Severity.ERROR)
    warning_count = sum(1 for i in unique_issues if i.severity == Severity.WARNING)
    info_count = sum(1 for i in unique_issues if i.severity == Severity.INFO)

    if unique_issues:
        print(f"\n{'─' * 60}")
        print(f"Summary: {error_count} error(s), {warning_count} warning(s), {info_count} info")

    if error_count > 0:
        sys.exit(1)
    elif warning_count > 0 and not args.warn_only:
        sys.exit(2)
    else:
        if not unique_issues:
            print("✓ No alignment issues found")
        sys.exit(0)


if __name__ == '__main__':
    main()
