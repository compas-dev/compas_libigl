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

    Raises
    ------
    ValueError
        If the ray point or direction is not finite and three-dimensional, or
        if the direction is zero.
    RuntimeError
        If libigl returns a malformed hit record.

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
    hits = _intersections.intersection_ray_mesh(P, D, V, F)
    if any(len(hit) != 4 for hit in hits):
        raise RuntimeError("libigl ray intersection result should contain four values per hit.")
    return hits


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

    Raises
    ------
    ValueError
        If `rays` is empty, does not have shape `(N, 2, 3)`, contains a
        nonfinite value, or contains a zero direction.
    RuntimeError
        If libigl does not return one valid hit list per input ray.

    """
    native_rays = np.asarray(rays, dtype=np.float64)
    if not native_rays.size:
        raise ValueError("rays should not be empty.")
    if native_rays.ndim != 3 or native_rays.shape[1:] != (2, 3):
        raise ValueError("rays should have shape (N, 2, 3).")
    if not np.isfinite(native_rays).all():
        raise ValueError("rays should contain only finite values.")
    P = np.ascontiguousarray(native_rays[:, 0, :])
    D = np.ascontiguousarray(native_rays[:, 1, :])
    if np.any(np.linalg.norm(D, axis=1) == 0):
        raise ValueError("ray directions should be nonzero.")
    V, F = as_native_mesh(M, "mesh")
    hits_per_ray = _intersections.intersection_rays_mesh(P, D, V, F)
    if len(hits_per_ray) != len(native_rays):
        raise RuntimeError("libigl ray intersections result should contain one hit list per input ray.")
    if any(len(hit) != 4 for hits in hits_per_ray for hit in hits):
        raise RuntimeError("libigl ray intersections result should contain four values per hit.")
    return hits_per_ray
