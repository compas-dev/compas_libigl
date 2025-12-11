import numpy as np
from compas.plugins import plugin

from compas_libigl import _cotmatrix


@plugin(category="trimesh")
def trimesh_cotmatrix(M):
    """Compute the cotangent Laplacian matrix of a triangle mesh.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    scipy.sparse.csc_matrix
        The cotangent Laplacian matrix in sparse format.
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _cotmatrix.trimesh_cotmatrix(V, F)


@plugin(category="trimesh")
def trimesh_cotmatrix_entries(M):
    """Compute cotangent values for each edge in each triangle.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    numpy.ndarray
        A matrix of shape (F, 3) containing cotangent values per edge.
        For each face, contains cotan of angles opposite to edges (1,2), (2,0), (0,1).
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _cotmatrix.trimesh_cotmatrix_entries(V, F)
