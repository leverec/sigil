# Documentation

All documentation for `src/`, `tests/`, and `bin/` is organized in this directory.

## Documentation Structure

Documentation files follow a consistent naming convention:

```
<directory>_<small-desc>.<ext>
```

Where:
- `<directory>` is the target directory being documented (e.g., `src`, `tests`, `bin`)
- `<small-desc>` is a brief description of what the document covers
- `<ext>` is either `.md` (Markdown) or `.txt` (plain text)

### Examples

- `src_overview.md` - Overview and architecture of the src directory
- `src_functions.md` - Documentation of individual functions in src
- `bin_sigil-sh.md` - Documentation for the sigil.sh shell script
- `tests_setup.txt` - How to set up and run tests

## Adding Documentation

When adding new documentation:

1. Choose the appropriate directory (`src`, `tests`, or `bin`)
2. Create a file named `<directory>_<description>.md` or `<directory>_<description>.txt`
3. Keep descriptions short and lowercase (e.g., `src_module-loading`, not `src_ModuleLoadingSystem`)
4. Use Markdown (`.md`) for formatted documentation with code blocks and structure
5. Use plain text (`.txt`) only for simple reference files

## Contributing to Docs

All documentation contributions follow the same process as code contributions. See [CONTRIBUTING.md](../CONTRIBUTING.md) for the pull request workflow.

When updating code, please update the corresponding documentation file if behavior or structure changes.
