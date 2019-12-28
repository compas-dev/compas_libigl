from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

if not compas.IPY:
    from .booleans import *


def mesh_union_proxy(a, b):
    import numpy as np
    cls = type(a)
    VA = np.array(a.get_vertices_attributes('xyz'), dtype=np.float64)
    FA = np.array([a.face_vertices(face) for face in a.faces()], dtype=np.int32)
    VB = np.array(b.get_vertices_attributes('xyz'), dtype=np.float64)
    FB = np.array([b.face_vertices(face) for face in b.faces()], dtype=np.int32)
    result = mesh_union(VA, FA, VB, FB)
    c = cls.from_vertices_and_faces(result.vertices, result.faces)
    return c


__all__ = [name for name in dir() if not name.startswith('_')]