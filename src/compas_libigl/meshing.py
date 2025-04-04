import numpy as np
from compas.plugins import plugin

from compas_libigl import _meshing


@plugin(category="trimesh")
def trimesh_remesh_along_isoline(M, scalars, isovalue):
    """Remesh a triangle mesh along an isoline.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles
    scalars : list[float]
        A scalar value per vertex.
    isovalue : float
        The value at which to compute the isoline.

    Returns
    -------
    tuple[list[list[float]], list[list[int]], list[int]]
        A tuple containing
        * the vertices of the remeshed mesh,
        * the faces of the remeshed mesh,
        * labels for the faces of the remeshed mesh.
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    S = np.asarray(scalars, dtype=np.float64)
    ISO = np.float64(isovalue)
    V2, F2, L = _meshing.trimesh_remesh_along_isoline(V, F, S, ISO)
    return V2.tolist(), F2.tolist(), L.tolist()


@plugin(category="trimesh")
def trimesh_remesh_along_isolines(M, scalars, isovalues):
    """Remesh a triangle mesh along multiple isolines.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles
    scalars : list[float]
        A scalar value per vertex.
    isovalues : list[float]
        The values at which to compute the isolines.

    Returns
    -------
    tuple[list[list[float]], list[list[int]], list[float], list[int]]
        A tuple containing
        * the vertices of the remeshed mesh,
        * the faces of the remeshed mesh,
        * scalar values for the vertices of the remeshed mesh,
        * labels for the faces of the remeshed mesh.
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    S = np.asarray(scalars, dtype=np.float64)
    ISO = np.asarray(isovalues, dtype=np.float64)
    V2, F2, S2, G2 = _meshing.trimesh_remesh_along_isolines(V, F, S, ISO)
    return V2.tolist(), F2.tolist(), S2.tolist(), G2.tolist()
