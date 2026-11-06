from __future__ import annotations

import numpy as np
from compas.typing import FloatSequenceLike
from compas.typing import IndexGroupsLike
from compas.typing import VerticesFaces

from compas_libigl._mesh import NativeTriangleMesh
from compas_libigl._mesh import as_native_faces
from compas_libigl._mesh import as_native_mesh
from compas_libigl._mesh import as_scalarfield
from compas_libigl._mesh import validate_native_mesh
from compas_libigl._mesh import validate_result_shape

from . import _meshing

__all__ = [
    "trimesh_cut_mesh",
    "trimesh_face_components",
    "trimesh_remesh_along_isoline",
    "trimesh_remesh_along_isolines",
]


def trimesh_remesh_along_isoline(
    mesh: VerticesFaces,
    scalarfield: FloatSequenceLike,
    scalar: float,
) -> NativeTriangleMesh:
    """Remesh a triangle mesh along an isoline.

    Parameters
    ----------
    mesh
        Structural vertex and triangle buffers.
    scalarfield
        A scalar value per vertex.
    scalar
        The value at which to compute the isoline.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        Native vertex and triangle arrays of the remeshed geometry.

    Raises
    ------
    RuntimeError
        If libigl returns malformed mesh or face-label arrays.

    Notes
    -----
    Input buffers are normalized once at the native boundary. The face labels
    produced internally by libigl are not part of the public result contract.

    """
    V, F = as_native_mesh(mesh, "mesh")
    if not len(F):
        raise ValueError("mesh should contain at least one triangle.")
    S = as_scalarfield(scalarfield, len(V))
    if not np.isfinite(scalar):
        raise ValueError("scalar should be finite.")
    V2, F2, labels = _meshing.trimesh_remesh_along_isoline(V, F, S, scalar)
    V2, F2 = validate_native_mesh((V2, F2), "remesh-along-isoline")
    validate_result_shape(labels, (len(F2),), "remesh-along-isoline face labels")
    return V2, F2


def trimesh_remesh_along_isolines(
    M: VerticesFaces,
    scalars: FloatSequenceLike,
    isovalues: FloatSequenceLike,
) -> tuple[list[list[float]], list[list[int]], list[float], list[int]]:
    """Remesh a triangle mesh along multiple isolines.

    Parameters
    ----------
    M
        Structural vertex and triangle buffers.
    scalars
        A scalar value per vertex.
    isovalues
        The values at which to compute the isolines.

    Returns
    -------
    tuple[list[list[float]], list[list[int]], list[float], list[int]]
        A tuple containing
        * the vertices of the remeshed mesh,
        * the faces of the remeshed mesh,
        * scalar values for the vertices of the remeshed mesh,
        * labels for the faces of the remeshed mesh.

    Raises
    ------
    RuntimeError
        If libigl returns malformed mesh, scalar, or face-label arrays.

    """
    V, F = as_native_mesh(M, "mesh")
    S = as_scalarfield(scalars, len(V))
    ISO = np.asarray(isovalues, dtype=np.float64)
    if ISO.ndim != 1 or not len(ISO):
        raise ValueError("isovalues should be a nonempty one-dimensional sequence.")
    if not np.all(np.isfinite(ISO)):
        raise ValueError("isovalues should contain only finite values.")
    ISO = np.ascontiguousarray(ISO, dtype=np.float64)
    V2, F2, S2, G2 = _meshing.trimesh_remesh_along_isolines(V, F, S, ISO)
    V2, F2 = validate_native_mesh((V2, F2), "remesh-along-isolines")
    validate_result_shape(S2, (len(V2),), "remesh-along-isolines scalar values")
    validate_result_shape(G2, (len(F2),), "remesh-along-isolines face labels")
    return V2.tolist(), F2.tolist(), S2.tolist(), G2.tolist()


def trimesh_cut_mesh(M: VerticesFaces, cuts: IndexGroupsLike) -> tuple[list[list[float]], list[list[int]]]:
    """Cut a mesh along specified edges.

    Parameters
    ----------
    M
        Structural vertex and triangle buffers.
    cuts
        A matrix of shape (F, 3) with boolean flags indicating
        which edges to cut. For each face, the three values
        correspond to edges (v0,v1), (v1,v2), (v2,v0).

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        A tuple containing
        * the vertices of the cut mesh (with duplicated vertices along cuts),
        * the faces of the cut mesh.

    Raises
    ------
    RuntimeError
        If libigl returns malformed vertex or triangle arrays.

    """
    V, F = as_native_mesh(M, "mesh")
    C = np.asarray(cuts, dtype=np.int32)
    if C.shape != F.shape:
        raise ValueError("cuts should have shape (M, 3), matching the mesh triangles.")
    C = np.ascontiguousarray(C, dtype=np.int32)
    Vn, Fn = _meshing.trimesh_cut_mesh(V, F, C)
    Vn, Fn = validate_native_mesh((Vn, Fn), "cut mesh")
    return Vn.tolist(), Fn.tolist()


def trimesh_face_components(M: VerticesFaces) -> list[int]:
    """Compute connected components of mesh faces.

    Parameters
    ----------
    M
        Structural vertex and triangle buffers.

    Returns
    -------
    list[int]
        Component ID per face. Faces sharing edges belong to the same component.

    Raises
    ------
    RuntimeError
        If libigl does not return one component ID per mesh face.

    """
    _, F = M
    F = as_native_faces(F, "mesh faces")
    C = _meshing.trimesh_face_components(F)
    validate_result_shape(C, (len(F),), "face components")
    return C.tolist()
