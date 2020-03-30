from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from .booleans import mesh_union as _mesh_union
from .booleans import mesh_difference as _mesh_difference
from .booleans import mesh_symmetric_difference as _mesh_symmetric_difference
from .booleans import mesh_intersection as _mesh_intersection


def mesh_union(VA, FA, VB, FB):
    VA = np.asarray(VA, dtype=np.float64)
    FA = np.asarray(FA, dtype=np.int32)
    VB = np.asarray(VB, dtype=np.float64)
    FB = np.asarray(FB, dtype=np.int32)
    result = _mesh_union(VA, FA, VB, FB)
    return result.vertices, result.faces


def mesh_difference(VA, FA, VB, FB):
    VA = np.asarray(VA, dtype=np.float64)
    FA = np.asarray(FA, dtype=np.int32)
    VB = np.asarray(VB, dtype=np.float64)
    FB = np.asarray(FB, dtype=np.int32)
    result = _mesh_difference(VA, FA, VB, FB)
    return result.vertices, result.faces


def mesh_symmetric_difference(VA, FA, VB, FB):
    VA = np.asarray(VA, dtype=np.float64)
    FA = np.asarray(FA, dtype=np.int32)
    VB = np.asarray(VB, dtype=np.float64)
    FB = np.asarray(FB, dtype=np.int32)
    result = _mesh_symmetric_difference(VA, FA, VB, FB)
    return result.vertices, result.faces


def mesh_intersection(VA, FA, VB, FB):
    VA = np.asarray(VA, dtype=np.float64)
    FA = np.asarray(FA, dtype=np.int32)
    VB = np.asarray(VB, dtype=np.float64)
    FB = np.asarray(FB, dtype=np.int32)
    result = _mesh_intersection(VA, FA, VB, FB)
    return result.vertices, result.faces


__all__ = [name for name in dir() if not name.startswith('_')]
