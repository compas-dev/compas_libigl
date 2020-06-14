from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_curvature import trimesh_gaussian_curvature as _gaussian
from compas_libigl_curvature import trimesh_principal_curvature as _principal


def trimesh_gaussian_curvature(M):
    """Compute the discrete gaussian curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple or :class:`compas.datastructures.Mesh`
        A mesh represented by a list of vertices and a list of faces
        or a COMPAS mesh object.

    Returns
    -------
    array
        The discrete gaussian curvature per vertex.

    Examples
    --------
    >>> import compas_libigl as igl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(igl.get('tubemesh.off'))
    >>> mesh.quads_to_triangles()
    >>> curvature = igl.trimesh_curvature(mesh)
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _trimesh_gaussian_curvature(V, F)


def trimesh_principal_curvature():
    pass


__all__ = [_ for _ in dir() if not _.startswith('_')]
