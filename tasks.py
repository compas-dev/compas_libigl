import sys

from invoke.tasks import task


@task
def check(ctx):
    """Run all style checks."""
    ctx.run("ruff check .")
    ctx.run("ruff format --check .")


@task
def lint(ctx):
    """Run the linter."""
    ctx.run("ruff check .")


@task(name="format")
def format_code(ctx):
    """Apply lint fixes and format the codebase."""
    ctx.run("ruff check --fix .")
    ctx.run("ruff format .")


@task
def typecheck(ctx):
    """Run static type checking."""
    ctx.run(f'pyright --pythonpath "{sys.executable}"')
    ctx.run(f'pyright --pythonpath "{sys.executable}" --verifytypes compas_libigl --ignoreexternal')


@task
def test(ctx):
    """Run the test suite."""
    ctx.run("pytest")


@task
def docs(ctx):
    """Build the documentation in strict mode."""
    ctx.run("mkdocs build --strict")
