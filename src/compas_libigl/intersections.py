from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from compas.typing import NumericArray
from compas.typing import RayData
from compas.typing import RayMeshHit
from compas.typing import VerticesFaces

from compas_libigl._mesh import as_native_mesh

from . import _intersections

__all__ = ["intersection_ray_mesh", "intersection_rays_mesh"]


def intersection_ray_mesh(ray: RayData, mesh: VerticesFaces) -> list[RayMeshHit]:
    """Compute the intersection(s) between a ray and a mesh.

    Parameters
    ----------
    ray
        A ray represented by a point and a direction vector.
    mesh
        Structural vertex and triangle buffers.

    Returns
    -------
    list[tuple[int, float, float, float]]
        A tuple per intersection of the ray with the mesh. Each tuple contains:

        0. the index of the intersected face
        1. the u coordinate of the intersection in the barycentric coordinates of the face
        2. the v coordinate of the intersection in the barycentric coordinates of the face
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
    V, F = as_native_mesh(mesh, "mesh")
    return _intersections.intersection_ray_mesh(P, D, V, F)


def intersection_rays_mesh(rays: Sequence[RayData] | NumericArray, M: VerticesFaces) -> list[list[RayMeshHit]]:
    """Compute the intersection(s) between multiple rays and a mesh.

    Parameters
    ----------
    rays
        Rays represented by structural `(point, direction)` pairs or a numeric
        array of shape `(N, 2, 3)`.
    M
        Structural vertex and triangle buffers.

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
    P = np.asarray(points, dtype=np.float64)
    D = np.asarray(vectors, dtype=np.float64)
    V, F = as_native_mesh(M, "mesh")
    return _intersections.intersection_rays_mesh(P, D, V, F)
