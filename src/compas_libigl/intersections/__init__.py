import numpy as np
from compas_libigl_intersections import intersection_ray_mesh as _intersection_ray_mesh
from compas_libigl_intersections import (
    intersection_rays_mesh as _intersection_rays_mesh,
)
from compas.plugins import plugin


@plugin(category="intersections")
def intersection_ray_mesh(ray, M):
    """Compute the intersection(s) between a ray and a mesh.

    Parameters
    ----------
    ray : tuple of point and vector
        A ray represented by a point and a direction vector.
    M : (list, list)
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    array
        The array contains a tuple per intersection of the ray with the mesh.
        Each tuple contains:

        0. the index of the intersected face
        1. the u coordinate of the intersection in the barycentric coordinates of the face
        2. the u coordinate of the intersection in the barycentric coordinates of the face
        3. the distance between the ray origin and the hit

    Examples
    --------
    >>> import compas
    >>> import compas_libigl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(compas.get('tubemesh.off'))
    >>> mesh.quads_to_triangles()
    >>> M = mesh.to_vertices_and_faces()
    >>> centroid = mesh.centroid()
    >>> ray = [centroid[0], centroid[1], 0], [0, 0, 1.0]
    >>> hits = compas_libigl.intersection_ray_mesh(ray, M)
    >>> len(hits) == 1
    True

    To compute the actual intersection point, do

    >>> from compas.geometry import add_vectors, scale_vector
    >>> point = add_vectors(ray[0], scale_vector(ray[1], hits[0][3]))

    """
    point, vector = ray
    vertices, faces = M
    P = np.asarray(point, dtype=np.float64)
    D = np.asarray(vector, dtype=np.float64)
    V = np.asarray(vertices, dtype=np.float64)
    F = np.asarray(faces, dtype=np.int32)
    return _intersection_ray_mesh(P, D, V, F)


def intersection_rays_mesh(rays, M):
    points, vectors = zip(*rays)
    vertices, faces = M
    P = np.asarray(points, dtype=np.float64)
    D = np.asarray(vectors, dtype=np.float64)
    V = np.asarray(vertices, dtype=np.float64)
    F = np.asarray(faces, dtype=np.int32)
    return _intersection_rays_mesh(P, D, V, F)
