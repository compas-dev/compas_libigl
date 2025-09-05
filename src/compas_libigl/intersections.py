import numpy as np
from compas.geometry import Point
from compas.plugins import plugin

from compas_libigl import _intersections


def _conversion_libigl_to_compas(hits_per_ray, M):
    """Convert libigl barycentric coordinates to COMPAS barycentric coordinates.

    Parameters
    ----------
    hits_per_ray : list[tuple[int, float, float, float]]
        Tuples of (face_index, u, v, distance) from libigl ray intersection
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    list[tuple[list[float], int, float, float, float]]
        Tuples of (point, face_index, u, v, w) in COMPAS barycentric coordinate ordering

    Note
    ----
    libigl uses: P = (1-u-v)*v0 + u*v1 + v*v2
    COMPAS uses: P = u*v0 + v*v1 + w*v2 where u + v + w = 1
    This function converts libigl coordinates to match COMPAS barycentric coordinate ordering
    """
    vertices = M[0]
    faces = M[1]

    hits_compas = []
    for h in hits_per_ray:
        idx, u_libigl, v_libigl, _ = h
        w = 1.0 - u_libigl - v_libigl  # libigl's (1-u-v) coefficient
        u = u_libigl  # libigl's u coefficient  
        v = v_libigl  # libigl's v coefficient

        face = faces[idx]
        p1, p2, p3 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
        point = barycenter_to_point(u, v, w, p1, p2, p3)
        
        # To match COMPAS barycentric coordinates exactly:
        # COMPAS expects coordinates in order [p1_weight, p2_weight, p3_weight]
        # Our formula is P = w*p1 + u*p2 + v*p3, so COMPAS order should be [w, u, v]
        hits_compas.append([point, idx, u, v, w])
    return hits_compas


def barycenter_to_point(u, v, w, p1, p2, p3):
    """Convert barycentric coordinates to a point using the working interpolation formula.

    Parameters
    ----------
    u : float
        The u coordinate (weight for p2)
    v : float
        The v coordinate (weight for p3)
    w : float
        The w coordinate (weight for p1)
    p1 : tuple[float, float, float]
        The first vertex
    p2 : tuple[float, float, float]
        The second vertex
    p3 : tuple[float, float, float]
        The third vertex

    Returns
    -------
    Point
        The interpolated point

    Note
    ----
    Uses barycentric interpolation: P = w*p1 + u*p2 + v*p3
    where w + u + v = 1
    """
    phit = [w * p1[0] + u * p2[0] + v * p3[0], 
            w * p1[1] + u * p2[1] + v * p3[1], 
            w * p1[2] + u * p2[2] + v * p3[2]]

    return Point(*phit)


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
    list[tuple[list[float], int, float, float, float]]
        The array contains a tuple per intersection of the ray with the mesh.
        Each tuple contains:

        0. the point of intersection
        1. the index of the intersected face
        2. the u coordinate of the intersection in COMPAS barycentric coordinates
        3. the v coordinate of the intersection in COMPAS barycentric coordinates
        4. the w coordinate of the intersection in COMPAS barycentric coordinates
        

        Note
        ----
        The returned barycentric coordinates follow COMPAS convention where:
        - For a triangle with vertices (p1, p2, p3) at face indices F[face_id]
        - The intersection point P = u*p1 + v*p2 + w*p3 where u + v + w = 1
        - These coordinates match those returned by compas.geometry.barycentric_coordinates
    """
    point, vector = ray
    vertices, faces = M
    P = np.asarray(point, dtype=np.float64)
    D = np.asarray(vector, dtype=np.float64)
    V = np.asarray(vertices, dtype=np.float64)
    F = np.asarray(faces, dtype=np.int32)

    hits_per_ray = _intersections.intersection_ray_mesh(P, D, V, F)

    # Convert libigl barycentric coordinates to COMPAS convention
    hits_compas = _conversion_libigl_to_compas(hits_per_ray, M)

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
    list[list[tuple[list[float], int, float, float, float]]]
        List of intersection results, one per ray.
        Each intersection result contains tuples with:

        0. the point of intersection
        1. the index of the intersected face
        2. the u coordinate of the intersection in COMPAS barycentric coordinates
        3. the v coordinate of the intersection in COMPAS barycentric coordinates
        4. the w coordinate of the intersection in COMPAS barycentric coordinates
        
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
        hits_per_ray_compas.append(_conversion_libigl_to_compas(hit, M))

    return hits_per_ray_compas
