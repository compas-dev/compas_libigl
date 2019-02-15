from itertools import groupby

import numpy

import compas

from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.plotters import MeshPlotter
from compas.utilities import i_to_rgb

import iso


mesh = Mesh.from_json(compas.get('tubemesh.json'))

mesh_quads_to_triangles(mesh)

key_index = mesh.key_index()

v = mesh.get_vertices_attributes('xyz')
f = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]
z = mesh.get_vertices_attribute('z')

V = numpy.array(v, dtype=numpy.float64)
F = numpy.array(f, dtype=numpy.int32)
Z = numpy.array(z, dtype=numpy.float64)
N = 30

result = iso.isolines(V, F, Z, N)

vertices = result.vertices.tolist()
edges = result.edges.tolist()

zmin = min(vertices, key=lambda v: v[2])[2]
zmax = max(vertices, key=lambda v: v[2])[2]
zspn = zmax - zmin

edges = sorted(edges, key=lambda e: vertices[e[0]][2])
edges = groupby(edges, key=lambda e: vertices[e[0]][2])

lines = []
for z, group in edges:
    for i, j in group:
        a = vertices[i]
        b = vertices[j]

        color = i_to_rgb((z - zmin) / zspn)

        lines.append({
            'start' : a,
            'end'   : b,
            'color' : color
        })

plotter = MeshPlotter(mesh)
plotter.draw_faces()
plotter.draw_lines(lines)
plotter.save('tubemesh_iso.png')
