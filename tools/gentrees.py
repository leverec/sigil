#!/usr/bin/env python3

# —— Import —— #
import os
import sys
import argparse
# —— Import —— #

# —— From Import —— #
from pathlib import Path
# —— From Import —— #

# —— HELP —— #
def sghelp():
    help_text = """
usage: gentrees.py [-h] [-y] [--depth N]
                   [--ignore LIST]
                   [--show-ignored]
                   [path]

Scan a directory and save its tree to tree.txt.

positional arguments:
    path            Directory to scan (default: current
                    directory)

options:
    -h, --help      Show this help message and exit
    -y, --yes       Skip all confirmation prompts
    --depth N       Maximum scan depth (default: unlimited)
    --ignore LIST   Comma-separated names/patterns to
                    ignore (added to the built-in ignore list)
    --show-ignored  Print the full ignore list and exit
"""
    print(help_text)
# —— HELP —— #

# ── Default ignore patterns ────────────────────────────────────────────────────
DEFAULT_IGNORE = {
    "__pycache__", ".DS_Store", "Thumbs.db",
    ".mypy_cache", ".ruff_cache", ".pytest_cache",
    "*.pyc", "*.pyo", ".git", f"{Path(__file__).name}"
}

# This built-in tools is just for example
# gentrees.py is made by claude
# the intent of this release is a tool that you made and you want to make it universal

def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

USE_COLOR = _supports_color()

def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text

def dim(t)    : return _c("2",     t)
def bold(t)   : return _c("1",     t)
def cyan(t)   : return _c("1;36",  t)
def green(t)  : return _c("1;32",  t)
def yellow(t) : return _c("1;33",  t)
def red(t)    : return _c("1;31",  t)
def gray(t)   : return _c("90",    t)
def blue(t)   : return _c("1;34",  t)
def magenta(t): return _c("1;35",  t)


# ── Tree characters ────────────────────────────────────────────────────────────

_TEE   = "├── "
_ELBOW = "└── "
_PIPE  = "│   "
_BLANK = "    "


# ── Filesystem scanner ─────────────────────────────────────────────────────────

def _is_ignored(name: str, ignore_set: set) -> bool:
    """Check if a name matches any ignore pattern (supports * wildcard suffix)."""
    if name in ignore_set:
        return True
    for pat in ignore_set:
        if pat.startswith("*") and name.endswith(pat[1:]):
            return True
    return False


def scan_directory(path, ignore, max_depth=None, _depth=0):
    """
    Recursively scan *path* and return a nested dict:
        - key   = entry name (str)
        - value = nested dict (dir) | None (file)
    Dirs come before files, both groups sorted alphabetically.
    """
    node = {}

    if max_depth is not None and _depth >= max_depth:
        return node

    try:
        entries = sorted(
            path.iterdir(),
            key=lambda e: (not e.is_dir(), e.name.lower())
        )
    except PermissionError:
        return node

    for entry in entries:
        if _is_ignored(entry.name, ignore):
            continue

        if entry.is_symlink():
            node[entry.name + " →"] = None
        elif entry.is_dir():
            node[entry.name] = scan_directory(
                entry, ignore, max_depth, _depth + 1
            )
        else:
            node[entry.name] = None

    return node


# ── Tree rendering ─────────────────────────────────────────────────────────────

def _file_color(name):
    """Return a coloured file name based on extension."""
    ext = Path(name).suffix.lower()
    if ext in {".py", ".js", ".ts", ".go", ".rs", ".c", ".cpp", ".java"}:
        return green(name)
    if ext in {".md", ".rst", ".txt"}:
        return blue(name)
    if ext in {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env"}:
        return yellow(name)
    if ext in {".sh", ".bash", ".zsh", ".fish"}:
        return magenta(name)
    if name.startswith("."):
        return dim(name)
    return name


def render_tree(node, prefix="", colorize=True):
    """Return visual tree lines. colorize=False -> plain text for tree.txt."""
    lines = []
    items = list(node.items())

    for idx, (name, value) in enumerate(items):
        is_last = idx == len(items) - 1
        conn    = _ELBOW if is_last else _TEE
        is_dir  = isinstance(value, dict)

        if colorize:
            c_conn = gray(prefix + conn)
            c_name = cyan(name + "/") if is_dir else _file_color(name)
            lines.append(c_conn + c_name)
        else:
            lines.append(f"{prefix}{conn}{name}{'/' if is_dir else ''}")

        if is_dir and value:
            child_prefix = prefix + (_BLANK if is_last else _PIPE)
            lines.extend(render_tree(value, child_prefix, colorize))
        elif is_dir and not value:
            child_prefix = prefix + (_BLANK if is_last else _PIPE)
            empty_hint = gray("(empty)") if colorize else "(empty)"
            elbow = gray(child_prefix + _ELBOW) if colorize else child_prefix + _ELBOW
            lines.append(elbow + empty_hint)

    return lines


# ── Stats ──────────────────────────────────────────────────────────────────────

def collect_stats(node, depth=1):
    """Return (total_items, dir_count, max_depth)."""
    total = 0
    dirs  = 0
    max_d = depth
    for name, value in node.items():
        total += 1
        if isinstance(value, dict):
            dirs += 1
            sub_total, sub_dirs, sub_depth = collect_stats(value, depth + 1)
            total += sub_total
            dirs  += sub_dirs
            max_d  = max(max_d, sub_depth)
    return total, dirs, max_d

# ── Prompt helpers ─────────────────────────────────────────────────────────────

def header(text):
    bar = gray("─" * 62)
    print(f"\n  {bar}")
    print(f"  {bold(text)}")
    print(f"  {bar}")


def prompt_confirm(warnings):
    """Single [Y/n] prompt listing all warnings. Returns True -> proceed."""
    label  = yellow("⚠  Warning" + ("s" if len(warnings) > 1 else "") + ":")
    bullet = yellow("•")

    print()
    print(f"  {label}")
    for w in warnings:
        print(f"    {bullet} {w}")
    print()

    try:
        raw = input(f"  {bold('Proceed anyway?')} {dim('[Y/n]')} ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False

    return raw in ("", "y", "yes")


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    if any(a in sys.argv[1:] for a in ("-h", "--help")):
        sghelp()
        sys.exit(0)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=None,
        metavar="N",
    )
    parser.add_argument(
        "--ignore",
        default="",
        metavar="LIST",
    )
    parser.add_argument(
        "--show-ignored",
        action="store_true",
    )
    parser.error = lambda message: (print("Try: sigil -h gentrees"), sys.exit(2))
    args         = parser.parse_args()
    force_yes    = args.yes

    # ── Build ignore set ───────────────────────────────────────────────────────
    ignore = set(DEFAULT_IGNORE)
    if args.ignore:
        for pat in args.ignore.split(","):
            pat = pat.strip()
            if pat:
                ignore.add(pat)

    if args.show_ignored:
        print("\n  Ignore patterns:")
        for p in sorted(ignore):
            print(f"    {dim('•')} {p}")
        print()
        sys.exit(0)

    # ── Resolve target directory ───────────────────────────────────────────────
    target = Path(args.path).resolve()

    if not target.exists():
        print(red(f"\n  ERROR: Path does not exist: {target}\n"))
        sys.exit(1)
    if not target.is_dir():
        print(red(f"\n  ERROR: Not a directory: {target}\n"))
        sys.exit(1)

    root_name = target.name
    out_path  = target / "tree.txt"

    # ── Scan ───────────────────────────────────────────────────────────────────
    header(f"🔍  Scanning  {dim(str(target))}")
    print()

    structure = scan_directory(target, ignore, max_depth=args.depth)

    # Remove tree.txt from display (we own it)
    structure.pop("tree.txt", None)

    # ── Render preview ─────────────────────────────────────────────────────────
    total, dirs, max_depth = collect_stats(structure)
    files = total - dirs

    print(f"  {cyan(root_name + '/')}")
    for line in render_tree(structure, prefix="  ", colorize=USE_COLOR):
        print(line)
    print()
    print(
        f"  {gray('→')} "
        f"{bold(str(dirs))} {'directory' if dirs == 1 else 'directories'}, "
        f"{bold(str(files))} {'file' if files == 1 else 'files'}"
        + (f"  {dim(f'(depth limited to {args.depth})')}" if args.depth else "")
    )

    # ── Gather warnings ────────────────────────────────────────────────────────
    warnings = []

    if out_path.exists():
        warnings.append("tree.txt already exists and will be overwritten")

    if total > 10:
        warnings.append(
            f"Large tree: {total} items ({dirs} dirs, {files} files)"
        )

    if max_depth >= 3:
        warnings.append(
            f"Tree is {max_depth} director{'ies' if max_depth != 1 else 'y'} deep "
            f"({root_name}{' → …' * (max_depth - 1)})"
        )

    # ── Single confirmation prompt (if needed) ─────────────────────────────────
    if warnings and not force_yes:
        if not prompt_confirm(warnings):
            print(f"\n  {yellow('Aborted.')} tree.txt was not written.\n")
            sys.exit(0)

    # ── Write tree.txt ─────────────────────────────────────────────────────────
    plain_lines = render_tree(structure, colorize=False)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"{root_name}/\n")
        for line in plain_lines:
            f.write(line + "\n")
        if args.depth or ignore - DEFAULT_IGNORE:
            f.write("\n")
            if args.depth:
                f.write(f"  [depth limited to {args.depth}]\n")
            extra = ignore - DEFAULT_IGNORE
            if extra:
                f.write(f"  [also ignored: {', '.join(sorted(extra))}]\n")

    # ── Summary ────────────────────────────────────────────────────────────────
    header("✅  Done")
    print()
    print(f"  {green('✓')} Scanned   : {bold(str(target))}")
    print(f"  {green('✓')} Saved to  : {bold(str(out_path))}")
    print(f"  {green('✓')} Items     : {dirs} dirs, {files} files")
    print()

if __name__ == "__main__":
    main()