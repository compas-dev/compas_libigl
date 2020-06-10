from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_massmatrix import trimesh_massmatrix as _trimesh_massmatrix


def trimesh_massmatrix(M):
    """Compute massmatrix on a triangle mesh using a scalarfield of data points
    assigned to its vertices.

    Parameters
    ----------
    M : tuple
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    array
        The mass per vertex.

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    mass = _trimesh_massmatrix(V, F)
    return mass


__all__ = [_ for _ in dir() if not _.startswith('_')]
