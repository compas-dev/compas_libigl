from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from itertools import groupby
from compas_libigl_isolines import trimesh_isolines as _trimesh_isolines


def trimesh_isolines(M, S, N=50):
    """Compute isolines on a triangle mesh using a scalarfield of data points
    assigned to its vertices.

    Parameters
    ----------
    M : tuple or :class:`compas.datastructures.Mesh`
        A mesh represented by a list of vertices and a list of faces
        or by a COMPAS mesh object.
    S : list
        A list of scalars.
    N : int, optional
        The number of isolines.
        Default is ``50``.

    Returns
    -------
    tuple
        0. The coordinates of the polyline segments representing the isolines.
        1. The segments of the polylines.

    Examples
    --------
    >>> import compas_libigl as igl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(igl.get('tubemesh.off'))
    >>> mesh.quads_to_triangles()
    >>> scalars = mesh.vertices_attribute('z')
    >>> vertices, edges = igl.trimesh_isolines(mesh, scalars, 50)

    To convert the vertices and edges to sets of isolines, use :func:`groupsort_isolines`

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    S = np.asarray(S, dtype=np.float64)
    # return the isolines as a tuple
    # not a struct
    iso = _trimesh_isolines(V, F, S, N)
    return iso.vertices, iso.edges


def groupsort_isolines(vertices, edges):
    """Group isolines edges per value level and sort edges into paths.

    Parameters
    ----------
    vertices : list
        Isoline vertices.
    edges : list
        Isoline vertex pairs.

    Returns
    -------
    list
        Every item in the list is a tuple
        containing a level value and level edges
        sorted into continuous paths.

    Examples
    --------
    >>>
    """
    levels = groupby(sorted(edges, key=lambda edge: vertices[edge[0]][2]), key=lambda edge: round(vertices[edge[0]][2], 3))
    isolines = []
    for value, edges in levels:
        paths = []
        edges = [edge.tolist() for edge in edges]
        edge = edges.pop()
        paths.append([edge])
        while edges:
            for edge in edges:
                found = False
                for path in paths:
                    a = path[0][0]
                    z = path[-1][1]
                    u, v = edge
                    if u == z:
                        path.append([u, v])
                        edges.remove(edge)
                        found = True
                        break
                    if v == z:
                        path.append([v, u])
                        edges.remove(edge)
                        found = True
                        break
                    if v == a:
                        path.insert(0, [u, v])
                        edges.remove(edge)
                        found = True
                        break
                    if u == a:
                        path.insert(0, [v, u])
                        edges.remove(edge)
                        found = True
                        break
                if not found:
                    paths.append([edge])
                    edges.remove(edge)
        isolines.append((value, paths))
    return isolines


__all__ = [_ for _ in dir() if not _.startswith('_')]
