import numpy as np
from compas.plugins import plugin

from compas_libigl import _massmatrix


@plugin(category="trimesh")
def trimesh_massmatrix(M):
    """Compute the mass matrix of a triangle mesh.

    Parameters
    ----------
    M : tuple or :class:`compas.datastructures.Mesh`
        A mesh represented by a list of vertices and a list of faces
        or by a COMPAS mesh object.

    Returns
    -------
    array
        The mass per vertex.

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _massmatrix.trimesh_massmatrix(V, F)
