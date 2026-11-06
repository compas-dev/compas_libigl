from __future__ import annotations

from numbers import Integral
from typing import Literal

import numpy as np
from compas.typing import Float64Array
from compas.typing import IndicesLike
from compas.typing import VerticesFaces

from compas_libigl._mesh import as_native_index_vector
from compas_libigl._mesh import as_native_mesh
from compas_libigl._mesh import validate_native_vector

from . import _geodistance

__all__ = ["trimesh_geodistance", "trimesh_geodistance_multiple"]


def trimesh_geodistance(
    mesh: VerticesFaces,
    source: int,
    method: Literal["exact", "heat"] = "exact",
) -> list[float]:
    """Compute the geodesic distance from a source point to all vertices.

    Calculates the geodesic distance from a single source vertex to all other
    vertices in the mesh using either exact or heat method.

    Parameters
    ----------
    mesh
        Structural vertex and triangle buffers.
    source
        The index of the source vertex.
    method
        Geodesic algorithm. Use `"exact"` for exact geodesics or `"heat"` for
        the faster approximate heat method.

    Returns
    -------
    list[float]
        The geodesic distances from the source to all vertices.

    Raises
    ------
    RuntimeError
        If `method` is not `"exact"` or `"heat"`, or if libigl returns an
        invalid distance vector.

    """
    V, F = as_native_mesh(mesh, "mesh")
    if isinstance(source, bool) or not isinstance(source, Integral):
        raise TypeError("source should be an integer vertex index.")
    if source < 0 or source >= len(V):
        raise IndexError("source vertex index is out of range.")
    distances = _geodistance.trimesh_geodistance(V, F, source, method)
    return validate_native_vector(distances, len(V), "geodistance").tolist()


def trimesh_geodistance_multiple(
    M: VerticesFaces,
    sources: IndicesLike,
    method: Literal["exact", "heat"] = "exact",
) -> Float64Array:
    """Compute the geodesic distance from multiple source points.

    Calculates the minimum geodesic distance from any of the source vertices
    to all other vertices in the mesh.

    Parameters
    ----------
    M
        Structural vertex and triangle buffers.
    sources
        The indices of the source vertices.
    method
        The method to use for geodesic distance computation.
        Options:
        * 'exact': Use exact geodesic algorithm
        * 'heat': Use heat method (faster but approximate)
        Default is 'exact'.

    Returns
    -------
    numpy.ndarray
        The minimum geodesic distances from any source to all vertices.

    Raises
    ------
    TypeError
        If a source is not an integer index, or is a boolean.
    ValueError
        If `sources` is not a nonempty one-dimensional collection.
    IndexError
        If a source index is outside the mesh vertex range.
    RuntimeError
        If `method` is not `"exact"` or `"heat"`, or if libigl returns an
        invalid distance vector.

    """
    V, F = as_native_mesh(M, "mesh")
    source_values = np.asarray(sources, dtype=object)
    if source_values.ndim != 1:
        raise ValueError("sources should be one-dimensional.")
    source_indices = as_native_index_vector(source_values, "sources")
    if not source_indices:
        raise ValueError("sources should not be empty.")
    if min(source_indices) < 0 or max(source_indices) >= len(V):
        raise IndexError("source vertex index is out of range.")
    native_sources = np.ascontiguousarray(source_indices, dtype=np.int32)
    distances = _geodistance.trimesh_geodistance_multiple(V, F, native_sources, method)
    return validate_native_vector(distances, len(V), "geodistance-multiple")
