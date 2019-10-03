import numpy
import compas
import os
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles

from compas_plotters import MeshPlotter

import geodistance as g

# mesh = Mesh.from_off('../../../data/libigl-tutorial-data/bunny.off')
# mesh = Mesh.from_obj('../../../data/libigl-tutorial-data/armadillo.obj')
dir_path = os.path.dirname(os.path.realpath(__file__))
mesh = Mesh.from_json(dir_path + '/tubemesh.json')

mesh_quads_to_triangles(mesh)


key_index = mesh.key_index()

V = numpy.array(mesh.get_vertices_attributes('xyz'), dtype=numpy.float64)
F = numpy.array([[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()], dtype=numpy.int32)

d = g.exact(V, F, 0)

print(d)

plotter = MeshPlotter(mesh)
plotter.draw_faces()
plotter.draw_vertices(text={key: "{:.0f}".format(d[key_index[key]]) for key in mesh.vertices()})
plotter.show()
