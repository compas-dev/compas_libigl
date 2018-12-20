import numpy

import compas
import triangulation as tri

from compas.datastructures import Mesh
from compas.plotters import MeshPlotter

V = numpy.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=numpy.float64)
E = numpy.array([[0, 1], [1, 2], [2, 3], [3, 0]], dtype=numpy.int32)

result = tri.polygon(V, E)

V2 = result.vertices
F2 = result.faces

mesh = Mesh.from_vertices_and_faces(V2.tolist(), F2.tolist())

plotter = MeshPlotter(mesh)

plotter.draw_faces()

plotter.show()
