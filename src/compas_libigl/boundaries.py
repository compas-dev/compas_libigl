from compas.typing import VerticesFaces

from compas_libigl._mesh import as_native_faces

from . import _boundaries

__all__ = ["trimesh_boundaries"]


def trimesh_boundaries(M: VerticesFaces) -> list[list[int]]:
    """Compute all ordered boundary loops of a manifold triangle mesh.

    Uses libigl to extract and order the boundary loops of a triangle mesh.
    The input mesh must be manifold for correct results.

    Parameters
    ----------
    M
        Structural vertex and triangle buffers.

    Returns
    -------
    list[list[int]]
        The ordered boundary loops of the triangle mesh.
        Each loop is a sequence of vertex indices defining a closed boundary.

    Notes
    -----
    The input mesh should be manifold. Non-manifold meshes may produce
    unexpected or incorrect results.

    """
    _, F = M
    F = as_native_faces(F, "mesh faces")
    result = _boundaries.trimesh_boundaries(F)
    return [list(loop) for loop in result]
