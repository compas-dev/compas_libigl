from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_intersections import intersection_ray_mesh as _intersection_ray_mesh


def intersection_ray_mesh(ray, mesh):
    """Compute the intersection(s) between a ray and a mesh.

    Parameters
    ----------
    ray : tuple of point and vector
        A ray represented by a point and a direction vector.
    mesh : tuple of vertices and faces
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    array of tuple
        The array contains a tuple per intersection of the ray with the mesh.
        Each tuple contains:

        0. the index of the intersected face
        1. the u coordinate of the intersection in the barycentric coordinates of the face
        2. the u coordinate of the intersection in the barycentric coordinates of the face
        3. the distance between the ray origin and the hit

    Notes
    -----
    To compute the actual intersection point, do

    .. code-block:: python

        point = add_vectors(ray[0], scale_vector(ray[1], hit[3]))

    """
    point, vector = ray
    vertices, faces = mesh
    P = np.asarray(point, dtype=np.float64)
    D = np.asarray(vector, dtype=np.float64)
    V = np.asarray(vertices, dtype=np.float64)
    F = np.asarray(faces, dtype=np.int32)
    hits = _intersection_ray_mesh(P, D, V, F)
    return hits


__all__ = [_ for _ in dir() if not _.startswith('_')]
