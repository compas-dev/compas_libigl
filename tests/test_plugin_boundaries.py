import importlib
import inspect
import sys
from types import ModuleType

import numpy as np
import pytest
import compas_libigl
from compas.geometry import Tessellation


def _load(monkeypatch, name, **native_functions):
    native_name = f"compas_libigl._{name}"
    native = ModuleType(native_name)
    for function_name, function in native_functions.items():
        setattr(native, function_name, function)
    monkeypatch.setitem(sys.modules, native_name, native)
    monkeypatch.setattr(compas_libigl, f"_{name}", native, raising=False)
    sys.modules.pop(f"compas_libigl.{name}", None)
    return importlib.import_module(f"compas_libigl.{name}")


@pytest.fixture
def open_tessellation():
    return Tessellation(
        [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]],
        [[0, 1, 2], [0, 2, 3]],
    )


def test_mapped_signatures_and_registration(monkeypatch):
    geodistance = _load(monkeypatch, "geodistance", trimesh_geodistance=lambda *args: np.zeros(3))
    intersections = _load(monkeypatch, "intersections", intersection_ray_mesh=lambda *args: [])
    isolines = _load(monkeypatch, "isolines", trimesh_isolines=lambda *args: ([], [], []))
    massmatrix = _load(monkeypatch, "massmatrix", trimesh_massmatrix=lambda *args: None)
    meshing = _load(monkeypatch, "meshing", trimesh_remesh_along_isoline=lambda *args: None)
    parametrisation = _load(monkeypatch, "parametrisation", harmonic=lambda *args: np.zeros((3, 2)), lscm=lambda *args: np.zeros((3, 2)))

    assert tuple(inspect.signature(geodistance.trimesh_geodistance).parameters) == ("mesh", "source", "method")
    assert tuple(inspect.signature(intersections.intersection_ray_mesh).parameters) == ("ray", "mesh")
    assert tuple(inspect.signature(isolines.trimesh_isolines).parameters) == ("mesh", "scalarfield", "number_of_isolines")
    assert tuple(inspect.signature(massmatrix.trimesh_massmatrix).parameters) == ("mesh",)
    assert tuple(inspect.signature(meshing.trimesh_remesh_along_isoline).parameters) == ("mesh", "scalarfield", "scalar")
    mapped = (
        geodistance.trimesh_geodistance,
        intersections.intersection_ray_mesh,
        isolines.trimesh_isolines,
        massmatrix.trimesh_massmatrix,
    )
    assert all(function.__plugin_spec__.extension_point.name == function.__name__ for function in mapped)
    assert meshing.trimesh_remesh_along_isoline.__plugin_spec__.extension_point.name == "_trimesh_remesh_along_isoline"
    assert parametrisation.trimesh_harmonic.__plugin_spec__.extension_point.name == "trimesh_harmonic"
    assert parametrisation.trimesh_lscm.__plugin_spec__.extension_point.name == "trimesh_lscm"
    assert not hasattr(geodistance.trimesh_geodistance_multiple, "__plugin_spec__")


def test_gaussian_curvature_is_not_registered(monkeypatch, open_tessellation):
    curvature = _load(monkeypatch, "curvature", trimesh_gaussian_curvature=lambda *args: np.arange(4), trimesh_principal_curvature=lambda *args: ())

    result = curvature.trimesh_gaussian_curvature(open_tessellation.to_vertices_and_triangles())
    assert result.tolist() == [0, 1, 2, 3]
    assert not hasattr(curvature.trimesh_gaussian_curvature, "__plugin_spec__")


@pytest.mark.parametrize("source", [True, 1.5, -1, 4])
def test_geodistance_rejects_invalid_source(monkeypatch, open_tessellation, source):
    geodistance = _load(monkeypatch, "geodistance", trimesh_geodistance=lambda *args: np.zeros(4))

    with pytest.raises((TypeError, IndexError)):
        geodistance.trimesh_geodistance(open_tessellation, source)


@pytest.mark.parametrize(
    "ray",
    [
        ([0, 0], [1, 0, 0]),
        ([0, 0, 0], [0, 0, 0]),
        ([0, 0, np.inf], [1, 0, 0]),
    ],
)
def test_ray_validation_precedes_native_call(monkeypatch, open_tessellation, ray):
    intersections = _load(monkeypatch, "intersections", intersection_ray_mesh=lambda *args: pytest.fail("native called"))

    with pytest.raises(ValueError):
        intersections.intersection_ray_mesh(ray, open_tessellation)


@pytest.mark.parametrize("values", [[], [0, 1, 2], [[0, 1, 2, 3]], [0, 1, 2, np.nan]])
def test_scalarfield_validation(monkeypatch, open_tessellation, values):
    isolines = _load(monkeypatch, "isolines", trimesh_isolines=lambda *args: pytest.fail("native called"))

    with pytest.raises(ValueError):
        isolines.trimesh_isolines(open_tessellation, values, 1)


def test_results_are_normalized(monkeypatch, open_tessellation):
    geodistance = _load(monkeypatch, "geodistance", trimesh_geodistance=lambda *args: np.arange(4, dtype=float))
    isolines = _load(
        monkeypatch,
        "isolines",
        trimesh_isolines=lambda *args: (np.array([[0.0, 0.0, 0.0]]), np.array([[0, 0]]), np.array([0])),
    )

    assert geodistance.trimesh_geodistance(open_tessellation, 0) == [0.0, 1.0, 2.0, 3.0]
    assert isolines.trimesh_isolines(open_tessellation, [0, 1, 2, 3], 1) == ([[0.0, 0.0, 0.0]], [[0, 0]])


def test_remesh_returns_raw_mesh_without_labels(monkeypatch, open_tessellation):
    native_result = (
        np.array(open_tessellation.vertices, dtype=float),
        np.array(open_tessellation.triangles, dtype=np.int32),
        np.array([0, 1]),
    )
    meshing = _load(monkeypatch, "meshing", trimesh_remesh_along_isoline=lambda *args: native_result)

    result = meshing.trimesh_remesh_along_isoline(open_tessellation.to_vertices_and_triangles(), [0, 1, 2, 3], 0.5)
    assert result[0] is native_result[0]
    assert result[1] is native_result[1]

    with pytest.raises(ValueError):
        meshing.trimesh_remesh_along_isoline(open_tessellation.to_vertices_and_triangles(), [0, 1, 2, 3], np.inf)


def test_remesh_normalizes_raw_buffers_without_mutation(monkeypatch):
    captured = {}

    def remesh(vertices, faces, scalarfield, scalar):
        captured.update(vertices=vertices, faces=faces, scalarfield=scalarfield, scalar=scalar)
        return vertices, faces, np.zeros(len(faces), dtype=np.int32)

    meshing = _load(monkeypatch, "meshing", trimesh_remesh_along_isoline=remesh)
    vertices = np.asfortranarray(np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32))
    faces = np.asarray([[0, 1, 2, 9]], dtype=np.int64)[:, :3]
    vertices.flags.writeable = False
    faces.flags.writeable = False
    vertices_before = vertices.copy()
    faces_before = faces.copy()

    result = meshing.trimesh_remesh_along_isoline((vertices, faces), [0, 1, 2], 0.5)

    assert captured["vertices"].dtype == np.float64
    assert captured["faces"].dtype == np.int32
    assert captured["vertices"].flags.c_contiguous
    assert captured["faces"].flags.c_contiguous
    assert captured["scalarfield"].dtype == np.float64
    assert result[0] is captured["vertices"]
    assert result[1] is captured["faces"]
    np.testing.assert_array_equal(vertices, vertices_before)
    np.testing.assert_array_equal(faces, faces_before)


@pytest.mark.parametrize(
    "native_result",
    [
        (np.empty((0, 2)), np.empty((0, 3), dtype=np.int32), np.empty(0, dtype=np.int32)),
        (np.empty((0, 3)), np.empty((0, 2), dtype=np.int32), np.empty(0, dtype=np.int32)),
    ],
)
def test_remesh_rejects_invalid_native_result_shape(monkeypatch, native_result):
    meshing = _load(monkeypatch, "meshing", trimesh_remesh_along_isoline=lambda *args: native_result)

    with pytest.raises(RuntimeError, match="libigl remesh-along-isoline result"):
        meshing.trimesh_remesh_along_isoline(
            ([[0, 0, 0], [1, 0, 0], [0, 1, 0]], [[0, 1, 2]]),
            [0, 1, 2],
            0.5,
        )


def test_parametrisation_topology_validation(monkeypatch, open_tessellation):
    parametrisation = _load(
        monkeypatch,
        "parametrisation",
        harmonic=lambda vertices, faces: np.zeros((len(vertices), 2)),
        lscm=lambda vertices, faces: np.zeros((len(vertices), 2)),
    )

    assert len(parametrisation.trimesh_harmonic(open_tessellation)) == 4

    closed = Tessellation(
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[0, 2, 1], [0, 1, 3], [1, 2, 3], [2, 0, 3]],
    )
    inconsistent = Tessellation(
        open_tessellation.vertices,
        [[0, 1, 2], [0, 3, 2]],
    )
    nonmanifold = Tessellation(
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1]],
        [[0, 1, 2], [1, 0, 3], [0, 1, 4]],
    )
    disconnected = Tessellation(
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [3, 0, 0], [4, 0, 0], [3, 1, 0]],
        [[0, 1, 2], [3, 4, 5]],
    )
    empty = Tessellation([], [])

    for invalid in (closed, inconsistent, nonmanifold, disconnected, empty):
        with pytest.raises(ValueError):
            parametrisation.trimesh_lscm(invalid)
