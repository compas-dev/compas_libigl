"""Shared array conversion at native triangle-mesh boundaries."""

from collections.abc import Iterable
from operator import index
from typing import SupportsIndex

import numpy as np
from compas.typing import Float64Array
from compas.typing import FloatSequenceLike
from compas.typing import Int32Array
from compas.typing import VerticesFaces

type NativeTriangleMesh = tuple[Float64Array, Int32Array]


def as_native_index_vector(values: Iterable[SupportsIndex], name: str) -> list[int]:
    """Convert an index vector to exact Python integers."""
    result: list[int] = []
    for value in values:
        if isinstance(value, (bool, np.bool_)):
            raise TypeError(f"{name} should contain integer indices, not booleans.")
        result.append(index(value))
    return result


def as_native_index_groups(values: Iterable[Iterable[SupportsIndex]], name: str) -> list[list[int]]:
    """Convert nested index groups to exact Python integers."""
    return [as_native_index_vector(group, name) for group in values]


def as_native_faces(faces: object, name: str, vertex_count: int | None = None) -> Int32Array:
    """Convert triangle indices to the representation required by libigl.

    Parameters
    ----------
    faces
        Triangle index rows.
    name
        Input name used in error messages.
    vertex_count
        Optional number of vertices for range validation.

    Returns
    -------
    numpy.ndarray
        C-contiguous `int32` triangle indices.

    """
    native = np.ascontiguousarray(faces, dtype=np.int64)
    if native.ndim != 2 or native.shape[1] != 3:
        raise ValueError(f"{name} should have shape (M, 3).")
    if native.size:
        minimum = native.min()
        maximum = native.max()
        limits = np.iinfo(np.int32)
        if minimum < limits.min or maximum > limits.max:
            raise OverflowError(f"{name} indices exceed the range supported by libigl.")
        if minimum < 0:
            raise IndexError(f"{name} index is out of range.")
        if vertex_count is not None and maximum >= vertex_count:
            raise IndexError(f"{name} index is out of range.")
    return np.ascontiguousarray(native, dtype=np.int32)


def as_scalarfield(values: FloatSequenceLike, vertex_count: int) -> Float64Array:
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


def as_native_mesh(mesh: VerticesFaces, name: str) -> NativeTriangleMesh:
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
    if vertices.ndim != 2 or vertices.shape[1] != 3:
        raise ValueError(f"{name} vertices should have shape (N, 3).")
    if not np.isfinite(vertices).all():
        raise ValueError(f"{name} vertices should be finite.")
    return vertices, as_native_faces(faces, f"{name} faces", len(vertices))


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


def validate_native_vector(result: Float64Array, length: int, operation: str) -> Float64Array:
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


def validate_native_uv(result: Float64Array, vertex_count: int, operation: str) -> Float64Array:
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
