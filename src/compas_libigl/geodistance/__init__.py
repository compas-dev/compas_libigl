from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_geodistance import trimesh_geodistance_exact as _exact
from compas_libigl_geodistance import trimesh_geodistance_heat as _heat


def trimesh_geodistance(M, source, method='exact'):
    """Compute the geodesic distance from every vertex of the mesh to a source vertex.

    Parameters
    ----------
    M : tuple or :class:`compas.datastructures.Mesh`
        A triangle mesh represented by a tuple of vertices and faces
        or a COMPAS mesh object.
    source : int
        The index of the vertex from where the geodesic distances should be calculated.
    method : {'exact', 'heat'}
        The method for calculating the distances.
        Default is `'exact'`.

    Returns
    -------
    list of float
        A list of geodesic distances from the source vertex.

    Raises
    ------
    NotImplementedError
        If ``method`` is not one of ``{'exact', 'heat'}``.

    Examples
    --------
    >>>
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    if method == 'exact':
        return _exact(V, F, source)
    if method == 'heat':
        return _heat(V, F, source)
    raise NotImplementedError


__all__ = [_ for _ in dir() if not _.startswith('_')]
