import numpy as np
from compas.geometry import Tessellation
from compas.plugins import plugin

from compas_libigl import _intersections
from compas_libigl._tessellation import as_libigl_tessellation


@plugin(category="intersections")
def intersection_ray_mesh(ray, mesh: Tessellation) -> list[tuple[int, float, float, float]]:
    """Compute the intersection(s) between a ray and a mesh.

    Parameters
    ----------
    ray : tuple[list[float], list[float]]
        A ray represented by a point and a direction vector.
    mesh
        The triangle tessellation.

    Returns
    -------
    list[tuple[int, float, float, float]]
        The array contains a tuple per intersection of the ray with the mesh.
        Each tuple contains:

        0. the index of the intersected face
        1. the u coordinate of the intersection in the barycentric coordinates of the face
        2. the u coordinate of the intersection in the barycentric coordinates of the face
        3. the distance between the ray origin and the hit
    """
    point, vector = ray
    P = np.asarray(point, dtype=np.float64)
    D = np.asarray(vector, dtype=np.float64)
    if P.shape != (3,) or D.shape != (3,):
        raise ValueError("ray point and direction should be three-dimensional.")
    if not np.all(np.isfinite(P)) or not np.all(np.isfinite(D)):
        raise ValueError("ray point and direction should contain only finite values.")
    if np.linalg.norm(D) == 0:
        raise ValueError("ray direction should be nonzero.")
    V, F = as_libigl_tessellation(mesh)
    return _intersections.intersection_ray_mesh(P, D, V, F)


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
        2. the u coordinate of the intersection in the barycentric coordinates of the face
        3. the distance between the ray origin and the hit
    """
    points, vectors = zip(*rays)
    vertices, faces = M
    P = np.asarray(points, dtype=np.float64)
    D = np.asarray(vectors, dtype=np.float64)
    V = np.asarray(vertices, dtype=np.float64)
    F = np.asarray(faces, dtype=np.int32)
    return _intersections.intersection_rays_mesh(P, D, V, F)
