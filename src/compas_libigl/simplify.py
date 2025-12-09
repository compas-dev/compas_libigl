import numpy as np
from compas.plugins import plugin

from compas_libigl import _simplify


@plugin(category="polyline")
def ramer_douglas_peucker(points, threshold):
    """Simplify a polyline using Ramer-Douglas-Peucker algorithm.

    Parameters
    ----------
    points : list[list[float]]
        A list of 3D points representing the polyline.
    threshold : float
        Maximum distance threshold for simplification.
        Points that deviate less than this from the simplified line are removed.

    Returns
    -------
    tuple[list[list[float]], list[int], list[int]]
        A tuple containing
        * the simplified polyline points,
        * indices in original polyline that were kept,
        * for each simplified point, its index in the original polyline.
    """
    P = np.asarray(points, dtype=np.float64)
    S, J, Q = _simplify.ramer_douglas_peucker(P, float(threshold))
    return S.tolist(), J.tolist(), Q.tolist()
