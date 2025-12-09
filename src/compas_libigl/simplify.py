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
    tuple[list[list[float]], list[int], list[list[float]]]
        A tuple containing
        * the simplified polyline points (S),
        * indices in original polyline that were kept (J),
        * for each original point, the corresponding point on the simplified curve (Q).
    """
    P = np.asarray(points, dtype=np.float64)
    S, J, Q = _simplify.ramer_douglas_peucker(P, float(threshold))
    return S.tolist(), J.tolist(), Q.tolist()
