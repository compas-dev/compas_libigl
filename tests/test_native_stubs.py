from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

NATIVE_MODULES = (
    "_boundaries",
    "_cotmatrix",
    "_curvature",
    "_geodistance",
    "_grad",
    "_intersections",
    "_isolines",
    "_mapping",
    "_massmatrix",
    "_meshing",
    "_parametrisation",
    "_planarize",
    "_simplify",
)
PACKAGE = Path(__file__).parents[1] / "src" / "compas_libigl"


@pytest.mark.parametrize("module_name", NATIVE_MODULES)
def test_native_stub_matches_exported_functions(module_name: str) -> None:
    stub = PACKAGE / f"{module_name}.pyi"
    assert stub.is_file()

    tree = ast.parse(stub.read_text(encoding="utf-8"))
    stub_functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}

    module = importlib.import_module(f"compas_libigl.{module_name}")
    native_functions = {name for name in dir(module) if not name.startswith("_") and callable(getattr(module, name))}

    assert stub_functions == native_functions
