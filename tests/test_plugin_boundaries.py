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


def test_implementation_signatures_and_lightweight_registration(monkeypatch):
    geodistance = _load(monkeypatch, "geodistance", trimesh_geodistance=lambda *args: np.zeros(3))
    intersections = _load(monkeypatch, "intersections", intersection_ray_mesh=lambda *args: [])
    isolines = _load(monkeypatch, "isolines", trimesh_isolines=lambda *args: ([], [], []))
    massmatrix = _load(monkeypatch, "massmatrix", trimesh_massmatrix=lambda *args: None)
    meshing = _load(monkeypatch, "meshing", trimesh_remesh_along_isoline=lambda *args: None)
    parametrisation = _load(monkeypatch, "parametrisation", harmonic=lambda *args: np.zeros((3, 2)), lscm=lambda *args: np.zeros((3, 2)))
    planarize = _load(monkeypatch, "planarize", planarize_quads=lambda *args: np.zeros((3, 3)))
    plugin_intersections = importlib.import_module("compas_libigl.plugins.intersections")
    plugin_quadmesh = importlib.import_module("compas_libigl.plugins.quadmesh")
    plugin_trimesh = importlib.import_module("compas_libigl.plugins.trimesh")

    assert tuple(inspect.signature(geodistance.trimesh_geodistance).parameters) == ("mesh", "source", "method")
    assert tuple(inspect.signature(intersections.intersection_ray_mesh).parameters) == ("ray", "mesh")
    assert tuple(inspect.signature(isolines.trimesh_isolines).parameters) == ("mesh", "scalarfield", "number_of_isolines")
    assert tuple(inspect.signature(massmatrix.trimesh_massmatrix).parameters) == ("mesh",)
    assert tuple(inspect.signature(meshing.trimesh_remesh_along_isoline).parameters) == ("mesh", "scalarfield", "scalar")
    assert tuple(inspect.signature(planarize.quadmesh_planarize).parameters) == ("M", "kmax", "maxdev")
    mapped = (
        (plugin_trimesh.trimesh_geodistance, "_trimesh_geodistance"),
        (plugin_intersections.intersection_ray_mesh, "_intersection_ray_mesh"),
        (plugin_trimesh.trimesh_isolines, "_trimesh_isolines"),
        (plugin_trimesh.trimesh_massmatrix, "_trimesh_massmatrix"),
        (plugin_trimesh.trimesh_remesh_along_isoline, "_trimesh_remesh_along_isoline"),
        (plugin_trimesh.trimesh_harmonic, "_trimesh_harmonic"),
        (plugin_trimesh.trimesh_lscm, "_trimesh_lscm"),
        (plugin_quadmesh.quadmesh_planarize, "quadmesh_planarize"),
    )
    assert all(function.__plugin_spec__.extension_point.name == name for function, name in mapped)
    signature_pairs = (
        (plugin_trimesh.trimesh_geodistance, geodistance.trimesh_geodistance),
        (plugin_intersections.intersection_ray_mesh, intersections.intersection_ray_mesh),
        (plugin_trimesh.trimesh_isolines, isolines.trimesh_isolines),
        (plugin_trimesh.trimesh_massmatrix, massmatrix.trimesh_massmatrix),
        (plugin_trimesh.trimesh_remesh_along_isoline, meshing.trimesh_remesh_along_isoline),
        (plugin_trimesh.trimesh_harmonic, parametrisation.trimesh_harmonic),
        (plugin_trimesh.trimesh_lscm, parametrisation.trimesh_lscm),
        (plugin_quadmesh.quadmesh_planarize, planarize.quadmesh_planarize),
    )
    assert all(inspect.signature(wrapper).parameters == inspect.signature(implementation).parameters for wrapper, implementation in signature_pairs)
    assert not hasattr(geodistance.trimesh_geodistance, "__plugin_spec__")
    assert not hasattr(intersections.intersection_ray_mesh, "__plugin_spec__")
    assert not hasattr(isolines.trimesh_isolines, "__plugin_spec__")
    assert not hasattr(massmatrix.trimesh_massmatrix, "__plugin_spec__")
    assert not hasattr(meshing.trimesh_remesh_along_isoline, "__plugin_spec__")
    assert not hasattr(parametrisation.trimesh_harmonic, "__plugin_spec__")
    assert not hasattr(parametrisation.trimesh_lscm, "__plugin_spec__")
    assert not hasattr(planarize.quadmesh_planarize, "__plugin_spec__")
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
        geodistance.trimesh_geodistance(open_tessellation.to_vertices_and_triangles(), source)


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
        intersections.intersection_ray_mesh(ray, open_tessellation.to_vertices_and_triangles())


@pytest.mark.parametrize("values", [[], [0, 1, 2], [[0, 1, 2, 3]], [0, 1, 2, np.nan]])
def test_scalarfield_validation(monkeypatch, open_tessellation, values):
    isolines = _load(monkeypatch, "isolines", trimesh_isolines=lambda *args: pytest.fail("native called"))

    with pytest.raises(ValueError):
        isolines.trimesh_isolines(open_tessellation.to_vertices_and_triangles(), values, 1)


def test_results_are_normalized(monkeypatch, open_tessellation):
    geodistance = _load(monkeypatch, "geodistance", trimesh_geodistance=lambda *args: np.arange(4, dtype=float))
    isolines = _load(
        monkeypatch,
        "isolines",
        trimesh_isolines=lambda *args: (np.array([[0.0, 0.0, 0.0]]), np.array([[0, 0]]), np.array([0])),
    )

    meshdata = open_tessellation.to_vertices_and_triangles()
    assert geodistance.trimesh_geodistance(meshdata, 0) == [0.0, 1.0, 2.0, 3.0]
    assert isolines.trimesh_isolines(meshdata, [0, 1, 2, 3], 1) == ([[0.0, 0.0, 0.0]], [[0, 0]])


@pytest.mark.parametrize(
    ("module_name", "native_name", "native_result", "message"),
    [
        ("geodistance", "trimesh_geodistance", np.zeros((4, 1)), "geodistance result"),
        ("massmatrix", "trimesh_massmatrix", np.zeros((3, 3)), "mass matrix result"),
    ],
)
def test_vector_operations_reject_invalid_native_result_shape(monkeypatch, open_tessellation, module_name, native_name, native_result, message):
    module = _load(monkeypatch, module_name, **{native_name: lambda *args: native_result})
    meshdata = open_tessellation.to_vertices_and_triangles()

    with pytest.raises(RuntimeError, match=message):
        if module_name == "geodistance":
            module.trimesh_geodistance(meshdata, 0)
        else:
            module.trimesh_massmatrix(meshdata)


@pytest.mark.parametrize(
    "native_result",
    [
        (np.zeros((1, 2)), np.zeros((1, 2), dtype=np.int32), np.zeros(1)),
        (np.zeros((1, 3)), np.zeros((1, 3), dtype=np.int32), np.zeros(1)),
    ],
)
def test_isolines_reject_invalid_native_result_shape(monkeypatch, open_tessellation, native_result):
    isolines = _load(monkeypatch, "isolines", trimesh_isolines=lambda *args: native_result)

    with pytest.raises(RuntimeError, match="libigl isolines result"):
        isolines.trimesh_isolines(open_tessellation.to_vertices_and_triangles(), [0, 1, 2, 3], 1)


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


def test_parametrisation_uses_raw_mesh_and_checks_result_shape(monkeypatch, open_tessellation):
    parametrisation = _load(
        monkeypatch,
        "parametrisation",
        harmonic=lambda vertices, faces: np.zeros((len(vertices), 2)),
        lscm=lambda vertices, faces: np.zeros((len(vertices), 2)),
    )

    meshdata = open_tessellation.to_vertices_and_triangles()
    assert len(parametrisation.trimesh_harmonic(meshdata)) == 4

    invalid = _load(
        monkeypatch,
        "parametrisation",
        harmonic=lambda vertices, faces: np.zeros((len(vertices), 3)),
        lscm=lambda vertices, faces: np.zeros((len(vertices), 3)),
    )
    with pytest.raises(RuntimeError, match="shape"):
        invalid.trimesh_lscm(meshdata)
