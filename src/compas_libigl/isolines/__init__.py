from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_isolines import trimesh_isolines as _trimesh_isolines


def trimesh_isolines(M, S, N=50):
    """Compute isolines on a triangle mesh using a scalarfield of data points
    assigned to its vertices.

    Parameters
    ----------
    M : tuple
        A mesh represented by a list of vertices and a list of faces.
    S : list
        A list of scalars.
    N : int, optional
        The number of isolines.
        Default is ``50``.

    Returns
    -------
    tuple
        0. The coordinates of the polyline segments representing the isolines.
        1. The segments of the polylines.

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    S = np.asarray(S, dtype=np.float64)
    iso = _trimesh_isolines(V, F, S, N)
    return iso.vertices, iso.edges


__all__ = [_ for _ in dir() if not _.startswith('_')]
