from __future__ import annotations

from typing import TYPE_CHECKING

from compas.typing import VerticesFaces

from compas_libigl._mesh import as_native_mesh

from . import _grad

if TYPE_CHECKING:
    from scipy.sparse import csc_matrix

__all__ = ["trimesh_grad"]


def trimesh_grad(M: VerticesFaces) -> csc_matrix:
    """Compute the gradient operator for a triangle mesh.

    Parameters
    ----------
    M
        Structural vertex and triangle buffers.

    Returns
    -------
    scipy.sparse.csc_matrix
        The gradient operator as a sparse matrix of size (3*F, V).
        When multiplied by a scalar field on vertices, produces gradient
        vectors per face (stacked as Gx, Gy, Gz).

    """
    V, F = as_native_mesh(M, "mesh")
    return _grad.trimesh_grad(V, F)
