from typing import Any, Tuple
from nptyping import NDArray
import numpy as np
from compas_libigl_boundaries import trimesh_boundaries as _trimesh_boundaries


def trimesh_boundaries(
    M: Tuple[
        NDArray[(Any, 3), np.float64],
        NDArray[(Any, 3), np.int32],
    ]
) -> NDArray[(Any, Any), np.int32]:
    """Compute all (ordered) boundary loops of a manifold triangle mesh.

    Parameters
    ----------
    M : (list, list)
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    array
        The ordered boundary loops of the triangle mesh.
        Each loop is a sequence of vertex indices.

    Notes
    -----
    The input mesh should be manifold.

    Examples
    --------
    >>> import compas
    >>> import compas_libigl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(compas.get('tubemesh.off'))
    >>> mesh.quads_to_triangles()
    >>> M = mesh.to_vertices_and_faces()
    >>> boundaries = compas_libigl.trimesh_boundaries(M)
    >>> len(boundaries) == 1
    True

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _trimesh_boundaries(V, F)
