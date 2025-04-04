import numpy as np
from compas.plugins import plugin

from compas_libigl import _parametrisation


@plugin(category="trimesh")
def trimesh_harmonic(M):
    """Compute the harmonic parametrisation of a triangle mesh within a fixed circular boundary.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    list[list[float]]
        The u, v parameters per vertex.

    Notes
    -----
    ``camelhead.off`` can be downloaded from https://raw.githubusercontent.com/libigl/libigl-tutorial-data/master/camelhead.off
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _parametrisation.harmonic(V, F)


@plugin(category="trimesh")
def trimesh_lscm(M):
    """Compute the least squares conformal map of a triangle mesh.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    list[list[float]]
        The u, v parameters per vertex.

    Notes
    -----
    ``camelhead.off`` can be downloaded from https://raw.githubusercontent.com/libigl/libigl-tutorial-data/master/camelhead.off
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _parametrisation.lscm(V, F)
