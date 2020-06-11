from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from compas_libigl_planarize import planarize_quads as _planarize_quads


def quadmesh_planarize(M, kmax=500, maxdev=0.005):
    """Planarize the faces of a quad mesh.

    Parameters
    ----------
    M : tuple or :class:`compas.datastructures.Mesh`
        A quad mesh represented by a list of vertices and a list of faces
        or by a COMPAS mesh object.
    kmax : int, optional
        The maximum number of iterations.
        Default is ``500``.
    maxdev : float, optional
        The maximum deviation from planar.
        Default is ``0.005``.

    Returns
    -------
    list
        The coordinates of the new vertices.

    Examples
    --------
    >>>

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _planarize_quads(V, F, kmax, maxdev)


__all__ = [_ for _ in dir() if not _.startswith('_')]
