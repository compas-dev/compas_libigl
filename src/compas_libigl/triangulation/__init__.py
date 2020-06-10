from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_triangulation import triangulate_points


def delaunay_triangulation(V):
    """Compute a Delaunay Triangulation of the givem points.

    Parameters
    ----------
    V : list
        The coordinates of the input points.

    Returns
    -------
    tuple
        0. The vertices

    """
    V = np.asarray(V, dtype=np.float64)
    E = np.array([], dtype=np.int32)
    H = np.array([], dtype=np.float64)
    tri = triangulate_points(V[:,:2], E, H, 'c')
    return tri.vertices, tri.faces


def constrained_delaunay_triangulation(V, E, H=None, area=None):
    """Compute a Delaunay Triangulation of the given points, constrained to specific edges and holes.

    Parameters
    ----------
    V : list or array
        The coordinates of the points of the triangulation.
    E : list or array
        Vertex index pairs defining specific edges of the triangulation.
        These edges can lie along internal curve features, or on the boundary of holes
        in the resulting mesh.
    H : list or array, optional
        Coordinates of an internal point per hole
        (to determine what is in and what is out).
    area : float, optional
        Target area for the triangles.
        If a value is provided, additional points will be added to the triangulation
        if necessary to satisfy the target.
        Points may also be added along the constraint edges.
        If no value is provided (default),
        the triangulation is simply constrained to the given points, edges, and holes.

    Returns
    -------
    tuple
        0. The vertices of the triangulation.
        1. The faces of the triangulation.

    """
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
    """Compute a Conforming Delaunay Triangulation of the given points, constrained to specific edges and holes.

    Parameters
    ----------
    V : list or array
        The coordinates of the points of the triangulation.
    E : list or array
        Vertex index pairs defining specific edges of the triangulation.
        These edges can lie along internal curve features, or on the boundary of holes
        in the resulting mesh.
    H : list or array, optional
        Coordinates of an internal point per hole
        (to determine what is in and what is out).
    area : float, optional
        Target area for the triangles.
        If a value is provided, additional points will be added to the triangulation
        if necessary to satisfy the target.
        Points may also be added along the constraint edges.
        If no value is provided (default),
        the triangulation is simply constrained to the given points, edges, and holes.

    Returns
    -------
    tuple
        0. The vertices of the triangulation.
        1. The faces of the triangulation.

    """
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
