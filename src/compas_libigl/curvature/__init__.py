from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_curvature import trimesh_curvature as _trimesh_curvature


def trimesh_curvature(M):
    """Compute the gaussian curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    array
        The curvature per vertex.

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    curvature = _trimesh_curvature(V, F)
    return curvature


__all__ = [_ for _ in dir() if not _.startswith('_')]
