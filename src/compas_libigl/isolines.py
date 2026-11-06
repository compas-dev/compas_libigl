from __future__ import annotations

import numpy as np
from compas.typing import FloatSequenceLike
from compas.typing import VerticesFaces

from compas_libigl._mesh import as_native_mesh
from compas_libigl._mesh import as_scalarfield
from compas_libigl._mesh import validate_result_shape

from . import _isolines

__all__ = ["trimesh_isolines"]


def trimesh_isolines(
    mesh: VerticesFaces,
    scalarfield: FloatSequenceLike,
    number_of_isolines: int = 50,
) -> tuple[list[list[float]], list[list[int]]]:
    """Compute isolines on a triangle mesh.

    Parameters
    ----------
    mesh
        Structural vertex and triangle buffers.
    scalarfield
        Scalar values, one per vertex of the mesh.
    number_of_isolines
        The number of evenly spaced isolines.

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        The isoline point coordinates and segments.

    Raises
    ------
    RuntimeError
        If libigl returns malformed point, segment, or segment-label arrays.

    Notes
    -----
    The input mesh should be triangulated for accurate results.
    A constant scalar field has no interior isolines and returns two empty
    lists without invoking libigl.

    """
    if number_of_isolines < 1:
        raise ValueError("number_of_isolines should be positive.")
    V, F = as_native_mesh(mesh, "mesh")
    S = as_scalarfield(scalarfield, len(V))
    minimum = float(S.min())
    maximum = float(S.max())
    if minimum == maximum:
        points = np.empty((0, 3), dtype=np.float64)
        segments = np.empty((0, 2), dtype=np.int32)
    else:
        ISO = np.linspace(minimum, maximum, number_of_isolines + 2)[1:-1]
        points, segments, labels = _isolines.trimesh_isolines(V, F, S, ISO)
        validate_result_shape(labels, (len(segments),), "isolines segment labels")
    if points.ndim != 2 or points.shape[1] != 3:
        raise RuntimeError("libigl isolines result points should have shape (N, 3).")
    if segments.ndim != 2 or segments.shape[1] != 2:
        raise RuntimeError("libigl isolines result segments should have shape (M, 2).")
    return points.tolist(), segments.tolist()
