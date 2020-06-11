from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_boundaries import trimesh_boundaries as _trimesh_boundaries


def trimesh_boundaries(M):
    """Compute the boundaries of a triangle mesh.

    Parameters
    ----------
    M : tuple
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    array
        The boundaries of the triangle mesh.

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    boundaries = _trimesh_boundaries(V, F)
    return boundaries


__all__ = [_ for _ in dir() if not _.startswith('_')]
