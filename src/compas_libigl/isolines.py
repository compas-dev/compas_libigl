from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from compas.plugins import plugin

from compas_libigl import _isolines  # type: ignore
from compas_libigl._mesh import as_native_mesh
from compas_libigl._mesh import as_scalarfield

if TYPE_CHECKING:
    from collections.abc import Sequence

    from compas._typing import NumericArray
    from compas._typing import TriangleMeshInput


@plugin(category="trimesh", pluggable_name="_trimesh_isolines")
def trimesh_isolines(
    mesh: TriangleMeshInput,
    scalarfield: Sequence[float] | NumericArray,
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

    Notes
    -----
    The input mesh should be triangulated for accurate results.

    """
    if number_of_isolines < 1:
        raise ValueError("number_of_isolines should be positive.")
    V, F = as_native_mesh(mesh, "mesh")
    S = as_scalarfield(scalarfield, len(V))
    ISO = np.linspace(float(S.min()), float(S.max()), number_of_isolines + 2)[1:-1]

    # Note: C++ function expects (V, F, isovalues, scalars)
    points, segments, _ = _isolines.trimesh_isolines(V, F, ISO, S)
    if points.ndim != 2 or points.shape[1] != 3:
        raise RuntimeError("libigl isolines result points should have shape (N, 3).")
    if segments.ndim != 2 or segments.shape[1] != 2:
        raise RuntimeError("libigl isolines result segments should have shape (M, 2).")
    return points.tolist(), segments.tolist()
