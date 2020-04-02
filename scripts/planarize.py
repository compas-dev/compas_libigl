import os
from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness
from compas_plotters import MeshPlotter
from compas.utilities import i_to_rgb
import compas_libigl as igl

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.off')

TOL = 0.02
MAXDEV = 0.005
KMAX = 500

mesh = Mesh.from_off(FILE)

V, F = mesh.to_vertices_and_faces()
V2 = igl.planarize_quads((V, F), KMAX, MAXDEV)

mesh = Mesh.from_vertices_and_faces(V2, F)
dev = mesh_flatness(mesh, maxdev=TOL)

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces(facecolor={fkey: i_to_rgb(dev[fkey]) for fkey in mesh.faces()})
plotter.show()
