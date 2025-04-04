import numpy as np
from compas.plugins import plugin

from compas_libigl import _massmatrix


@plugin(category="trimesh")
def trimesh_massmatrix(M):
    """Compute the mass matrix of a triangle mesh.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    scipy.sparse.csc_matrix
        The mass matrix in sparse format.
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _massmatrix.trimesh_massmatrix(V, F)
