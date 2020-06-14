from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_meshing \
    import trimesh_remesh_along_isoline as _trimesh_remesh_along_isoline


def trimesh_remesh_along_isoline(mesh, scalarfield, scalar):
    """Remesh a mesh along an isoline of a scalarfield over the vertices.

    Parameters
    ----------
    mesh : tuple or :class:`compas.datastructures.Mesh`
        A mesh represented by a list of vertices and a list of faces
        or a COMPAS mesh object.
    scalarfield : list or array of float
        A scalar value per vertex of the mesh.
    scalar : float
        A value within the range of the scalarfield.

    Returns
    -------
    tuple
        Vertices and faces of the remeshed mesh.

    Examples
    --------
    >>> import compas_libigl as igl
    >>> from compas.datastructures import Mesh
    >>>

    """
    V, F = mesh
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    S = np.asarray(scalarfield, dtype=np.float64)
    return _trimesh_remesh_along_isolines(V, F, S, scalar)


__all__ = [_ for _ in dir() if not _.startswith('_')]
