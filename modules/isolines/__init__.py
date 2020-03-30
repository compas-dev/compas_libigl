from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from itertools import groupby

from .isolines import trimesh_isolines as _trimesh_isolines


def trimesh_isolines(vertices, faces, scalarfield, N=50):
    V = np.asarray(vertices, dtype=np.float64)
    F = np.asarray(faces, dtype=np.int32)
    S = np.asarray(scalarfield, dtype=np.float64)
    iso = _trimesh_isolines(V, F, S, N)
    vertices = iso.vertices.tolist()
    edges = iso.edges.tolist()
    levels = groupby(sorted(edges, key=lambda edge: vertices[edge[0]][2]), key=lambda edge: vertices[edge[0]][2])
    return vertices, [[scalar, list(level)] for scalar, level in levels]


__all__ = [_ for _ in dir() if not _.startswith('_')]
