from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from compas.plugins import plugin

from compas_libigl import _meshing  # type: ignore
from compas_libigl._mesh import as_native_mesh
from compas_libigl._mesh import as_scalarfield
from compas_libigl._mesh import validate_native_mesh

if TYPE_CHECKING:
    from collections.abc import Sequence

    from compas._typing import NumericArray
    from compas._typing import TriangleMeshInput


@plugin(category="trimesh", pluggable_name="_trimesh_remesh_along_isoline")
def trimesh_remesh_along_isoline(
    mesh: TriangleMeshInput,
    scalarfield: Sequence[float] | NumericArray,
    scalar: float,
) -> TriangleMeshInput:
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
    V2, F2, _ = _meshing.trimesh_remesh_along_isoline(V, F, S, np.float64(scalar))
    return validate_native_mesh((V2, F2), "remesh-along-isoline")


def trimesh_remesh_along_isolines(M, scalars, isovalues):
    """Remesh a triangle mesh along multiple isolines.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles
    scalars : list[float]
        A scalar value per vertex.
    isovalues : list[float]
        The values at which to compute the isolines.

    Returns
    -------
    tuple[list[list[float]], list[list[int]], list[float], list[int]]
        A tuple containing
        * the vertices of the remeshed mesh,
        * the faces of the remeshed mesh,
        * scalar values for the vertices of the remeshed mesh,
        * labels for the faces of the remeshed mesh.
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    S = np.asarray(scalars, dtype=np.float64)
    ISO = np.asarray(isovalues, dtype=np.float64)
    V2, F2, S2, G2 = _meshing.trimesh_remesh_along_isolines(V, F, S, ISO)
    return V2.tolist(), F2.tolist(), S2.tolist(), G2.tolist()


def trimesh_cut_mesh(M, cuts):
    """Cut a mesh along specified edges.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles
    cuts : list[list[int]]
        A matrix of shape (F, 3) with boolean flags indicating
        which edges to cut. For each face, the three values
        correspond to edges (v0,v1), (v1,v2), (v2,v0).

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        A tuple containing
        * the vertices of the cut mesh (with duplicated vertices along cuts),
        * the faces of the cut mesh.
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    C = np.asarray(cuts, dtype=np.int32)
    Vn, Fn = _meshing.trimesh_cut_mesh(V, F, C)
    return Vn.tolist(), Fn.tolist()


def trimesh_face_components(M):
    """Compute connected components of mesh faces.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    list[int]
        Component ID per face. Faces sharing edges belong to the same component.
    """
    V, F = M
    F = np.asarray(F, dtype=np.int32)
    C = _meshing.trimesh_face_components(F)
    return C.tolist()
