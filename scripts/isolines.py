import os
from itertools import groupby
import numpy
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas_plotters import MeshPlotter
from compas.utilities import i_to_rgb
import compas_libigl as igl

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh = Mesh.from_json(FILE)
mesh_quads_to_triangles(mesh)

key_index = mesh.key_index()

v = mesh.get_vertices_attributes('xyz')
f = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]
s = mesh.get_vertices_attribute('z')

V = numpy.array(v, dtype=numpy.float64)
F = numpy.array(f, dtype=numpy.int32)
S = numpy.array(s, dtype=numpy.float64)
N = 50

iso = igl.trimesh_isolines(V, F, S, N)

smin = min(s)
smax = max(s)
sspn = smax - smin

levels = groupby(iso.edges, key=lambda e: iso.vertices[e[0]][2])

lines = []
for s, edges in levels:
    color = i_to_rgb((s - smin) / sspn)
    for i, j in edges:
        lines.append({
            'start' : iso.vertices[i],
            'end'   : iso.vertices[j],
            'color' : color
        })


plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.draw_lines(lines)
plotter.show()
