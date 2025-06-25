import numpy as np

from compas_libigl import _boundaries


def trimesh_boundaries(M):
    """Compute all ordered boundary loops of a manifold triangle mesh.

    Uses libigl to extract and order the boundary loops of a triangle mesh.
    The input mesh must be manifold for correct results.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    list[list[int]]
        The ordered boundary loops of the triangle mesh.
        Each loop is a sequence of vertex indices defining a closed boundary.

    Notes
    -----
    The input mesh should be manifold.
    Non-manifold meshes may produce unexpected or incorrect results.
    """
    V, F = M
    F = np.asarray(F, dtype=np.int32)
    result = _boundaries.trimesh_boundaries(F)
    return [list(loop) for loop in result]
