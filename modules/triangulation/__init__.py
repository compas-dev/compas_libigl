from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import compas
from compas.utilities import pairwise


if not compas.IPY:
    from .triangulation import triangulate_points

# else:
#     def triangulate_polygon(polygon):
#         import numpy as np
#         V = np.array(polygon, dtype=np.float64)
#         E = np.array(list(pairwise(polygon + polygon[:1])), dtype=np.int32)
#         tri = triangulate_polygon(V, E)
#         V2 = tri.vertices
#         F2 = tri.faces
#         mesh = Mesh.from_vertices_and_faces(V2, F2)


def delaunay_triangulation(V):
    import numpy
    E = numpy.array([], dtype=numpy.int32)
    H = numpy.array([], dtype=numpy.float64)
    return triangulate_points(V, E, H, 'c')


def constrained_delaunay_triangulation(V, E, H=None, area=None):
    import numpy
    if H is None:
        H = numpy.array([], dtype=numpy.float64)
    if area:
        opts = 'pa{}q'.format(area)
    else:
        opts = 'pq'
    return triangulate_points(V, E, H, opts)


def conforming_delaunay_triangulation(V, E, H=None, area=None):
    import numpy
    if H is None:
        H = numpy.array([], dtype=numpy.float64)
    if area:
        opts = 'pa{}q0D'.format(area)
    else:
        opts = 'pq0D'
    return triangulate_points(V, E, H, opts)



__all__ = [_ for _ in dir() if not _.startswith('_')]
