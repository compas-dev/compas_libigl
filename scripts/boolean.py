# https://libigl.github.io/tutorial/#boolean-operations-on-meshes

import numpy
import compas
from compas.geometry import Box
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.datastructures import mesh_subdivide_quad
from compas_viewers.meshviewer import MeshViewer
import compas_libigl as igl

# note: provide interface to other boolean operations

# create a box mesh around the center of the world
# -2.5 =< x =< +2.5
# -1.5 =< y =< +1.5
# -0.5 =< z =< +0.5

box = Box.from_width_height_depth(5.0, 3.0, 1.0)
a = Mesh.from_shape(box)
# a = mesh_subdivide_quad(a, k=2)
mesh_quads_to_triangles(a)

# create a box mesh around the center of the world
# -0.5 =< x =< +0.5
# -2.5 =< y =< +2.5
# -1.5 =< z =< +1.5

box = Box.from_width_height_depth(1.0, 5.0, 3.0)
b = Mesh.from_shape(box)
# b = mesh_subdivide_quad(b, k=2)
mesh_quads_to_triangles(b)

# convert mesh `a` to numpy arrays with vertices and faces
# note: replace this by functionality of `compas.interop`

VA = numpy.array(a.get_vertices_attributes('xyz'), dtype=numpy.float64)
FA = numpy.array([a.face_vertices(face) for face in a.faces()], dtype=numpy.int32)

# convert mesh `b` to numpy arrays with vertices and faces
# note: replace this by functionality of `compas.interop`

VB = numpy.array(b.get_vertices_attributes('xyz'), dtype=numpy.float64)
FB = numpy.array([b.face_vertices(face) for face in b.faces()], dtype=numpy.int32)

# create the union of a and b

result = igl.mesh_union(VA, FA, VB, FB)

# construct a new COMPAS mesh

c = Mesh.from_vertices_and_faces(result.vertices, result.faces)

# visualize the result

viewer = MeshViewer()
viewer.mesh = c
viewer.show()
