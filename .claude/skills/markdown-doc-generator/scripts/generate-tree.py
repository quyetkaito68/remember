#!/usr/bin/env python3
"""
Folder Tree Generator - Sinh cây thư mục ASCII/Unicode
Usage: python generate-tree.py [path] [options]
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Set, Optional

# Unicode box-drawing characters for tree
TREE_CHARS = {
    'branch': '├── ',
    'last_branch': '└── ',
    'vertical': '│   ',
    'space': '    ',
}

# Default ignore patterns
DEFAULT_IGNORE = {
    '.git', '.github', '.gitignore', '.gitmodules',
    '__pycache__', '*.pyc', '.pytest_cache', '.coverage',
    'node_modules', 'dist', 'build', '.next', '.nuxt',
    'target', 'Cargo.lock', '*.log',
    '.DS_Store', 'Thumbs.db',
    '.env', '.env.local', '.env.*.local',
    '*.swp', '*.swo', '*~',
    '.idea', '.vscode', '*.swp',
    'venv', 'env', '.venv', 'virtualenv',
    '.mypy_cache', '.ruff_cache',
    'coverage', '.nyc_output',
    'vendor', 'bower_components',
}

def should_ignore(name: str, ignore_patterns: Set[str]) -> bool:
    """Check if file/directory should be ignored."""
    # Exact match
    if name in ignore_patterns:
        return True
    # Pattern match (simple glob)
    for pattern in ignore_patterns:
        if pattern.startswith('*') and name.endswith(pattern[1:]):
            return True
        if pattern.endswith('*') and name.startswith(pattern[:-1]):
            return True
    return False

def get_tree_entries(path: Path, ignore_patterns: Set[str], show_hidden: bool = False) -> List[Path]:
    """Get sorted directory entries, filtering ignored."""
    try:
        entries = list(path.iterdir())
    except PermissionError:
        return []

    filtered = []
    for entry in entries:
        if not show_hidden and entry.name.startswith('.'):
            continue
        if should_ignore(entry.name, ignore_patterns):
            continue
        filtered.append(entry)

    # Sort: directories first, then files, both alphabetically
    filtered.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
    return filtered

def generate_tree(
    root: Path,
    prefix: str = '',
    ignore_patterns: Set[str] = None,
    max_depth: int = -1,
    current_depth: int = 0,
    show_hidden: bool = False,
    show_size: bool = False,
    follow_symlinks: bool = False
) -> List[str]:
    """Recursively generate tree lines."""
    if ignore_patterns is None:
        ignore_patterns = DEFAULT_IGNORE.copy()

    if max_depth >= 0 and current_depth > max_depth:
        return []

    lines = []
    entries = get_tree_entries(root, ignore_patterns, show_hidden)

    for i, entry in enumerate(entries):
        is_last = (i == len(entries) - 1)
        branch_char = TREE_CHARS['last_branch'] if is_last else TREE_CHARS['branch']

        # Build display name
        name = entry.name
        if entry.is_dir():
            name += '/'
        elif entry.is_symlink() and not follow_symlinks:
            name += ' @'

        # Add size if requested
        size_str = ''
        if show_size and entry.is_file():
            try:
                size = entry.stat().st_size
                if size < 1024:
                    size_str = f' ({size}B)'
                elif size < 1024 * 1024:
                    size_str = f' ({size/1024:.1f}KB)'
                else:
                    size_str = f' ({size/(1024*1024):.1f}MB)'
            except OSError:
                pass

        lines.append(f'{prefix}{branch_char}{name}{size_str}')

        # Recurse into directories
        if entry.is_dir() and (not entry.is_symlink() or follow_symlinks):
            next_prefix = prefix + (TREE_CHARS['space'] if is_last else TREE_CHARS['vertical'])
            lines.extend(generate_tree(
                entry, next_prefix, ignore_patterns, max_depth,
                current_depth + 1, show_hidden, show_size, follow_symlinks
            ))

    return lines

def main():
    parser = argparse.ArgumentParser(
        description='Generate ASCII/Unicode folder tree',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate-tree.py                    # Current directory
  python generate-tree.py /path/to/project   # Specific path
  python generate-tree.py -d 2               # Max depth 2
  python generate-tree.py -a                 # Show hidden files
  python generate-tree.py -s                 # Show file sizes
  python generate-tree.py -I "*.test.ts"     # Additional ignore pattern
        """
    )

    parser.add_argument('path', nargs='?', default='.', help='Root directory path')
    parser.add_argument('-d', '--depth', type=int, default=-1, help='Max depth (-1 for unlimited)')
    parser.add_argument('-a', '--all', action='store_true', help='Show hidden files')
    parser.add_argument('-s', '--size', action='store_true', help='Show file sizes')
    parser.add_argument('-I', '--ignore', action='append', default=[], help='Additional ignore patterns')
    parser.add_argument('-L', '--follow-links', action='store_true', help='Follow symlinks')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--no-root', action='store_true', help="Don't show root directory name")

    args = parser.parse_args()

    root_path = Path(args.path).resolve()
    if not root_path.exists():
        print(f"Error: Path '{root_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    if not root_path.is_dir():
        print(f"Error: '{root_path}' is not a directory", file=sys.stderr)
        sys.exit(1)

    # Combine ignore patterns
    ignore_patterns = DEFAULT_IGNORE.copy()
    ignore_patterns.update(args.ignore)

    # Generate tree
    output_lines = []

    if not args.no_root:
        output_lines.append(f'{root_path.name}/')

    tree_lines = generate_tree(
        root_path,
        ignore_patterns=ignore_patterns,
        max_depth=args.depth,
        show_hidden=args.all,
        show_size=args.size,
        follow_symlinks=args.follow_links
    )
    output_lines.extend(tree_lines)

    output = '\n'.join(output_lines)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Tree written to {args.output}")
    else:
        print(output)

if __name__ == '__main__':
    main()