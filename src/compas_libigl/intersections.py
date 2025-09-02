import numpy as np
from compas.plugins import plugin

from compas_libigl import _intersections


def _conversion_libigl_to_compas(hits_per_ray):
    """Convert libigl barycentric coordinates to COMPAS barycentric coordinates.

    Parameters
    ----------
    hits_per_ray : list[tuple[int, float, float, float]]
        Tuples of (face_index, u, v, distance) from libigl ray intersection

    Returns
    -------
    list[tuple[int, float, float, float]]
        Tuples of (face_index, w, u, v) in COMPAS barycentric coordinate ordering

    Note
    ----
    libigl uses: P = (1-u-v)*v0 + u*v1 + v*v2
    This function returns [w, u, v] = [1-u-v, u, v] to match COMPAS ordering
    """

    hits_compas = []
    for h in hits_per_ray:
        idx, u, v, _ = h
        w = 1.0 - u - v
        hits_compas.append([idx, w, v, u])
    return hits_compas


def barycenter_to_point(u, v, w, p1, p2, p3):
    """Convert COMPAS barycentric coordinates to a point.

    Parameters
    ----------
    u : float
        The u coordinate
    v : float
        The v coordinate
    w : float
        The w coordinate
    p1 : tuple[float, float, float]
        The first point
    p2 : tuple[float, float, float]
        The second point
    p3 : tuple[float, float, float]
        The third point


    Returns
    -------
    list[float]
        The point at the intersection of the ray and the mesh

    Note
    ----
    libigl uses: P = (1-u-v)*v0 + u*v1 + v*v2
    This function returns [w, u, v] = [1-u-v, u, v] to match COMPAS ordering
    """
    w = 1 - u - v  # barycentric coordinates

    phit = [u * p1[0] + v * p2[0] + w * p3[0], u * p1[1] + v * p2[1] + w * p3[1], u * p1[2] + v * p2[2] + w * p3[2]]

    return phit


@plugin(category="intersections")
def intersection_ray_mesh(ray, M):
    """Compute the intersection(s) between a ray and a mesh.

    Parameters
    ----------
    ray : tuple[list[float], list[float]]
        A ray represented by a point and a direction vector.
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    list[tuple[int, float, float, float]]
        The array contains a tuple per intersection of the ray with the mesh.
        Each tuple contains:

        0. the index of the intersected face
        1. the u coordinate of the intersection in the barycentric coordinates of the face
        2. the v coordinate of the intersection in the barycentric coordinates of the face
        3. the distance between the ray origin and the hit

        Note
        ----
        The barycentric coordinates (u, v) follow the libigl convention where:
        - For a triangle with vertices (v0, v1, v2) at face indices F[face_id]
        - The intersection point P = (1-u-v)*v0 + u*v1 + v*v2
        - This differs from COMPAS barycentric_coordinates which uses a different vertex ordering
    """
    point, vector = ray
    vertices, faces = M
    P = np.asarray(point, dtype=np.float64)
    D = np.asarray(vector, dtype=np.float64)
    V = np.asarray(vertices, dtype=np.float64)
    F = np.asarray(faces, dtype=np.int32)

    hits_per_ray = _intersections.intersection_ray_mesh(P, D, V, F)

    # Convert libigl barycentric coordinates to COMPAS convention
    hits_compas = _conversion_libigl_to_compas(hits_per_ray)

    return hits_compas


def intersection_rays_mesh(rays, M):
    """Compute the intersection(s) between multiple rays and a mesh.

    Parameters
    ----------
    rays : list[tuple[list[float], list[float]]]
        List of rays, each represented by a point and a direction vector.
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    list[list[tuple[int, float, float, float]]]
        List of intersection results, one per ray.
        Each intersection result contains tuples with:

        0. the index of the intersected face
        1. the u coordinate of the intersection in the barycentric coordinates of the face
        2. the v coordinate of the intersection in the barycentric coordinates of the face
        3. the distance between the ray origin and the hit
    """
    points, vectors = zip(*rays)
    vertices, faces = M
    P = np.asarray(points, dtype=np.float64)
    D = np.asarray(vectors, dtype=np.float64)
    V = np.asarray(vertices, dtype=np.float64)
    F = np.asarray(faces, dtype=np.int32)

    hits_per_ray = _intersections.intersection_rays_mesh(P, D, V, F)

    # Convert libigl barycentric coordinates to COMPAS convention
    hits_per_ray_compas = []
    for hit in hits_per_ray:
        hits_per_ray_compas.append(_conversion_libigl_to_compas(hit))

    return hits_per_ray_compas
