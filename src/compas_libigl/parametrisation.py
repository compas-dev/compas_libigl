from compas.geometry import Tessellation
from compas.plugins import plugin

from compas_libigl import _parametrisation
from compas_libigl._tessellation import as_libigl_tessellation
from compas_libigl._tessellation import validate_parametrisation_topology


@plugin(category="trimesh", pluggable_name="trimesh_harmonic")
def trimesh_harmonic(mesh: Tessellation) -> list[list[float]]:
    """Compute the harmonic parametrisation of a triangle mesh within a fixed circular boundary.

    Parameters
    ----------
    mesh
        The triangle tessellation.

    Returns
    -------
    list[list[float]]
        The u, v parameters per vertex.

    """
    V, F = as_libigl_tessellation(mesh)
    validate_parametrisation_topology(F, len(V))
    return _parametrisation.harmonic(V, F).tolist()


@plugin(category="trimesh", pluggable_name="trimesh_lscm")
def trimesh_lscm(mesh: Tessellation) -> list[list[float]]:
    """Compute the least squares conformal map of a triangle mesh.

    Parameters
    ----------
    mesh
        The triangle tessellation.

    Returns
    -------
    list[list[float]]
        The u, v parameters per vertex.

    """
    V, F = as_libigl_tessellation(mesh)
    validate_parametrisation_topology(F, len(V))
    return _parametrisation.lscm(V, F).tolist()
