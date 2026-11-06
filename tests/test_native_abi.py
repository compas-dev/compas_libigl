from __future__ import annotations

import numpy as np
import pytest
from scipy.sparse import csc_matrix

from compas_libigl import _boundaries
from compas_libigl import _cotmatrix
from compas_libigl import _curvature
from compas_libigl import _geodistance
from compas_libigl import _grad
from compas_libigl import _intersections
from compas_libigl import _isolines
from compas_libigl import _mapping
from compas_libigl import _massmatrix
from compas_libigl import _meshing
from compas_libigl import _parametrisation
from compas_libigl import _planarize
from compas_libigl import _simplify


@pytest.fixture
def native_mesh() -> tuple[np.ndarray, np.ndarray]:
    vertices = np.asarray(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
        dtype=np.float64,
    )
    faces = np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int32)
    return vertices, faces


def assert_owned_array(result: np.ndarray, dtype: np.dtype, shape: tuple[int, ...]) -> None:
    assert isinstance(result, np.ndarray)
    assert result.dtype == dtype
    assert result.shape == shape
    assert result.flags.owndata


def test_boundary_native_abi(native_mesh) -> None:
    _, faces = native_mesh
    boundaries = _boundaries.trimesh_boundaries(faces)
    assert isinstance(boundaries, list)
    assert all(isinstance(loop, list) for loop in boundaries)
    assert all(isinstance(index, int) for loop in boundaries for index in loop)


def test_sparse_operator_native_abi(native_mesh) -> None:
    vertices, faces = native_mesh
    cotmatrix = _cotmatrix.trimesh_cotmatrix(vertices, faces)
    entries = _cotmatrix.trimesh_cotmatrix_entries(vertices, faces)
    gradient = _grad.trimesh_grad(vertices, faces)
    massmatrix = _massmatrix.trimesh_massmatrix(vertices, faces)

    assert isinstance(cotmatrix, csc_matrix)
    assert cotmatrix.shape == (4, 4)
    assert_owned_array(entries, np.dtype(np.float64), (2, 3))
    assert isinstance(gradient, csc_matrix)
    assert gradient.shape == (6, 4)
    assert isinstance(massmatrix, csc_matrix)
    assert massmatrix.shape == (4, 4)


def test_curvature_native_abi(native_mesh) -> None:
    vertices, faces = native_mesh
    gaussian = _curvature.trimesh_gaussian_curvature(vertices, faces)
    assert_owned_array(gaussian, np.dtype(np.float64), (4,))

    principal = _curvature.trimesh_principal_curvature(vertices, faces)
    assert isinstance(principal, tuple)
    assert_owned_array(principal[0], np.dtype(np.float64), (4, 3))
    assert_owned_array(principal[1], np.dtype(np.float64), (4, 3))
    assert_owned_array(principal[2], np.dtype(np.float64), (4,))
    assert_owned_array(principal[3], np.dtype(np.float64), (4,))


def test_geodistance_native_abi(native_mesh) -> None:
    vertices, faces = native_mesh
    sources = np.asarray([0], dtype=np.int32)
    results = (
        _geodistance.trimesh_geodistance(vertices, faces, 0, "exact"),
        _geodistance.trimesh_geodistance_multiple(vertices, faces, sources, "exact"),
        _geodistance.trimesh_geodistance_exact(vertices, faces, 0),
        _geodistance.trimesh_geodistance_heat(vertices, faces, 0),
    )
    for result in results:
        assert_owned_array(result, np.dtype(np.float64), (4,))

    with pytest.raises(RuntimeError, match="Unknown method"):
        _geodistance.trimesh_geodistance(vertices, faces, 0, "unsupported")


def test_intersection_native_abi(native_mesh) -> None:
    vertices, faces = native_mesh
    point = np.asarray([0.5, 0.5, 1.0], dtype=np.float64)
    direction = np.asarray([0.0, 0.0, -1.0], dtype=np.float64)
    hits = _intersections.intersection_ray_mesh(point, direction, vertices, faces)
    hits_per_ray = _intersections.intersection_rays_mesh(point[None, :], direction[None, :], vertices, faces)

    assert isinstance(hits, list)
    assert all(isinstance(hit, tuple) and len(hit) == 4 for hit in hits)
    assert isinstance(hits_per_ray, list)
    assert all(isinstance(ray_hits, list) for ray_hits in hits_per_ray)


def test_isoline_native_abi(native_mesh) -> None:
    vertices, faces = native_mesh
    values = np.asarray([0.0, 1.0, 1.0, 0.0], dtype=np.float64)
    isovalues = np.asarray([0.5], dtype=np.float64)
    points, segments, labels = _isolines.trimesh_isolines(vertices, faces, values, isovalues)

    assert_owned_array(points, np.dtype(np.float64), (3, 3))
    assert_owned_array(segments, np.dtype(np.int32), (2, 2))
    assert_owned_array(labels, np.dtype(np.int32), (2,))
    assert segments.min() >= 0
    assert segments.max() < len(points)
    assert np.array_equal(labels, np.zeros(2, dtype=np.int32))


def test_mapping_native_abi(native_mesh) -> None:
    vertices, faces = native_mesh
    result = _mapping.map_mesh_with_automatic_parameterization(
        vertices,
        faces,
        vertices[:3].copy(),
        [[0, 1, 2]],
        True,
        True,
        [],
        1e-6,
    )

    mapped_vertices, mapped_faces, normals, boundary_flags, groups = result
    assert_owned_array(mapped_vertices, np.dtype(np.float64), (4, 3))
    assert isinstance(mapped_faces, list)
    assert_owned_array(normals, np.dtype(np.float64), (4, 3))
    assert isinstance(boundary_flags, list)
    assert all(isinstance(flag, bool) for flag in boundary_flags)
    assert isinstance(groups, list)
    assert all(isinstance(group, int) for group in groups)


def test_meshing_native_abi(native_mesh) -> None:
    vertices, faces = native_mesh
    values = np.asarray([0.0, 1.0, 1.0, 0.0], dtype=np.float64)
    isovalues = np.asarray([0.5], dtype=np.float64)
    cuts = np.zeros((2, 3), dtype=np.int32)

    remeshed_vertices, remeshed_faces, labels = _meshing.trimesh_remesh_along_isoline(vertices, faces, values, 0.5)
    assert_owned_array(remeshed_vertices, np.dtype(np.float64), (7, 3))
    assert_owned_array(remeshed_faces, np.dtype(np.int32), (6, 3))
    assert_owned_array(labels, np.dtype(np.int32), (6,))

    vertices2, faces2, values2, groups2 = _meshing.trimesh_remesh_along_isolines(vertices, faces, values, isovalues)
    assert_owned_array(vertices2, np.dtype(np.float64), (7, 3))
    assert_owned_array(faces2, np.dtype(np.int32), (6, 3))
    assert_owned_array(values2, np.dtype(np.float64), (7,))
    assert_owned_array(groups2, np.dtype(np.int32), (6,))

    cut_vertices, cut_faces = _meshing.trimesh_cut_mesh(vertices, faces, cuts)
    assert_owned_array(cut_vertices, np.dtype(np.float64), (4, 3))
    assert_owned_array(cut_faces, np.dtype(np.int32), (2, 3))
    assert_owned_array(_meshing.trimesh_face_components(faces), np.dtype(np.int32), (2,))


def test_parametrisation_native_abi(native_mesh) -> None:
    vertices, faces = native_mesh
    assert_owned_array(_parametrisation.harmonic(vertices, faces), np.dtype(np.float64), (4, 2))
    assert_owned_array(_parametrisation.lscm(vertices, faces), np.dtype(np.float64), (4, 2))


def test_planarization_and_simplification_native_abi(native_mesh) -> None:
    vertices, _ = native_mesh
    quads = np.asarray([[0, 1, 2, 3]], dtype=np.int32)
    assert_owned_array(_planarize.planarize_quads(vertices, quads, 1, 0.005), np.dtype(np.float64), (4, 3))

    simplified, indices, projected = _simplify.ramer_douglas_peucker(vertices, 0.1)
    assert_owned_array(simplified, np.dtype(np.float64), (4, 3))
    assert_owned_array(indices, np.dtype(np.int32), (4,))
    assert_owned_array(projected, np.dtype(np.float64), (4, 3))


def test_native_boundary_rejects_wrong_face_rank(native_mesh) -> None:
    vertices, faces = native_mesh
    with pytest.raises(TypeError):
        _cotmatrix.trimesh_cotmatrix(vertices, faces[:, 0])
