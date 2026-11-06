from __future__ import annotations

from compas.typing import VerticesFaces

from compas_libigl._mesh import as_native_mesh
from compas_libigl._mesh import validate_native_uv

from . import _parametrisation

__all__ = ["trimesh_harmonic", "trimesh_lscm"]


def trimesh_harmonic(mesh: VerticesFaces) -> list[list[float]]:
    """Compute the harmonic parametrisation of a triangle mesh within a fixed circular boundary.

    Parameters
    ----------
    mesh
        Structural vertex and triangle buffers.

    Returns
    -------
    list[list[float]]
        The u, v parameters per vertex.

    Raises
    ------
    RuntimeError
        If libigl does not return one two-dimensional parameter per mesh
        vertex.

    """
    V, F = as_native_mesh(mesh, "mesh")
    uv = _parametrisation.harmonic(V, F)
    return validate_native_uv(uv, len(V), "harmonic parametrisation").tolist()


def trimesh_lscm(mesh: VerticesFaces) -> list[list[float]]:
    """Compute the least squares conformal map of a triangle mesh.

    Parameters
    ----------
    mesh
        Structural vertex and triangle buffers.

    Returns
    -------
    list[list[float]]
        The u, v parameters per vertex.

    Raises
    ------
    RuntimeError
        If libigl does not return one two-dimensional parameter per mesh
        vertex.

    """
    V, F = as_native_mesh(mesh, "mesh")
    uv = _parametrisation.lscm(V, F)
    return validate_native_uv(uv, len(V), "LSCM parametrisation").tolist()
