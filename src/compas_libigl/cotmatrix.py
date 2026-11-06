from __future__ import annotations

from typing import TYPE_CHECKING

from compas.typing import Float64Array
from compas.typing import VerticesFaces

from compas_libigl._mesh import as_native_mesh
from compas_libigl._mesh import validate_result_shape

from . import _cotmatrix

if TYPE_CHECKING:
    from scipy.sparse import csc_matrix

__all__ = ["trimesh_cotmatrix", "trimesh_cotmatrix_entries"]


def trimesh_cotmatrix(M: VerticesFaces) -> csc_matrix:
    """Compute the cotangent Laplacian matrix of a triangle mesh.

    Parameters
    ----------
    M
        Structural vertex and triangle buffers.

    Returns
    -------
    scipy.sparse.csc_matrix
        The cotangent Laplacian matrix in sparse format.

    Raises
    ------
    RuntimeError
        If libigl returns a matrix whose shape does not match the mesh.

    """
    V, F = as_native_mesh(M, "mesh")
    matrix = _cotmatrix.trimesh_cotmatrix(V, F)
    return validate_result_shape(matrix, (len(V), len(V)), "cotangent matrix")


def trimesh_cotmatrix_entries(M: VerticesFaces) -> Float64Array:
    """Compute cotangent values for each edge in each triangle.

    Parameters
    ----------
    M
        Structural vertex and triangle buffers.

    Returns
    -------
    numpy.ndarray
        A matrix of shape (F, 3) containing cotangent values per edge.
        For each face, contains cotan of angles opposite to edges (1,2), (2,0), (0,1).

    Raises
    ------
    RuntimeError
        If libigl does not return three cotangent values per mesh face.

    """
    V, F = as_native_mesh(M, "mesh")
    entries = _cotmatrix.trimesh_cotmatrix_entries(V, F)
    return validate_result_shape(entries, (len(F), 3), "cotangent entries")
