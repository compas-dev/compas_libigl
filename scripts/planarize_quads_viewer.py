import os
import numpy
import compas

from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness
from compas.utilities import i_to_rgb
from compas_viewers.meshviewer import MeshViewer
from compas_libigl import planarize_quads


# note: add zoom_extents, flip_cycles,
# note: add custom command planarize_faces

# viewer.add_command(planarize_quads_cmd)

MAXDEV = 0.005
KMAX = 500

HERE = os.path.dirname(__file__)

# FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')
# mesh1 = Mesh.from_json(FILE)

FILE = os.path.join(HERE, '../data/libigl-tutorial-data/inspired_mesh_quads_Conjugate.off')
mesh1 = Mesh.from_off(FILE)

vertices, faces = mesh1.to_vertices_and_faces()

V1 = numpy.array(vertices, dtype=numpy.float64)
F1 = numpy.array(faces, dtype=numpy.int32)

V2 = planarize_quads(V1, F1, KMAX, MAXDEV)

mesh2 = Mesh.from_vertices_and_faces(V2, faces)
dev2 = mesh_flatness(mesh2, maxdev=MAXDEV)

viewer = MeshViewer()
viewer.mesh = mesh2
viewer.show()
