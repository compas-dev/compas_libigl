from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

try:
from compas_libigl_booleans import mesh_union as _mesh_union
from compas_libigl_booleans import mesh_difference as _mesh_difference
from compas_libigl_booleans import mesh_symmetric_difference as _mesh_symmetric_difference
from compas_libigl_booleans import mesh_intersection as _mesh_intersection
except:
    pass

def mesh_union(A, B):
    """Compute the union of two meshes.

    Parameters
    ----------
    A : tuple
        The first mesh, represented by a tuple of a list of vertices,
        and a list of faces.
    B : tuple
        The second mesh, represented by a tuple of a list of vertices,
        and a list of faces.

    Returns
    -------
    C : tuple
        A list of vertices, and a list of faces, representing the union.
    """
    VA, FA = A
    VB, FB = B
    VA = np.asarray(VA, dtype=np.float64)
    FA = np.asarray(FA, dtype=np.int32)
    VB = np.asarray(VB, dtype=np.float64)
    FB = np.asarray(FB, dtype=np.int32)
    result = _mesh_union(VA, FA, VB, FB)
    return result.vertices, result.faces


def mesh_difference(A, B):
    """Compute the difference of two meshes.

    Parameters
    ----------
    A : tuple
        The first mesh, represented by a tuple of a list of vertices,
        and a list of faces.
    B : tuple
        The second mesh, represented by a tuple of a list of vertices,
        and a list of faces.

    Returns
    -------
    C : tuple
        A list of vertices, and a list of faces, representing the difference.
    """
    VA, FA = A
    VB, FB = B
    VA = np.asarray(VA, dtype=np.float64)
    FA = np.asarray(FA, dtype=np.int32)
    VB = np.asarray(VB, dtype=np.float64)
    FB = np.asarray(FB, dtype=np.int32)
    result = _mesh_difference(VA, FA, VB, FB)
    return result.vertices, result.faces


def mesh_symmetric_difference(A, B):
    """Compute the symmetric difference of two meshes.

    Parameters
    ----------
    A : tuple
        The first mesh, represented by a tuple of a list of vertices,
        and a list of faces.
    B : tuple
        The second mesh, represented by a tuple of a list of vertices,
        and a list of faces.

    Returns
    -------
    C : tuple
        A list of vertices, and a list of faces, representing the symmetric difference.
    """
    VA, FA = A
    VB, FB = B
    VA = np.asarray(VA, dtype=np.float64)
    FA = np.asarray(FA, dtype=np.int32)
    VB = np.asarray(VB, dtype=np.float64)
    FB = np.asarray(FB, dtype=np.int32)
    result = _mesh_symmetric_difference(VA, FA, VB, FB)
    return result.vertices, result.faces


def mesh_intersection(A, B):
    """Compute the intersection of two meshes.

    Parameters
    ----------
    A : tuple
        The first mesh, represented by a tuple of a list of vertices,
        and a list of faces.
    B : tuple
        The second mesh, represented by a tuple of a list of vertices,
        and a list of faces.

    Returns
    -------
    C : tuple
        A list of vertices, and a list of faces, representing the intersection.
    """
    VA, FA = A
    VB, FB = B
    VA = np.asarray(VA, dtype=np.float64)
    FA = np.asarray(FA, dtype=np.int32)
    VB = np.asarray(VB, dtype=np.float64)
    FB = np.asarray(FB, dtype=np.int32)
    result = _mesh_intersection(VA, FA, VB, FB)
    return result.vertices, result.faces


__all__ = [name for name in dir() if not name.startswith('_')]
