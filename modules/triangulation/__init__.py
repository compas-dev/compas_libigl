from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import compas
from compas.utilities import pairwise


if not compas.IPY:
    from .triangulation import triangulate_polygon

else:
    def triangulate_polygon(polygon):
        import numpy as np
        V = np.array(polygon, dtype=np.float64)
        E = np.array(list(pairwise(polygon + polygon[:1])), dtype=np.int32)
        tri = triangulate_polygon(V, E)
        V2 = tri.vertices
        F2 = tri.faces
        mesh = Mesh.from_vertices_and_faces(V2, F2)


__all__ = [_ for _ in dir() if not _.startswith('_')]
