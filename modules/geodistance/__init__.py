from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from .geodistance import trimesh_geodistance_exact as _exact
from .geodistance import trimesh_geodistance_heat as _heat


def trimesh_geodistance_exact(V, F, index):
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    D = _exact(V, F, index)
    return D


def trimesh_geodistance_heat(V, F, index):
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    D = _heat(V, F, index)
    return D


__all__ = [_ for _ in dir() if not _.startswith('_')]
