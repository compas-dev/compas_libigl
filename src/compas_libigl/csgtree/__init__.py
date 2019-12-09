from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

if not compas.IPY:
    from .csgtree import *


def mesh_csgtree_proxy(a, b, c, d, e, f):
    import numpy as np
    cls = type(a)
    VA = np.array(a.get_vertices_attributes('xyz'), dtype=np.float64)
    FA = np.array([a.face_vertices(face) for face in a.faces()], dtype=np.int32)
    VB = np.array(b.get_vertices_attributes('xyz'), dtype=np.float64)
    FB = np.array([b.face_vertices(face) for face in b.faces()], dtype=np.int32)
    VC = np.array(c.get_vertices_attributes('xyz'), dtype=np.float64)
    FC = np.array([c.face_vertices(face) for face in c.faces()], dtype=np.int32)
    VD = np.array(d.get_vertices_attributes('xyz'), dtype=np.float64)
    FD = np.array([d.face_vertices(face) for face in d.faces()], dtype=np.int32)
    VE = np.array(e.get_vertices_attributes('xyz'), dtype=np.float64)
    FE = np.array([e.face_vertices(face) for face in e.faces()], dtype=np.int32)
    result = mesh_csgtree(VA, FA, VB, FB, VC, FC, VD, FD, VE, FE)
    c = cls.from_vertices_and_faces(result.vertices, result.faces)
    return c


__all__ = [name for name in dir() if not name.startswith('_')]
