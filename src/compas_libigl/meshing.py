from collections.abc import Sequence

import numpy as np
from compas.geometry import Tessellation
from compas.plugins import plugin

from compas_libigl import _meshing
from compas_libigl._tessellation import as_libigl_tessellation
from compas_libigl._tessellation import as_scalarfield


@plugin(category="trimesh")
def trimesh_remesh_along_isoline(
    mesh: Tessellation,
    scalarfield: Sequence[float],
    scalar: float,
) -> Tessellation:
    """Remesh a triangle mesh along an isoline.

    Parameters
    ----------
    mesh
        The triangle tessellation.
    scalarfield : list[float]
        A scalar value per vertex.
    scalar
        The value at which to compute the isoline.

    Returns
    -------
    Tessellation
        The remeshed triangle geometry.
    """
    V, F = as_libigl_tessellation(mesh)
    S = as_scalarfield(scalarfield, len(V))
    if not np.isfinite(scalar):
        raise ValueError("scalar should be finite.")
    V2, F2, _ = _meshing.trimesh_remesh_along_isoline(V, F, S, np.float64(scalar))
    return Tessellation(V2, F2)


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
