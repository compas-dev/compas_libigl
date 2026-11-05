"""Shared array conversion at native triangle-mesh boundaries."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from compas._typing import NumericArray
    from compas._typing import TriangleMeshInput

type NativeTriangleMesh = tuple[np.ndarray, np.ndarray]


def as_scalarfield(values: Sequence[float] | NumericArray, vertex_count: int) -> np.ndarray:
    """Convert a per-vertex scalar field to a native array.

    Parameters
    ----------
    values
        Scalar value at every mesh vertex.
    vertex_count
        Number of mesh vertices.

    Returns
    -------
    numpy.ndarray
        C-contiguous `float64` scalar values.

    """
    scalars = np.asarray(values, dtype=np.float64)
    if scalars.ndim != 1:
        raise ValueError("scalarfield should be one-dimensional.")
    if len(scalars) != vertex_count:
        raise ValueError("scalarfield should contain one value per mesh vertex.")
    if not len(scalars):
        raise ValueError("scalarfield should not be empty.")
    if not np.all(np.isfinite(scalars)):
        raise ValueError("scalarfield should contain only finite values.")
    return np.ascontiguousarray(scalars, dtype=np.float64)


def as_native_mesh(mesh: TriangleMeshInput, name: str) -> NativeTriangleMesh:
    """Convert structural mesh buffers to the representation required by libigl.

    Parameters
    ----------
    mesh
        Structural vertex and triangle buffers.
    name
        Input name used in error messages.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        C-contiguous `float64` vertices and `int32` triangles.

    """
    try:
        vertices, faces = mesh
    except (TypeError, ValueError):
        raise TypeError(f"{name} should be a (vertices, triangles) pair.")

    vertices = np.ascontiguousarray(vertices, dtype=np.float64)
    faces = np.ascontiguousarray(faces, dtype=np.int64)
    if vertices.ndim != 2 or vertices.shape[1] != 3:
        raise ValueError(f"{name} vertices should have shape (N, 3).")
    if faces.ndim != 2 or faces.shape[1] != 3:
        raise ValueError(f"{name} faces should have shape (M, 3).")
    if not np.isfinite(vertices).all():
        raise ValueError(f"{name} vertices should be finite.")
    if faces.size:
        minimum = faces.min()
        maximum = faces.max()
        limits = np.iinfo(np.int32)
        if minimum < limits.min or maximum > limits.max:
            raise OverflowError(f"{name} face indices exceed the range supported by libigl.")
        if minimum < 0 or maximum >= len(vertices):
            raise IndexError(f"{name} face index is out of range.")
    return vertices, np.ascontiguousarray(faces, dtype=np.int32)


def validate_native_mesh(result: NativeTriangleMesh, operation: str) -> NativeTriangleMesh:
    """Check the shape of a native triangle-mesh result.

    Parameters
    ----------
    result
        Native vertex and triangle arrays.
    operation
        Operation name used in error messages.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        The unchanged native vertex and triangle arrays.

    """
    vertices, faces = result
    if vertices.ndim != 2 or vertices.shape[1] != 3:
        raise RuntimeError(f"libigl {operation} result vertices should have shape (N, 3).")
    if faces.ndim != 2 or faces.shape[1] != 3:
        raise RuntimeError(f"libigl {operation} result faces should have shape (M, 3).")
    return vertices, faces


def validate_native_vector(result: np.ndarray, length: int, operation: str) -> np.ndarray:
    """Check the shape of a native per-vertex result.

    Parameters
    ----------
    result
        Native result array.
    length
        Expected number of values.
    operation
        Operation name used in error messages.

    Returns
    -------
    numpy.ndarray
        The unchanged native result array.

    """
    if result.ndim != 1 or len(result) != length:
        raise RuntimeError(f"libigl {operation} result should have shape ({length},).")
    return result


def validate_native_uv(result: np.ndarray, vertex_count: int, operation: str) -> np.ndarray:
    """Check the shape of a native UV result.

    Parameters
    ----------
    result
        Native UV array.
    vertex_count
        Expected number of UV coordinates.
    operation
        Operation name used in error messages.

    Returns
    -------
    numpy.ndarray
        The unchanged native UV array.

    """
    if result.ndim != 2 or result.shape != (vertex_count, 2):
        raise RuntimeError(f"libigl {operation} result should have shape ({vertex_count}, 2).")
    return result
