import os
import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness
from compas_plotters import MeshPlotter
from compas.utilities import i_to_rgb
from compas_libigl import planarize_quads

TOL = 0.01
MAXDEV = 0.005
KMAX = 500
HERE = os.path.dirname(__file__)

# FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')
# mesh1 = Mesh.from_json(FILE)

# FILE = os.path.join(HERE, '../data/libigl-tutorial-data/inspired_mesh_quads_Conjugate.off')
# FILE = os.path.join(HERE, '../data/bunny.off')

mesh1 = Mesh.from_off(compas.get('tubemesh.off'))

vertices, faces = mesh1.to_vertices_and_faces()
vertices = planarize_quads(vertices, faces, KMAX, MAXDEV)

mesh2 = Mesh.from_vertices_and_faces(vertices, faces)
dev2 = mesh_flatness(mesh2, maxdev=TOL)

plotter = MeshPlotter(mesh2, figsize=(8, 5))
plotter.draw_faces(facecolor={fkey: i_to_rgb(dev2[fkey]) for fkey in mesh2.faces()})
plotter.show()
