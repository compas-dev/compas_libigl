from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import compas
import numpy

from .triangulation import triangulate_points


def delaunay_triangulation(V):
    V = numpy.asarray(V, dtype=numpy.float64)
    E = numpy.array([], dtype=numpy.int32)
    H = numpy.array([], dtype=numpy.float64)

    tri = triangulate_points(V[:,:2], E, H, 'c')
    return tri.vertices, tri.faces


def constrained_delaunay_triangulation(V, E, H=None, area=None):
    V = numpy.asarray(V, dtype=numpy.float64)
    E = numpy.asarray(E, dtype=numpy.int32)

    if H is None:
        H = numpy.array([], dtype=numpy.float64)
    else:
        H = numpy.asarray(H, dtype=numpy.float64)
        H = H[:,:2]

    if area:
        opts = 'pa{}q'.format(area)
    else:
        opts = 'pq'

    tri = triangulate_points(V[:,:2], E, H, opts)
    return tri.vertices, tri.faces


def conforming_delaunay_triangulation(V, E, H=None, area=None):
    V = numpy.asarray(V, dtype=numpy.float64)
    E = numpy.asarray(E, dtype=numpy.int32)

    if H is None:
        H = numpy.array([], dtype=numpy.float64)
    else:
        H = numpy.asarray(H, dtype=numpy.float64)
        H = H[:,:2]

    if area:
        opts = 'pa{}q0D'.format(area)
    else:
        opts = 'pq0D'

    tri = triangulate_points(V[:,:2], E, H, opts)
    return tri.vertices, tri.faces


__all__ = [_ for _ in dir() if not _.startswith('_')]
