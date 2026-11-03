from compas.geometry import Tessellation
from compas.plugins import plugin

from compas_libigl import _massmatrix
from compas_libigl._tessellation import as_libigl_tessellation


@plugin(category="trimesh")
def trimesh_massmatrix(mesh: Tessellation) -> list[float]:
    """Compute the mass matrix of a triangle mesh.

    Parameters
    ----------
    mesh
        The triangle tessellation.

    Returns
    -------
    list[float]
        The barycentric mass associated with every vertex.
    """
    V, F = as_libigl_tessellation(mesh)
    matrix = _massmatrix.trimesh_massmatrix(V, F)
    return matrix.diagonal().tolist()
