import importlib
import sys
from types import ModuleType

import numpy as np
import pytest
import compas_libigl


MESH = (
    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
    [[0, 1, 2], [0, 2, 3]],
)


def _load(monkeypatch, name, **native_functions):
    native_name = f"compas_libigl._{name}"
    native = ModuleType(native_name)
    for function_name, function in native_functions.items():
        setattr(native, function_name, function)
    monkeypatch.setitem(sys.modules, native_name, native)
    monkeypatch.setattr(compas_libigl, f"_{name}", native, raising=False)
    sys.modules.pop(f"compas_libigl.{name}", None)
    return importlib.import_module(f"compas_libigl.{name}")


@pytest.mark.parametrize(
    ("sources", "error"),
    [
        ([], ValueError),
        ([[0]], ValueError),
        ([True], TypeError),
        ([np.bool_(False)], TypeError),
        ([0.5], TypeError),
        ([-1], IndexError),
        ([4], IndexError),
        ([2**40], IndexError),
    ],
)
def test_geodistance_multiple_validates_sources_before_native_call(monkeypatch, sources, error):
    geodistance = _load(monkeypatch, "geodistance", trimesh_geodistance_multiple=lambda *args: pytest.fail("native called"))

    with pytest.raises(error):
        geodistance.trimesh_geodistance_multiple(MESH, sources)


def test_geodistance_multiple_checks_result_cardinality(monkeypatch):
    geodistance = _load(monkeypatch, "geodistance", trimesh_geodistance_multiple=lambda *args: np.zeros(3))

    with pytest.raises(RuntimeError, match="geodistance-multiple result"):
        geodistance.trimesh_geodistance_multiple(MESH, [0, 1])


@pytest.mark.parametrize(
    "rays",
    [
        [],
        [([0.0, 0.0], [0.0, 0.0, -1.0])],
        [([0.0, 0.0, np.nan], [0.0, 0.0, -1.0])],
        [([0.0, 0.0, 1.0], [0.0, 0.0, 0.0])],
    ],
)
def test_batched_ray_validation_precedes_native_call(monkeypatch, rays):
    intersections = _load(monkeypatch, "intersections", intersection_rays_mesh=lambda *args: pytest.fail("native called"))

    with pytest.raises(ValueError):
        intersections.intersection_rays_mesh(rays, MESH)


@pytest.mark.parametrize(
    "native_result",
    [
        [],
        [[(0, 0.0, 0.0)]],
    ],
)
def test_batched_ray_intersections_check_result_cardinality(monkeypatch, native_result):
    intersections = _load(monkeypatch, "intersections", intersection_rays_mesh=lambda *args: native_result)
    rays = [([0.0, 0.0, 1.0], [0.0, 0.0, -1.0])]

    with pytest.raises(RuntimeError, match="ray intersections result"):
        intersections.intersection_rays_mesh(rays, MESH)


def test_sparse_operator_wrappers_check_native_shapes(monkeypatch):
    cotmatrix = _load(
        monkeypatch,
        "cotmatrix",
        trimesh_cotmatrix=lambda *args: np.zeros((3, 3)),
        trimesh_cotmatrix_entries=lambda *args: np.zeros((3, 3)),
    )
    grad = _load(monkeypatch, "grad", trimesh_grad=lambda *args: np.zeros((5, 4)))

    with pytest.raises(RuntimeError, match="cotangent matrix result"):
        cotmatrix.trimesh_cotmatrix(MESH)
    with pytest.raises(RuntimeError, match="cotangent entries result"):
        cotmatrix.trimesh_cotmatrix_entries(MESH)
    with pytest.raises(RuntimeError, match="gradient operator result"):
        grad.trimesh_grad(MESH)


def test_curvature_wrappers_check_native_shapes(monkeypatch):
    curvature = _load(
        monkeypatch,
        "curvature",
        trimesh_gaussian_curvature=lambda *args: np.zeros(3),
        trimesh_principal_curvature=lambda *args: (
            np.zeros((4, 2)),
            np.zeros((4, 3)),
            np.zeros(4),
            np.zeros(4),
        ),
    )

    with pytest.raises(RuntimeError, match="Gaussian curvature result"):
        curvature.trimesh_gaussian_curvature(MESH)
    with pytest.raises(RuntimeError, match="principal direction 1 result"):
        curvature.trimesh_principal_curvature(MESH)


def test_isolines_check_segment_label_cardinality(monkeypatch):
    isolines = _load(
        monkeypatch,
        "isolines",
        trimesh_isolines=lambda *args: (
            np.zeros((2, 3)),
            np.zeros((2, 2), dtype=np.int32),
            np.zeros(1, dtype=np.int32),
        ),
    )

    with pytest.raises(RuntimeError, match="segment labels result"):
        isolines.trimesh_isolines(MESH, [0.0, 1.0, 1.0, 0.0], 1)


@pytest.mark.parametrize(
    ("native_result", "message"),
    [
        ((np.zeros((4, 2)), [[0, 1, 2]], np.zeros((4, 3)), [False], [0]), "mapping vertices"),
        ((np.zeros((4, 3)), [[0, 1, 2]], np.zeros((3, 3)), [False], [0]), "mapping normals"),
        ((np.zeros((4, 3)), [[0, 1, 2]], np.zeros((4, 3)), [], [0]), "boundary flags"),
        ((np.zeros((4, 3)), [[0, 1, 2]], np.zeros((4, 3)), [False], []), "polygon groups"),
    ],
)
def test_mapping_checks_native_result_shapes_and_cardinalities(monkeypatch, native_result, message):
    mapping = _load(monkeypatch, "mapping", map_mesh_with_automatic_parameterization=lambda *args: native_result)

    with pytest.raises(RuntimeError, match=message):
        mapping.map_mesh(MESH, ([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]], [[0, 1, 2]]))


def test_meshing_wrappers_check_native_result_shapes_and_cardinalities(monkeypatch):
    meshing = _load(
        monkeypatch,
        "meshing",
        trimesh_remesh_along_isoline=lambda *args: (np.zeros((4, 3)), np.zeros((2, 3), dtype=np.int32), np.zeros(1, dtype=np.int32)),
        trimesh_remesh_along_isolines=lambda *args: (
            np.zeros((4, 3)),
            np.zeros((2, 3), dtype=np.int32),
            np.zeros(3),
            np.zeros(2, dtype=np.int32),
        ),
        trimesh_cut_mesh=lambda *args: (np.zeros((4, 2)), np.zeros((2, 3), dtype=np.int32)),
        trimesh_face_components=lambda *args: np.zeros(1, dtype=np.int32),
    )

    with pytest.raises(RuntimeError, match="face labels result"):
        meshing.trimesh_remesh_along_isoline(MESH, [0.0, 1.0, 1.0, 0.0], 0.5)
    with pytest.raises(RuntimeError, match="scalar values result"):
        meshing.trimesh_remesh_along_isolines(MESH, [0.0, 1.0, 1.0, 0.0], [0.5])
    with pytest.raises(RuntimeError, match="cut mesh result vertices"):
        meshing.trimesh_cut_mesh(MESH, [[0, 0, 0], [0, 0, 0]])
    with pytest.raises(RuntimeError, match="face components result"):
        meshing.trimesh_face_components(MESH)


def test_simplification_checks_native_result_shapes_and_cardinalities(monkeypatch):
    simplify = _load(
        monkeypatch,
        "simplify",
        ramer_douglas_peucker=lambda *args: (
            np.zeros((2, 3)),
            np.zeros(1, dtype=np.int32),
            np.zeros((4, 3)),
        ),
    )

    with pytest.raises(RuntimeError, match="retained indices result"):
        simplify.ramer_douglas_peucker(MESH[0], 0.1)
