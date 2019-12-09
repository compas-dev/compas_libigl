import os
import numpy
import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.utilities import Colormap
from compas_plotters import MeshPlotter
import compas_libigl as igl

# mesh = Mesh.from_off('../../../data/libigl-tutorial-data/bunny.off')
# mesh = Mesh.from_obj('../../../data/libigl-tutorial-data/armadillo.obj')

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh = Mesh.from_json(FILE)
mesh_quads_to_triangles(mesh)

key_index = mesh.key_index()

vertices = mesh.get_vertices_attributes('xyz')
faces = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

V = numpy.array(vertices, dtype=numpy.float64)
F = numpy.array(faces, dtype=numpy.int32)
D = igl.trimesh_geodistance_exact(V, F, 0)

cmap = Colormap(D, 'red')

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.draw_vertices(radius=0.2, facecolor={key: cmap(d) for key, d in zip(mesh.vertices(), D)})
plotter.show()
