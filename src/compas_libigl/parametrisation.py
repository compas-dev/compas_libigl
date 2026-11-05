from __future__ import annotations

from typing import TYPE_CHECKING

from compas.plugins import plugin

from compas_libigl import _parametrisation  # type: ignore
from compas_libigl._mesh import as_native_mesh
from compas_libigl._mesh import validate_native_uv

if TYPE_CHECKING:
    from compas._typing import TriangleMeshInput


@plugin(category="trimesh", pluggable_name="_trimesh_harmonic")
def trimesh_harmonic(mesh: TriangleMeshInput) -> list[list[float]]:
    """Compute the harmonic parametrisation of a triangle mesh within a fixed circular boundary.

    Parameters
    ----------
    mesh
        Structural vertex and triangle buffers.

    Returns
    -------
    list[list[float]]
        The u, v parameters per vertex.

    """
    V, F = as_native_mesh(mesh, "mesh")
    uv = _parametrisation.harmonic(V, F)
    return validate_native_uv(uv, len(V), "harmonic parametrisation").tolist()


@plugin(category="trimesh", pluggable_name="_trimesh_lscm")
def trimesh_lscm(mesh: TriangleMeshInput) -> list[list[float]]:
    """Compute the least squares conformal map of a triangle mesh.

    Parameters
    ----------
    mesh
        Structural vertex and triangle buffers.

    Returns
    -------
    list[list[float]]
        The u, v parameters per vertex.

    """
    V, F = as_native_mesh(mesh, "mesh")
    uv = _parametrisation.lscm(V, F)
    return validate_native_uv(uv, len(V), "LSCM parametrisation").tolist()
