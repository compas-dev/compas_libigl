from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_parametrisation import trimesh_parametrisation_harmonic as _harmonic


def trimesh_harmonic_map(M):
    """Compute the harmonic parametrisation of a triangle mesh.

    Parameters
    ----------
    M : tuple
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    array
        The u, v parameters per vertex.

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    uv = _harmonic(V, F)
    return uv


__all__ = [_ for _ in dir() if not _.startswith('_')]
