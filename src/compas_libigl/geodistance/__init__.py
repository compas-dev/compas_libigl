from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_geodistance import trimesh_geodistance_exact as _exact
from compas_libigl_geodistance import trimesh_geodistance_heat as _heat


def trimesh_geodistance(M, source, method='exact'):
    """Compute the geodesic distance from every vertex of the mesh to a root vertex.

    Parameters
    ----------
    M : tuple
        A triangle mesh represented by a tuple of vertices and faces.
    source : int
        The index of the vertex from where the geodesic distances should be calculated.
    method : {'exact', 'heat'}
        The method for calculating the distances.
        Default is `'exact'`.

    Returns
    -------
    D : list
        A list of geodesic distances from the source vertex.

    Notes
    -----
    You have to make sure the mesh is a triangle mesh.
    No checking is performed by the method.

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    if method == 'exact':
        D = _exact(V, F, source)
    elif method == 'heat':
        D = _heat(V, F, source)
    else:
        raise NotImplementedError
    return D


__all__ = [_ for _ in dir() if not _.startswith('_')]
