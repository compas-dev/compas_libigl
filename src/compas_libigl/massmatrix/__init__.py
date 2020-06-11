from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_massmatrix import trimesh_massmatrix as _trimesh_massmatrix


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
    >>> import compas_libigl as igl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(igl.get('tubemesh.off'))
    >>> mesh.quads_to_triangles()
    >>> mass = igl.trimesh_massmatrix(mesh)
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _trimesh_massmatrix(V, F)


__all__ = [_ for _ in dir() if not _.startswith('_')]
