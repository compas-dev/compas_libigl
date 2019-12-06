from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

if not compas.IPY:
    from .geodistance import *


def trimesh_geodistance_exact_proxy(mesh, key):
    import numpy as np
    vertices, faces = mesh.to_vertices_and_faces()
    V = np.array(vertices, dtype=np.float64)
    F = np.array(faces, dtype=np.int32)
    D = trimesh_geodistance_exact(V, F, key)
    return D.tolist()


def trimesh_geodistance_heat_proxy(mesh, key):
    import numpy as np
    vertices, faces = mesh.to_vertices_and_faces()
    V = np.array(vertices, dtype=np.float64)
    F = np.array(faces, dtype=np.int32)
    D = trimesh_geodistance_heat(V, F, key)
    return D.tolist()


__all__ = [_ for _ in dir() if not _.startswith('_')]
