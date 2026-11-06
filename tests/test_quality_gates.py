from pathlib import Path
import tomllib


def test_quality_gates_include_executable_documentation_examples():
    repository = Path(__file__).parents[1]
    pyproject = tomllib.loads((repository / "pyproject.toml").read_text(encoding="utf-8"))
    workflow = (repository / ".github" / "workflows" / "build.yml").read_text(encoding="utf-8")

    assert "docs/examples" in pyproject["tool"]["pyright"]["include"]
    assert "docs/examples/**/*.py" in pyproject["tool"]["ruff"]["extend-include"]
    assert "uv run pyright" in workflow
    assert "uv run ruff check ." in workflow


def test_executable_documentation_examples_have_no_type_ignores():
    examples = Path(__file__).parents[1] / "docs" / "examples"

    for example in examples.rglob("*.py"):
        assert "type:" + " ignore" not in example.read_text(encoding="utf-8")


def test_build_checks_lowest_and_current_numeric_dependencies():
    repository = Path(__file__).parents[1]
    workflow = (repository / ".github" / "workflows" / "build.yml").read_text(encoding="utf-8")

    assert "numeric-compatibility:" in workflow
    assert "numpy==1.26.0" in workflow
    assert "scipy==1.11.4" in workflow
    assert "numpy>=2,<3" in workflow
    assert "uv run --no-sync pyright --verifytypes compas_libigl --ignoreexternal" in workflow
