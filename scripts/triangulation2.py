import os
import json
import numpy
import compas
from compas.datastructures import Mesh
from compas.geometry import centroid_points_xy
from compas_plotters import MeshPlotter
from compas.utilities import geometric_key
from compas.utilities import pairwise
import compas_libigl as igl

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
FILE = os.path.join(DATA, 'rhino1.json')

with open(FILE, 'r') as f:
    data = json.load(f)

gkey_xyz = {geometric_key(point): point for point in data['boundary']}
gkey_xyz.update({geometric_key(point): point for point in data['segments']})
gkey_xyz.update({geometric_key(point): point for point in data['hole']})
gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz.keys())}

xyz = list(gkey_xyz.values())
edges = []
edges += [[gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]] for a, b in pairwise(data['boundary'])]
edges += [[gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]] for a, b in pairwise(data['segments'])]
edges += [[gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]] for a, b in pairwise(data['hole'])]
holes = []
holes += [centroid_points_xy([xyz[gkey_index[geometric_key(point)]] for point in data['hole'][:-1]])]

V = numpy.array(xyz, dtype=numpy.float64)
E = numpy.array(edges, dtype=numpy.int32)
H = numpy.array(holes, dtype=numpy.float64)

# tri = igl.delaunay_triangulation(V)
# tri = igl.constrained_delaunay_triangulation(V, E)
tri = igl.conforming_delaunay_triangulation(V, E, H, area=0.05)

V2 = tri.vertices
F2 = tri.faces

mesh = Mesh.from_vertices_and_faces(V2, F2)

lines = []
for u, v in E:
    lines.append({'start': V[u], 'end': V[v], 'color': '#ff0000', 'width': 2.0})

# points = []
# for point in H:
#     points.append({'pos': point, 'edgecolor': '#0000ff', 'radius': 0.5})

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
# plotter.draw_points(points)
plotter.draw_lines(lines)
plotter.show()
