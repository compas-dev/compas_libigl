import numpy

import compas
import compas_libigl

from compas.datastructures import Mesh
from compas.plotters import MeshPlotter

import iso


mesh = Mesh.from_off('../../../data/libigl-tutorial-data/bunny.off')

V = numpy.array(mesh.get_vertices_attributes('xyz'), dtype=numpy.float64)
F = numpy.array([mesh.face_vertices(fkey) for fkey in mesh.faces()], dtype=numpy.int32)

z = numpy.array(mesh.get_vertices_attribute('z'), dtype=numpy.float64)
n = 100

result = iso.isolines(V, F, z, n)

print(result)

# plotter = MeshPlotter(mesh)
# plotter.draw_faces()
# plotter.show()
