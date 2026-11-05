# Contributing

Fork and clone the repository, create a focused branch, then synchronize the locked development environment:

```bash
git clone https://github.com/<username>/compas_libigl.git
cd compas_libigl
git switch -c <branch-name>
uv sync --frozen --all-groups
```

## Adding a binding

Add the C++ implementation under `src`, register its nanobind module in `CMakeLists.txt`, and add the public Python wrapper under `src/compas_libigl`. Keep native modules small and use the existing modules as concrete examples rather than introducing a new binding layer.

Rebuild after changing C++ code:

```bash
uv sync --reinstall-package compas-libigl --frozen --all-groups
```

Add focused tests for the public behavior and failure modes. Tests must write generated files only to pytest temporary directories.

Document public behavior with MkDocs-compatible NumPy-style docstrings and update the API or examples when the user-facing contract changes. Run the authoritative checks before opening a pull request:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
uv run mkdocs build --strict
uv build
```

Add a concise entry to `CHANGELOG.md`, push the branch to your fork, and open a pull request for review.
