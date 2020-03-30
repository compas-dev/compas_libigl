import os
import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness
from compas_plotters import MeshPlotter
from compas.utilities import i_to_rgb
import compas_libigl as igl

TOL = 0.02
MAXDEV = 0.005
KMAX = 500
HERE = os.path.dirname(__file__)

mesh = Mesh.from_off(compas.get('tubemesh.off'))

vertices, faces = mesh.to_vertices_and_faces()
vertices = igl.planarize_quads(vertices, faces, KMAX, MAXDEV)

mesh = Mesh.from_vertices_and_faces(vertices, faces)
dev = mesh_flatness(mesh, maxdev=TOL)

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces(facecolor={fkey: i_to_rgb(dev[fkey]) for fkey in mesh.faces()})
plotter.show()
