# Contributing to Sigil

Thank you for taking the time to contribute. This document outlines the process and guidelines for contributing to Sigil.

> Please read [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) before contributing.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:

```bash
git clone https://github.com/<your-username>/sigil.git
cd sigil
```

3. Set the upstream remote:

```bash
git remote add upstream https://github.com/leverec/sigil.git
```

4. Create a new branch for your work:

```bash
git checkout -b your-branch-name
```

## How to Contribute

### Reporting Bugs

Before opening a new issue, search the existing issues to avoid duplicates.

When filing a bug report, include:

- A clear and descriptive title
- Steps to reproduce the problem
- Expected behavior vs actual behavior
- Your environment (OS, Python version, shell)
- Any relevant error output or logs

### Suggesting Features

Open an issue with the label `enhancement`. Describe:

- What the feature does
- Why it would be useful
- Any implementation ideas you have in mind

### Submitting a Pull Request

1. Make sure your branch is up to date with upstream:

```bash
git fetch upstream
git rebase upstream/main
```

2. Make your changes and write tests where applicable.
3. Run the test suite and confirm everything passes:

```bash
python3 -m pytest -v
```

4. Push your branch and open a pull request against `main`.
5. Fill out the pull request description clearly, referencing any related issues.

Pull requests that break existing tests or lack a clear description will not be merged until those issues are addressed.

## Development Guidelines

### Project Structure

```text
sigil/
  bin/          # Shell entry point
  docs/         # Documentation
  src/          # Core source code
  tests/        # Test suite
  tools/        # User-facing tools
  installer.sh  # Installer
```

Place new source logic under `src/`, new tools under `tools/`, and tests under `tests/`.

### Code Style

- Target Python 3.6 compatibility at minimum (the project supports Python 3.6+).
- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Keep functions small and focused on a single responsibility.
- Add comments where the intent is not immediately obvious, but prefer clear naming over excessive comments.
- Shell scripts should be POSIX-compatible where possible.

### Writing Tests

- Use `pytest` for all tests.
- Place test files under `tests/` with the naming convention `test_<module>.py`.
- Each new feature or bug fix should be accompanied by at least one test.
- Run the full suite before submitting:

```bash
python3 -m pytest -v
```

## Commit Message Convention

Use the following format:

```
<type>: <short summary>
```

Types:

| Type     | When to use                                      |
|----------|--------------------------------------------------|
| feat     | A new feature                                    |
| fix      | A bug fix                                        |
| docs     | Documentation changes only                       |
| test     | Adding or updating tests                         |
| refactor | Code change that is not a fix or feature         |
| chore    | Build process, dependency, or tooling changes    |

Keep the summary short (under 72 characters). Use the imperative mood: "add feature" not "added feature".

Example:

```
feat: add sghelp support to gentrees tool
fix: prevent overwrite when origin modifier is absent
docs: update usage section in README
```

Project Link: [https://github.com/leverec/sigil](https://github.com/leverec/sigil)
