import numpy
import compas
from compas.datastructures import Mesh
from compas.geometry import centroid_points_xy
from compas_plotters import MeshPlotter
import compas_libigl as igl

V = numpy.array([[0, 0, 0], [10, 0, 0], [10, 10, 0], [0, 10, 0], [3, 3, 0], [7, 3, 0], [7, 7, 0], [3, 7, 0]], dtype=numpy.float64)
E = numpy.array([[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [6, 2]], dtype=numpy.int32)
H = numpy.array([centroid_points_xy(V[4:])], dtype=numpy.float64)

# tri = igl.delaunay_triangulation(V)
# tri = igl.constrained_delaunay_triangulation(V, E, area=1.0/1000)
tri = igl.conforming_delaunay_triangulation(V, E, H, area=100.0/5000)

V2 = tri.vertices
F2 = tri.faces

mesh = Mesh.from_vertices_and_faces(V2, F2)

lines = []
for u, v in E:
    lines.append({'start': V[u], 'end': V[v], 'color': '#ff0000', 'width': 2.0})

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.draw_lines(lines)
plotter.show()
