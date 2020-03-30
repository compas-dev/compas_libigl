from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from .triangulation import triangulate_points


def delaunay_triangulation(V):
    V = np.asarray(V, dtype=np.float64)
    E = np.array([], dtype=np.int32)
    H = np.array([], dtype=np.float64)
    tri = triangulate_points(V[:,:2], E, H, 'c')
    return tri.vertices, tri.faces


def constrained_delaunay_triangulation(V, E, H=None, area=None):
    V = np.asarray(V, dtype=np.float64)
    E = np.asarray(E, dtype=np.int32)
    if H is None:
        H = np.array([], dtype=np.float64)
    else:
        H = np.asarray(H, dtype=np.float64)
        H = H[:,:2]
    if area:
        opts = 'pa{}q'.format(area)
    else:
        opts = 'pq'
    tri = triangulate_points(V[:,:2], E, H, opts)
    return tri.vertices, tri.faces


def conforming_delaunay_triangulation(V, E, H=None, area=None):
    V = np.asarray(V, dtype=np.float64)
    E = np.asarray(E, dtype=np.int32)
    if H is None:
        H = np.array([], dtype=np.float64)
    else:
        H = np.asarray(H, dtype=np.float64)
        H = H[:,:2]
    if area:
        opts = 'pa{}q0D'.format(area)
    else:
        opts = 'pq0D'
    tri = triangulate_points(V[:,:2], E, H, opts)
    return tri.vertices, tri.faces


__all__ = [_ for _ in dir() if not _.startswith('_')]
