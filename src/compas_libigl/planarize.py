import numpy as np
from compas.plugins import plugin

from compas_libigl import _planarize


@plugin(category="quadmesh")
def quadmesh_planarize(M, kmax=500, maxdev=0.005):
    """Planarize the faces of a quad mesh.

    Iteratively modify vertex positions to make all quad faces as planar as possible
    while minimizing the deviation from the original shape.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A quad mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are quads
    kmax : int, optional
        The maximum number of iterations.
        Default is ``500``.
    maxdev : float, optional
        The maximum allowed deviation from planarity.
        Default is ``0.005``.

    Returns
    -------
    list[list[float]]
        The coordinates of the new vertices after planarization.

    Notes
    -----
    The input mesh should consist primarily of quad faces for best results.
    Non-quad faces may produce unexpected results.
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _planarize.planarize_quads(V, F, kmax, maxdev)
