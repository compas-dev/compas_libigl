from typing import SupportsFloat

import numpy as np
from compas.typing import PointsLike

from compas_libigl._mesh import validate_result_shape

from . import _simplify

__all__ = ["ramer_douglas_peucker"]


def ramer_douglas_peucker(
    points: PointsLike,
    threshold: SupportsFloat,
) -> tuple[list[list[float]], list[int], list[list[float]]]:
    """Simplify a polyline using Ramer-Douglas-Peucker algorithm.

    Parameters
    ----------
    points
        A list of 3D points representing the polyline.
    threshold
        Maximum distance threshold for simplification.
        Points that deviate less than this from the simplified line are removed.

    Returns
    -------
    tuple[list[list[float]], list[int], list[list[float]]]
        A tuple containing
        * the simplified polyline points (S),
        * indices in original polyline that were kept (J),
        * for each original point, the corresponding point on the simplified curve (Q).

    Raises
    ------
    RuntimeError
        If libigl returns malformed point, retained-index, or projected-point
        arrays.

    """
    P = np.asarray(points, dtype=np.float64)
    S, J, Q = _simplify.ramer_douglas_peucker(P, float(threshold))
    validate_result_shape(S, (None, 3), "polyline simplification points")
    validate_result_shape(J, (len(S),), "polyline simplification retained indices")
    validate_result_shape(Q, (len(P), 3), "polyline simplification projected points")
    return S.tolist(), J.tolist(), Q.tolist()
