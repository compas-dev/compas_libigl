# https://libigl.github.io/tutorial/#boolean-operations-on-meshes

import numpy

import compas
from compas.geometry import Box
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.datastructures import mesh_subdivide_quad

from compas_viewers.meshviewer import MeshViewer

import compas_libigl as igl

box = Box.from_width_height_depth(5.0, 3.0, 1.0)
a = Mesh.from_vertices_and_faces(box.vertices, box.faces)
a = mesh_subdivide_quad(a, k=2)
mesh_quads_to_triangles(a)

box = Box.from_width_height_depth(1.0, 5.0, 3.0)
b = Mesh.from_vertices_and_faces(box.vertices, box.faces)
b = mesh_subdivide_quad(b, k=2)
mesh_quads_to_triangles(b)

VA = numpy.array(a.get_vertices_attributes('xyz'), dtype=numpy.float64)
FA = numpy.array([a.face_vertices(face) for face in a.faces()], dtype=numpy.int32)

VB = numpy.array(b.get_vertices_attributes('xyz'), dtype=numpy.float64)
FB = numpy.array([b.face_vertices(face) for face in b.faces()], dtype=numpy.int32)

result = igl.mesh_union(VA, FA, VB, FB)

c = Mesh.from_vertices_and_faces(result.vertices, result.faces)

viewer = MeshViewer()
viewer.mesh = c
viewer.show()
