# Development environment

Install [uv](https://docs.astral.sh/uv/) and create the locked environment:

```bash
uv sync --frozen --all-groups
```

This installs the Python project and development tools. It does not install the platform compiler or SDK described in [Compiler requirements](compiler.md). The editable native extension is rebuilt when the project is synchronized after native source changes:

```bash
uv sync --reinstall-package compas-libigl --frozen --all-groups
```

Run tools through the locked environment:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
uv run mkdocs build --strict
uv build
```

The repository also provides thin Invoke conveniences for commonly sequenced commands:

```bash
uv run invoke check
uv run invoke typecheck
uv run invoke test
uv run invoke docs
```

The direct tool commands are authoritative. Invoke does not create environments, install native prerequisites, or publish releases.
