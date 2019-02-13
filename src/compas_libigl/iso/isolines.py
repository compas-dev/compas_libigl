import numpy

import compas
import compas_libigl

from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.plotters import MeshPlotter

import iso


# mesh = Mesh.from_off('../../../data/libigl-tutorial-data/beetle.off')

mesh = Mesh.from_json(compas.get('tubemesh.json'))

mesh_quads_to_triangles(mesh)

key_index = mesh.key_index()

V = numpy.array(mesh.get_vertices_attributes('xyz'), dtype=numpy.float64)
F = numpy.array([[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()], dtype=numpy.int32)

z = numpy.array(mesh.get_vertices_attribute('z'), dtype=numpy.float64)
n = 30

result = iso.isolines(V, F, z, n)

vertices = result.vertices.tolist()
edges = result.edges.tolist()

lines = []
for i, j in edges:
    lines.append({
        'start' : vertices[i],
        'end'   : vertices[j],
    })

plotter = MeshPlotter(mesh)

plotter.draw_faces()
plotter.draw_lines(lines)

plotter.show()
