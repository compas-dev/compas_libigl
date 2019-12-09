import numpy
import compas
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter
import compas_libigl as igl

# note: provide interface to triangulation options

V = numpy.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=numpy.float64)
E = numpy.array([[0, 1], [1, 2], [2, 3], [3, 0]], dtype=numpy.int32)

tri = igl.triangulate_polygon(V, E)

V2 = tri.vertices
F2 = tri.faces

mesh = Mesh.from_vertices_and_faces(V2, F2)

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.show()
