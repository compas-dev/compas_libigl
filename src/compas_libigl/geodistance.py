from __future__ import annotations

from numbers import Integral
from typing import TYPE_CHECKING
from typing import Literal

import numpy as np

from compas_libigl import _geodistance  # type: ignore
from compas_libigl._mesh import as_native_mesh
from compas_libigl._mesh import validate_native_vector

if TYPE_CHECKING:
    from compas._typing import TriangleMeshInput


def trimesh_geodistance(
    mesh: TriangleMeshInput,
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
    NotImplementedError
        If method is not one of {'exact', 'heat'}.

    """
    V, F = as_native_mesh(mesh, "mesh")
    if isinstance(source, bool) or not isinstance(source, Integral):
        raise TypeError("source should be an integer vertex index.")
    if source < 0 or source >= len(V):
        raise IndexError("source vertex index is out of range.")
    distances = _geodistance.trimesh_geodistance(V, F, source, method)
    return validate_native_vector(distances, len(V), "geodistance").tolist()


def trimesh_geodistance_multiple(M, sources, method="exact"):
    """Compute the geodesic distance from multiple source points.

    Calculates the minimum geodesic distance from any of the source vertices
    to all other vertices in the mesh.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles
    sources : list[int]
        The indices of the source vertices.
    method : str, optional
        The method to use for geodesic distance computation.
        Options:
        * 'exact': Use exact geodesic algorithm
        * 'heat': Use heat method (faster but approximate)
        Default is 'exact'.

    Returns
    -------
    list[float]
        The minimum geodesic distances from any source to all vertices.

    Raises
    ------
    NotImplementedError
        If method is not one of {'exact', 'heat'}.
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    sources = np.asarray(sources, dtype=np.int32)
    return _geodistance.trimesh_geodistance_multiple(V, F, sources, method)
