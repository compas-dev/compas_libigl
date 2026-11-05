from __future__ import annotations

from typing import TYPE_CHECKING

from compas_libigl import _massmatrix  # type: ignore
from compas_libigl._mesh import as_native_mesh
from compas_libigl._mesh import validate_native_vector

if TYPE_CHECKING:
    from compas._typing import TriangleMeshInput


def trimesh_massmatrix(mesh: TriangleMeshInput) -> list[float]:
    """Compute the mass matrix of a triangle mesh.

    Parameters
    ----------
    mesh
        Structural vertex and triangle buffers.

    Returns
    -------
    list[float]
        The barycentric mass associated with every vertex.

    """
    V, F = as_native_mesh(mesh, "mesh")
    matrix = _massmatrix.trimesh_massmatrix(V, F)
    diagonal = matrix.diagonal()
    return validate_native_vector(diagonal, len(V), "mass matrix").tolist()
