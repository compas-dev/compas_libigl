from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_boundaries import trimesh_boundaries as _trimesh_boundaries


def trimesh_boundaries(M):
    """Compute all (ordered) boundary loops of a manifold triangle mesh.

    Parameters
    ----------
    M : tuple or :class:`compas.datastructures.Mesh`
        A mesh represented by a list of vertices and a list of faces
        or a COMPAS mesh object.

    Returns
    -------
    array
        The ordered boundary loops of the triangle mesh.

    Notes
    -----
    The input mesh should be manifold.

    Examples
    --------
    >>> import compas_libigl as igl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(igl.get('tubemesh.off'))
    >>> mesh.quads_to_triangles()
    >>> boundaries = igl.trimesh_boundaries(mesh)
    >>> len(boundaries) == 1
    True
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _trimesh_boundaries(V, F)


__all__ = [_ for _ in dir() if not _.startswith('_')]
