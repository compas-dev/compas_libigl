"""
********************************************************************************
compas_libigl
********************************************************************************

.. currentmodule:: compas_libigl


TriMesh
=======

.. autosummary::
    :toctree: generated/

    trimesh_boundaries
    trimesh_gaussian_curvature
    trimesh_principal_curvature
    trimesh_geodistance
    trimesh_isolines
    trimesh_massmatrix
    trimesh_harmonic
    trimesh_lscm
    trimesh_remesh_along_isoline


QuadMesh
========

.. autosummary::
    :toctree: generated/

    quadmesh_planarize


Miscellaneous
=============

.. autosummary::
    :toctree: generated/

    intersection_ray_mesh

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import compas

from .geodistance import *
from .isolines import *
from .planarize import *
from .massmatrix import *
from .curvature import *
from .intersections import *
from .parametrisation import *
from .boundaries import *
from .meshing import *


__author__ = ["tom van mele"]
__copyright__ = "Block Research Group - ETH Zurich"
__license__ = "Mozilla Public License Version 2.0"
__email__ = "van.mele@arch.ethz.ch"
__version__ = "0.1.0"


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
    >>> mesh = Mesh.from_off(igl.get('bunny.off'))

    """
    filename = filename.strip('/')

    localpath = compas._os.absjoin(DATA, filename)

    if os.path.exists(localpath):
        return localpath
    else:
        return "https://github.com/BlockResearchGroup/compas_libigl/raw/master/data/{}".format(filename)


def get_beetle():
    return "https://raw.githubusercontent.com/libigl/libigl-tutorial-data/master/beetle.off"


def get_armadillo():
    return "https://raw.githubusercontent.com/libigl/libigl-tutorial-data/master/armadillo.obj"


__all__ = [name for name in dir() if not name.startswith('_')]
