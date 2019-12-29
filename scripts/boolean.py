# https://libigl.github.io/tutorial/#boolean-operations-on-meshes

import numpy
import compas
from compas.geometry import Box
from compas.geometry import Translation
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.datastructures import mesh_subdivide_quad
from compas.datastructures import mesh_transform
from compas_viewers.multimeshviewer import MultiMeshViewer
from compas_viewers.multimeshviewer import MeshObject
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

# create the booleans between A and B
booleans = [igl.mesh_union, igl.mesh_difference, igl.mesh_intersection]
results = [boolean(VA, FA, VB, FB) for boolean in booleans]

# create meshes
meshes = [Mesh.from_vertices_and_faces(r.vertices, r.faces) for r in results]

# visualize the result
viewer = MultiMeshViewer()

# translate meshes 5.0 each on the Y-axis
pos = 0.0
spacing = 5.0
for m in meshes:
	mesh_transform(m, Translation([0.0, pos, 0.0]))
	pos += spacing

# create mesh objects for visualization
viewer.meshes = [MeshObject(m) for m in meshes]
viewer.show()
