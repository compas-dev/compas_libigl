import numpy as np
from compas.plugins import plugin

from compas_libigl import _grad


@plugin(category="trimesh")
def trimesh_grad(M):
    """Compute the gradient operator for a triangle mesh.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    scipy.sparse.csc_matrix
        The gradient operator as a sparse matrix of size (3*F, V).
        When multiplied by a scalar field on vertices, produces gradient
        vectors per face (stacked as Gx, Gy, Gz).
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _grad.trimesh_grad(V, F)
