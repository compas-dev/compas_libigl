import numpy
import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles

import compas_libigl as igl

a = Mesh.from_polyhedron(6)
mesh_quads_to_triangles(a)

b = a.copy()

for key, attr in b.vertices(True):
    attr['x'] += 0.1 * attr['x']
    attr['y'] += 0.1 * attr['y']
    attr['z'] += 0.1 * attr['z']

VA = numpy.array(a.get_vertices_attributes('xyz'), dtype=numpy.float64)
FA = numpy.array([a.face_vertices(face) for face in a.faces()], dtype=numpy.int32)

VB = numpy.array(b.get_vertices_attributes('xyz'), dtype=numpy.float64)
FB = numpy.array([b.face_vertices(face) for face in b.faces()], dtype=numpy.int32)

c = igl.mesh_union(VA, FA, VB, FB)

print(c.vertices)
print(c.faces)
