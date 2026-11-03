from collections.abc import Sequence

import numpy as np
from compas.geometry import Tessellation
from compas.plugins import plugin

from compas_libigl import _isolines
from compas_libigl._tessellation import as_libigl_tessellation
from compas_libigl._tessellation import as_scalarfield


@plugin(category="trimesh")
def trimesh_isolines(
    mesh: Tessellation,
    scalarfield: Sequence[float] | np.ndarray,
    number_of_isolines: int = 50,
) -> tuple[list[list[float]], list[list[int]]]:
    """
    Compute isolines on a triangle mesh.

    Parameters
    ----------
    mesh
        The triangle tessellation.
    scalarfield : sequence[float] | numpy.ndarray
        Scalar values, one per vertex of the mesh.
    number_of_isolines
        The number of evenly spaced isolines.

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        The isoline point coordinates and segments.

    Notes
    -----
    The input mesh should be triangulated for accurate results.
    """
    if number_of_isolines < 1:
        raise ValueError("number_of_isolines should be positive.")
    V, F = as_libigl_tessellation(mesh)
    S = as_scalarfield(scalarfield, len(V))
    ISO = np.linspace(float(S.min()), float(S.max()), number_of_isolines + 2)[1:-1]

    # Note: C++ function expects (V, F, isovalues, scalars)
    points, segments, _ = _isolines.trimesh_isolines(V, F, ISO, S)
    return points.tolist(), segments.tolist()
