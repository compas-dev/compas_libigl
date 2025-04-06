import os
import compas
from ._nanobind import add, __doc__
from .boundaries import trimesh_boundaries
from .curvature import trimesh_gaussian_curvature, trimesh_principal_curvature
from .geodistance import trimesh_geodistance, trimesh_geodistance_multiple
from .intersections import intersection_ray_mesh, intersection_rays_mesh
from .isolines import trimesh_isolines, groupsort_isolines
from .massmatrix import trimesh_massmatrix
from .parametrisation import trimesh_harmonic, trimesh_lscm
from .planarize import quadmesh_planarize
from .meshing import trimesh_remesh_along_isoline, trimesh_remesh_along_isolines


__version__ = "0.4.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


def get(filename):
    """Get the full path to one of the sample data files.

    Parameters
    ----------
    filename : str
        The name of the data file.
        The filename should be specified relative to the COMPAS data directory,
        without leading or trailing slashes.

    Returns
    -------
    str
        The full path to the specified file.

    Notes
    -----
    The file name should be specified relative to the package data directory
    (``compas_libigl/data``).

    Examples
    --------
    >>> import os
    >>> from compas_libigl import get
    >>> get('tubemesh.json')

    """
    filename = filename.strip("/")

    localpath = compas._os.absjoin(DATA, filename)

    if os.path.exists(localpath):
        return localpath

    return None


def find(name):
    """Find a file in the data directory through recursive search.

    """
    datapath = DATA
    return compas.find(name, datapath)


__all_plugins__ = [
    "compas_libigl._nanobind",
    "compas_libigl.boundaries",
    "compas_libigl.curvature",
    "compas_libigl.geodistance",
    "compas_libigl.intersections",
    "compas_libigl.isolines",
    "compas_libigl.massmatrix",
    "compas_libigl.parametrisation",
    "compas_libigl.planarize",
    "compas_libigl.meshing",
]

__all__ = [
    "HOME",
    "DATA",
    "DOCS",
    "TEMP",
    "add",
    "__doc__",
    "get",
    "find",
    "trimesh_boundaries",
    "trimesh_gaussian_curvature",
    "trimesh_principal_curvature",
    "trimesh_geodistance",
    "trimesh_geodistance_multiple",
    "intersection_ray_mesh",
    "intersection_rays_mesh",
    "trimesh_isolines",
    "groupsort_isolines",
    "trimesh_massmatrix",
    "trimesh_harmonic",
    "trimesh_lscm",
    "quadmesh_planarize",
    "trimesh_remesh_along_isoline",
    "trimesh_remesh_along_isolines",
]
