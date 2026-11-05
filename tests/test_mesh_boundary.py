import numpy as np
import pytest

from compas_libigl._mesh import as_native_mesh


@pytest.mark.parametrize(
    "vertices",
    [
        [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
        ((0, 0, 0), (1, 0, 0), (0, 1, 0)),
        np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32),
        np.asfortranarray(np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float64)),
        np.asarray([[0, 0, 0, 9], [1, 0, 0, 9], [0, 1, 0, 9]], dtype=np.float64)[:, :3],
    ],
)
@pytest.mark.parametrize(
    "faces",
    [
        [[0, 1, 2]],
        ((0, 1, 2),),
        np.asarray([[0, 1, 2]], dtype=np.int32),
        np.asfortranarray(np.asarray([[0, 1, 2]], dtype=np.int64)),
        np.asarray([[0, 1, 2, 9]], dtype=np.int64)[:, :3],
    ],
)
def test_native_mesh_conversion_is_safe_and_nonmutating(vertices, faces):
    vertices_before = np.asarray(vertices).copy()
    faces_before = np.asarray(faces).copy()

    native_vertices, native_faces = as_native_mesh((vertices, faces), "mesh")

    assert native_vertices.dtype == np.float64
    assert native_faces.dtype == np.int32
    assert native_vertices.flags.c_contiguous
    assert native_faces.flags.c_contiguous
    np.testing.assert_array_equal(vertices, vertices_before)
    np.testing.assert_array_equal(faces, faces_before)


def test_native_mesh_conversion_accepts_readonly_buffers():
    vertices = np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float64)
    faces = np.asarray([[0, 1, 2]], dtype=np.int64)
    vertices.flags.writeable = False
    faces.flags.writeable = False

    native_vertices, native_faces = as_native_mesh((vertices, faces), "mesh")

    assert native_vertices is vertices
    assert native_faces.dtype == np.int32


@pytest.mark.parametrize(
    ("mesh", "error", "message"),
    [
        (([[0, 0]], [[0, 0, 0]]), ValueError, r"shape \(N, 3\)"),
        (([[0, 0, 0]], [[0, 0]]), ValueError, r"shape \(M, 3\)"),
        (([[0, 0, float("nan")]], [[0, 0, 0]]), ValueError, "finite"),
        (([[0, 0, 0]], [[-1, 0, 0]]), IndexError, "out of range"),
        (([[0, 0, 0]], np.asarray([[2**32, 0, 0]], dtype=np.int64)), OverflowError, "range supported"),
    ],
)
def test_native_mesh_conversion_rejects_unsafe_buffers(mesh, error, message):
    with pytest.raises(error, match=message):
        as_native_mesh(mesh, "mesh")
