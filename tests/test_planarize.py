from copy import deepcopy
import compas
import numpy as np
import pytest
from compas.datastructures import Mesh
import compas_libigl.planarize as planarize_module
from compas_libigl.planarize import quadmesh_planarize


def test_quadmesh_planarize():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    M = mesh.to_vertices_and_faces()
    new_vertices = quadmesh_planarize(M, kmax=10, maxdev=0.01)
    assert len(new_vertices) == mesh.number_of_vertices()


@pytest.mark.parametrize(
    "mesh",
    [
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            [[0, 1, 2]],
        ],
        (
            ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
            ((0, 1, 2),),
        ),
        (
            np.asarray([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], dtype=np.float32),
            np.asarray([[0, 1, 2]], dtype=np.int64),
        ),
    ],
)
def test_quadmesh_planarize_accepts_sequences_without_mutation(mesh):
    mesh_before = deepcopy(mesh)

    result = quadmesh_planarize(mesh, kmax=1)

    assert isinstance(result, list)
    np.testing.assert_array_equal(mesh[0], mesh_before[0])
    np.testing.assert_array_equal(mesh[1], mesh_before[1])


@pytest.mark.parametrize("face", [[0, 1], [0, 1, 2, 3, 4]])
def test_quadmesh_planarize_rejects_invalid_faces_without_mutation(face):
    mesh = ([[0.0, 0.0, 0.0]] * len(face), [face])
    mesh_before = deepcopy(mesh)

    with pytest.raises(ValueError, match="triangles or quads"):
        quadmesh_planarize(mesh)

    assert mesh == mesh_before


def test_quadmesh_planarize_normalizes_native_arrays(monkeypatch):
    captured = {}

    def planarize_quads(vertices, faces, kmax, maxdev):
        captured.update(vertices=vertices, faces=faces, kmax=kmax, maxdev=maxdev)
        return vertices.copy()

    monkeypatch.setattr(planarize_module._planarize, "planarize_quads", planarize_quads)
    vertices = np.asfortranarray([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]])
    faces = np.asarray([[0, 1, 2, 3, 99]], dtype=np.int64)[:, :4]

    result = quadmesh_planarize((vertices, faces), kmax=2, maxdev=0.01)

    assert captured["vertices"].dtype == np.float64
    assert captured["faces"].dtype == np.int32
    assert captured["vertices"].flags.c_contiguous
    assert captured["faces"].flags.c_contiguous
    assert captured["faces"].shape == (1, 4)
    assert captured["kmax"] == 2
    assert captured["maxdev"] == 0.01
    assert result == vertices.tolist()


@pytest.mark.parametrize(
    ("vertices", "faces", "error", "message"),
    [
        ([[0.0, 0.0]], [[0, 0, 0]], ValueError, "vertices should have shape"),
        ([[0.0, 0.0, np.nan]], [[0, 0, 0]], ValueError, "vertices should be finite"),
        ([[0.0, 0.0, 0.0]], [[-1, 0, 0]], IndexError, "index is out of range"),
        ([[0.0, 0.0, 0.0]], [[0, 0, 1]], IndexError, "index is out of range"),
        ([[0.0, 0.0, 0.0]], [[0, 0, np.iinfo(np.int32).max + 1]], OverflowError, "exceed the range"),
    ],
)
def test_quadmesh_planarize_rejects_unsafe_native_inputs(vertices, faces, error, message):
    with pytest.raises(error, match=message):
        quadmesh_planarize((vertices, faces))


@pytest.mark.parametrize(
    "native_result",
    [
        [[0.0, 0.0, 0.0]],
        np.zeros((2, 3)),
        np.zeros((3, 2)),
    ],
)
def test_quadmesh_planarize_rejects_invalid_native_result(monkeypatch, native_result):
    monkeypatch.setattr(planarize_module._planarize, "planarize_quads", lambda *args: native_result)
    mesh = ([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], [[0, 1, 2]])

    with pytest.raises(RuntimeError, match=r"result should have shape \(3, 3\)"):
        quadmesh_planarize(mesh)
