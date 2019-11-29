from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

HERE = os.path.dirname(__file__)
HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))

print(HERE)

def get(filename):
    filename = filename.strip('/')
    return os.path.abspath(os.path.join(DATA, filename))


from .planarize import planarize_quads
from .isolines import trimesh_isolines
from .triangulation import triangulate_polygon

from .geodistance import trimesh_geodistance_exact
from .geodistance import trimesh_geodistance_heat

from .booleans import mesh_union
from .csgtree import mesh_csgtree


__all__ = [name for name in dir() if not name.startswith('__')]
