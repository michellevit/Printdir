#!/usr/bin/env python3
import os
import fnmatch
import argparse
import sys
import re


# Default base path where you keep most projects (customize if needed)
DEFAULT_BASE_DIR = r"C:\Users\Michelle\Documents\Coding_Projects"

# Directories we generally don't want in app trees
EXCLUDED_DIRS = {
    "node_modules", ".git", ".next", ".turbo", ".vercel",
    "dist", "build", "coverage", ".cache", ".parcel-cache",
    "__pycache__", ".pytest_cache", ".mypy_cache",
    ".vscode", ".idea", ".DS_Store",
    "out"
}


# Noisy/binary files to hide
EXCLUDED_FILE_GLOBS = [
    "*.log", "*.lock", "*.min.*", "*.map", "*.pyc",
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp", "*.svg",
    "*.ico", "*.pdf", "*.zip", "*.tar", "*.gz", "*.7z",
    "*.exe", "*.dll", "*.so", "*.dylib"
]

def file_is_excluded(name: str) -> bool:
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDED_FILE_GLOBS)

def generate_tree_lines(root: str, max_depth: int | None = None, include_files: bool = True):
    lines = []
    root = os.path.abspath(root)
    lines.append(f"|-- {os.path.basename(root) or root}")

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        rel = os.path.relpath(dirpath, root)
        depth = 0 if rel == "." else rel.count(os.sep) + 1  # children under root

        # Prune excluded directories (by name)
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]

        # Stop descending beyond max depth
        if max_depth is not None and depth >= max_depth:
            dirnames[:] = []

        dirnames.sort()
        filenames.sort()

        if rel != ".":
            indent = "  " * depth
            lines.append(f"{indent}|-- {os.path.basename(dirpath)}")

        if include_files:
            file_depth = depth + 1
            if max_depth is None or file_depth <= max_depth:
                indent_f = "  " * file_depth
                for name in filenames:
                    if not file_is_excluded(name):
                        lines.append(f"{indent_f}└── {name}")
    return lines


def _normalize(s: str) -> str:
    # lowercase, drop all non-alphanumeric chars (treat -, _, spaces the same)
    return re.sub(r'[^a-z0-9]+', '', s.lower())

def resolve_root(input_value: str | None, base_dir: str) -> str | None:
    """
    If input is a valid path, return its absolute path.
    Otherwise, treat it as a project name and search in base_dir (case/underscore/dash insensitive).
    Prefers: exact (normalized) -> startswith (normalized) -> contains (normalized).
    """
    val = (input_value or ".").strip().strip('"').strip("'")

    # If it's a path that exists (absolute or relative), use it directly
    if os.path.exists(val):
        return os.path.abspath(val)

    base_dir = os.path.abspath(base_dir)
    if not os.path.isdir(base_dir):
        print(f"Base directory not found: {base_dir}")
        return None

    try:
        entries = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    except OSError as e:
        print(f"Error reading base directory: {e}")
        return None

    q_norm = _normalize(val)
    if not q_norm:
        print("Empty project name after normalization.")
        return None

    # Build (name, normalized) pairs
    pairs = [(d, _normalize(d)) for d in entries]

    exact = [d for d, n in pairs if n == q_norm]
    starts = [d for d, n in pairs if n.startswith(q_norm)]
    contains = [d for d, n in pairs if q_norm in n]

    # Deduplicate while preserving priority order
    seen, candidates = set(), []
    for group in (exact, starts, contains):
        for d in group:
            if d not in seen:
                candidates.append(d); seen.add(d)

    if not candidates:
        print(f"No matching project folders under:\n  {base_dir}\nQuery: {val}")
        return None
    if len(candidates) == 1:
        return os.path.abspath(os.path.join(base_dir, candidates[0]))

    print("Multiple matches found:")
    for i, d in enumerate(candidates, start=1):
        print(f"  {i}. {d}")
    while True:
        choice = input("Choose a number: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(candidates):
                return os.path.abspath(os.path.join(base_dir, candidates[idx - 1]))
        print("Invalid choice. Please enter a valid number.")


def main():
    parser = argparse.ArgumentParser(description="Print a folder tree for full-stack apps.")
    parser.add_argument("target", nargs="?", help="Directory path OR project name to search in base dir.")
    parser.add_argument("--base-dir", default=DEFAULT_BASE_DIR, help="Where to search when a project name is given.")
    parser.add_argument("--max-depth", type=int, default=None, help="Optional depth limit.")
    parser.add_argument("--output-file", default=None, help="Also write output to this file.")
    args = parser.parse_args()

    # If no positional arg, prompt the user
    target = args.target
    if not target:
        try:
            target = input(f"Enter full path OR project name [{os.getcwd()}]: ").strip()
            if target == "":
                target = os.getcwd()
        except EOFError:
            target = os.getcwd()

    root = resolve_root(target, args.base_dir)
    if not root:
        return 1
    if not os.path.isdir(root):
        print(f"Not a directory: {root}")
        return 1

    lines = generate_tree_lines(root, max_depth=args.max_depth, include_files=True)

    # Print to console
    for line in lines:
        print(line)

    # Optional: also write to a file if requested
    if args.output_file:
        try:
            with open(args.output_file, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(lines) + "\n")
        except OSError as e:
            print(f"Warning: could not write output file: {e}", file=sys.stderr)

    return 0

if __name__ == "__main__":
    sys.exit(main())
