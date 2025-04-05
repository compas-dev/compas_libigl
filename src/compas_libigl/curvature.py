import numpy as np

from compas_libigl import _curvature


def trimesh_gaussian_curvature(M):
    """Compute the discrete gaussian curvature of a triangle mesh.

    Calculates the Gaussian curvature at each vertex of a triangle mesh
    using the angle defect method.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    list[float]
        The gaussian curvature values per vertex.
        Positive values indicate elliptic points, negative values indicate hyperbolic points,
        and zero values indicate parabolic or flat points.
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _curvature.trimesh_gaussian_curvature(V, F)


def trimesh_principal_curvature(M):
    """Compute the principal curvatures and directions of a triangle mesh.

    Calculates both the principal curvature values and their corresponding
    directions at each vertex of the mesh.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles

    Returns
    -------
    tuple[list[list[float]], list[list[float]], list[float], list[float]]
        A tuple containing:
        * PD1: Principal direction 1 per vertex (normalized vectors)
        * PD2: Principal direction 2 per vertex (normalized vectors)
        * PV1: Principal curvature value 1 per vertex (maximum curvature)
        * PV2: Principal curvature value 2 per vertex (minimum curvature)
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    PD1, PD2, PV1, PV2 = _curvature.trimesh_principal_curvature(V, F)
    return PD1.tolist(), PD2.tolist(), PV1.tolist(), PV2.tolist()
