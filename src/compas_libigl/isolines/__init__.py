from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import groupby
import compas

if not compas.IPY:
    from .isolines import trimesh_isolines


def trimesh_isolines_proxy(vertices, faces, scalarfield, N=50):
    import numpy as np
    from collections import namedtuple
    V = np.array(vertices, dtype=np.float64)
    F = np.array(faces, dtype=np.int32)
    S = np.array(scalarfield, dtype=np.float64)
    iso = trimesh_isolines(V, F, S, N)
    return iso.vertices, iso.edges


__all__ = [_ for _ in dir() if not _.startswith('_')]
