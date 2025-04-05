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


__author__ = ["tom van mele", "petras vestartas"]
__copyright__ = "Block Research Group - ETH Zurich"
__license__ = "Mozilla Public License Version 2.0"
__email__ = "van.mele@arch.ethz.ch, petrasvestartas@gmail.com"
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
        The following are available.

        * boxes.obj
        * faces.obj
        * fink.obj
        * hypar.obj
        * lines.obj
        * saddle.obj

    Returns
    -------
    str
        The full path to the specified file.

    Notes
    -----
    The file name should be specified relative to the sample data folder.
    This folder is only locally available if you installed :mod:`compas_libigl` from source,
    or if you are working directly with the source.
    In all other cases, the function will get the corresponding files direcly from
    the GitHub repo.

    Examples
    --------
    >>> import compas_libigl as igl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(igl.get("bunny.off"))

    """
    filename = filename.strip("/")

    localpath = compas._os.absjoin(DATA, filename)

    if os.path.exists(localpath):
        return localpath
    else:
        return "https://github.com/BlockResearchGroup/compas_libigl/raw/master/data/{}".format(filename)


def get_beetle():
    return "https://raw.githubusercontent.com/libigl/libigl-tutorial-data/master/beetle.off"


def get_armadillo():
    return "https://raw.githubusercontent.com/libigl/libigl-tutorial-data/master/armadillo.obj"


__all_plugins__ = [
    "compas_libigl._nanobindcompas_libigl._boundaries",
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
    "get_beetle",
    "get_armadillo",
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
