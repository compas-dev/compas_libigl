from compas.typing import Float64Array
from compas.typing import VerticesFaces

from compas_libigl._mesh import as_native_mesh

from . import _curvature

__all__ = ["trimesh_gaussian_curvature", "trimesh_principal_curvature"]


def trimesh_gaussian_curvature(M: VerticesFaces) -> Float64Array:
    """Compute the discrete gaussian curvature of a triangle mesh.

    Calculates the Gaussian curvature at each vertex of a triangle mesh
    using the angle defect method.

    Parameters
    ----------
    M
        Structural vertex and triangle buffers.

    Returns
    -------
    numpy.ndarray
        The gaussian curvature values per vertex.
        Positive values indicate elliptic points, negative values indicate hyperbolic points,
        and zero values indicate parabolic or flat points.

    Notes
    -----
    This is a direct libigl operation, not the COMPAS Gaussian-curvature
    plugin. Libigl's angle-defect boundary convention does not match the core
    contract, so the operation is intentionally not registered.

    """
    V, F = as_native_mesh(M, "mesh")
    return _curvature.trimesh_gaussian_curvature(V, F)


def trimesh_principal_curvature(M: VerticesFaces) -> tuple[list[list[float]], list[list[float]], list[float], list[float]]:
    """Compute the principal curvatures and directions of a triangle mesh.

    Calculates both the principal curvature values and their corresponding
    directions at each vertex of the mesh.

    Parameters
    ----------
    M
        Structural vertex and triangle buffers.

    Returns
    -------
    tuple[list[list[float]], list[list[float]], list[float], list[float]]
        A tuple containing:
        * PD1: Principal direction 1 per vertex (normalized vectors)
        * PD2: Principal direction 2 per vertex (normalized vectors)
        * PV1: Principal curvature value 1 per vertex (maximum curvature)
        * PV2: Principal curvature value 2 per vertex (minimum curvature)

    """
    V, F = as_native_mesh(M, "mesh")
    PD1, PD2, PV1, PV2 = _curvature.trimesh_principal_curvature(V, F)
    return PD1.tolist(), PD2.tolist(), PV1.tolist(), PV2.tolist()
