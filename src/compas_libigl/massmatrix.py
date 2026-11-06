from __future__ import annotations

from compas.typing import VerticesFaces

from compas_libigl._mesh import as_native_mesh
from compas_libigl._mesh import validate_native_vector

from . import _massmatrix

__all__ = ["trimesh_massmatrix"]


def trimesh_massmatrix(mesh: VerticesFaces) -> list[float]:
    """Compute the mass matrix of a triangle mesh.

    Parameters
    ----------
    mesh
        Structural vertex and triangle buffers.

    Returns
    -------
    list[float]
        The barycentric mass associated with every vertex.

    Raises
    ------
    RuntimeError
        If libigl does not return one mass value per mesh vertex.

    """
    V, F = as_native_mesh(mesh, "mesh")
    matrix = _massmatrix.trimesh_massmatrix(V, F)
    diagonal = matrix.diagonal()
    return validate_native_vector(diagonal, len(V), "mass matrix").tolist()
