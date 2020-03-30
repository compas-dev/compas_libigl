import os
import numpy
import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas_plotters import MeshPlotter
import compas_libigl as igl

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh = Mesh.from_json(FILE)
mesh_quads_to_triangles(mesh)

key_index = mesh.key_index()

# Option 1: create numpy arrays pass matrices as references to C++

vertices = mesh.get_vertices_attributes('xyz')
faces = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

V = numpy.array(vertices, dtype=numpy.float64)
F = numpy.array(faces, dtype=numpy.int32)

heat_obj = igl.HeatObject()
heat_obj.setMesh(V, F)
d = heat_obj.getDistanceHeat(0)

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.draw_vertices(text={key: "{:.0f}".format(d[key_index[key]]) for key in mesh.vertices()})
plotter.show()

# Option 2: pass compas mesh object to C++ and use it there "directly":
# (in this case, the data is still copied on the c++ side, but if the data within the mesh object
# would directly be compatible with the igl function, then it could be done without
# copying or conversion)

heat_obj2 = igl.HeatObject()
heat_obj2.setMesh(mesh)
d2 = heat_obj2.getDistanceHeat(0)

plotter2 = MeshPlotter(mesh, figsize=(8, 5))
plotter2.draw_faces()
plotter2.draw_vertices(text={key: "{:.0f}".format(d2[key_index[key]]) for key in mesh.vertices()})
plotter2.show()
