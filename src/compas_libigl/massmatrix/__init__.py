import numpy as np
from compas_libigl_massmatrix import trimesh_massmatrix as _trimesh_massmatrix
from compas.plugins import plugin


@plugin(category="trimesh")
def trimesh_massmatrix(M):
    """Compute massmatrix on a triangle mesh using a scalarfield of data points
    assigned to its vertices.

    Parameters
    ----------
    M : tuple or :class:`compas.datastructures.Mesh`
        A mesh represented by a list of vertices and a list of faces
        or by a COMPAS mesh object.

    Returns
    -------
    array
        The mass per vertex.

    Examples
    --------
    >>> import compas
    >>> import compas_libigl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(compas.get('tubemesh.off'))
    >>> mesh.quads_to_triangles()
    >>> M = mesh.to_vertices_and_faces()
    >>> mass = compas_libigl.trimesh_massmatrix(M)

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _trimesh_massmatrix(V, F)
