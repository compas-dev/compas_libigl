from __future__ import annotations

import numpy as np
from compas.typing import VerticesFaces

from . import _planarize

__all__ = ["quadmesh_planarize"]


def quadmesh_planarize(M: VerticesFaces, kmax: int = 500, maxdev: float = 0.005) -> list[list[float]]:
    """Planarize the faces of a quad mesh.

    Iteratively modify vertex positions to make all quad faces as planar as possible
    while minimizing the deviation from the original shape.

    Parameters
    ----------
    M
        Vertex coordinates and triangle or quad faces.
    kmax
        The maximum number of iterations.
    maxdev
        The maximum allowed deviation from planarity.

    Returns
    -------
    list[list[float]]
        The coordinates of the new vertices after planarization.

    Raises
    ------
    ValueError
        If the vertices are not finite 3D coordinates, or if a face has a
        number of vertices other than three or four.
    OverflowError
        If a face index exceeds the range supported by libigl.
    IndexError
        If a face index is outside the vertex array.
    RuntimeError
        If the native result does not contain one 3D point per input vertex.

    Notes
    -----
    Triangle faces are padded for the native operation without modifying the
    input face sequences.

    """

    vertices, faces = M
    padded_faces = []

    for face in faces:
        padded_face = list(face)
        if len(padded_face) == 3:
            padded_face.append(padded_face[0])
        elif len(padded_face) != 4:
            raise ValueError("All faces must be triangles or quads for planarization.")
        padded_faces.append(padded_face)

    V = np.ascontiguousarray(vertices, dtype=np.float64)
    F64 = np.ascontiguousarray(padded_faces, dtype=np.int64)
    if V.ndim != 2 or V.shape[1] != 3:
        raise ValueError("mesh vertices should have shape (N, 3).")
    if not np.isfinite(V).all():
        raise ValueError("mesh vertices should be finite.")
    if F64.ndim != 2 or F64.shape[1] != 4:
        raise ValueError("mesh faces should have shape (M, 4) after padding triangles.")
    if F64.size:
        minimum = F64.min()
        maximum = F64.max()
        limits = np.iinfo(np.int32)
        if minimum < limits.min or maximum > limits.max:
            raise OverflowError("mesh face indices exceed the range supported by libigl.")
        if minimum < 0 or maximum >= len(V):
            raise IndexError("mesh face index is out of range.")

    F = np.ascontiguousarray(F64, dtype=np.int32)
    result = _planarize.planarize_quads(V, F, kmax, maxdev)
    if not isinstance(result, np.ndarray) or result.shape != (len(V), 3):
        raise RuntimeError(f"libigl planarization result should have shape ({len(V)}, 3).")
    return result.tolist()
