import numpy as np

from compas_libigl import _curvature


def trimesh_gaussian_curvature(M):
    """Compute the discrete gaussian curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[float]
        The gaussian curvature per vertex.

    Examples
    --------
    >>> import compas
    >>> import compas_libigl as libigl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(compas.get("tubemesh.off"))
    >>> mesh.quads_to_triangles()
    >>> M = mesh.to_vertices_and_faces()
    >>> K = libigl.trimesh_gaussian_curvature(M)
    >>> len(K) == len(mesh.vertices)
    True

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _curvature.trimesh_gaussian_curvature(V, F)


def trimesh_principal_curvature(M):
    """Compute the principal curvatures and directions of a triangle mesh.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    tuple[list[list[float]], list[list[float]], list[float], list[float]]
        The principal directions (PD1, PD2) and principal values (PV1, PV2).

    Examples
    --------
    >>> import compas
    >>> import compas_libigl as libigl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(compas.get("tubemesh.off"))
    >>> mesh.quads_to_triangles()
    >>> M = mesh.to_vertices_and_faces()
    >>> PD1, PD2, PV1, PV2 = libigl.trimesh_principal_curvature(M)
    >>> len(PV1) == len(mesh.vertices)
    True

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    PD1, PD2, PV1, PV2 = _curvature.trimesh_principal_curvature(V, F)
    return PD1.tolist(), PD2.tolist(), PV1.tolist(), PV2.tolist()
