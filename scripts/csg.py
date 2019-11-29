# https://libigl.github.io/tutorial/#csg-tree

import numpy

import compas

from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Cylinder
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import Vector
from compas.geometry import Point
from compas.geometry import Circle
from compas.geometry import Plane

from compas.geometry import centroid_points

from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.datastructures import mesh_flip_cycles
from compas.datastructures import mesh_subdivide_quad

from compas_viewers.meshviewer import MeshViewer

import compas_libigl as igl

# origin = Point(0.0, 0.0, 0.0)

# cube = Box.from_width_height_depth(1.0, 1.0, 1.0)
# centroid = centroid_points(cube.vertices)
# vector = Vector.from_start_end(centroid, origin)
# T = Translation(vector)
# cube.transform(T)

# a = Mesh.from_vertices_and_faces(cube.vertices, cube.faces)
# a = mesh_subdivide_quad(a, k=2)
# mesh_quads_to_triangles(a)
# mesh_flip_cycles(a)

# sphere = Sphere(origin, 0.5)

# b = Mesh.from_vertices_and_faces(* sphere.to_vertices_and_faces())
# mesh_quads_to_triangles(b)
# mesh_flip_cycles(b)

# xcyl = Cylinder(Circle(Plane(origin, Vector(1.0, 0.0, 0.0)), 0.35), 2.0)
# T = Translation([-1.0, 0.0, 0.0])
# xcyl.transform(T)

# c = Mesh.from_vertices_and_faces(* xcyl.to_vertices_and_faces())
# mesh_quads_to_triangles(c)
# mesh_flip_cycles(c)

# ycyl = Cylinder(Circle(Plane(origin, Vector(0.0, 1.0, 0.0)), 0.35), 2.0)
# T = Translation([0.0, -1.0, 0.0])
# ycyl.transform(T)

# d = Mesh.from_vertices_and_faces(* ycyl.to_vertices_and_faces())
# mesh_quads_to_triangles(d)
# mesh_flip_cycles(d)

# zcyl = Cylinder(Circle(Plane(origin, Vector(0.0, 0.0, 1.0)), 0.35), 2.0)
# T = Translation([0.0, 0.0, -1.0])
# zcyl.transform(T)

# e = Mesh.from_vertices_and_faces(* zcyl.to_vertices_and_faces())
# mesh_quads_to_triangles(e)
# mesh_flip_cycles(e)

a = Mesh.from_obj(igl.get('libigl-tutorial-data/cube.obj'))
b = Mesh.from_obj(igl.get('libigl-tutorial-data/sphere.obj'))
c = Mesh.from_obj(igl.get('libigl-tutorial-data/xcylinder.obj'))
d = Mesh.from_obj(igl.get('libigl-tutorial-data/ycylinder.obj'))
e = Mesh.from_obj(igl.get('libigl-tutorial-data/zcylinder.obj'))

VA = numpy.array(a.get_vertices_attributes('xyz'), dtype=numpy.float64)
FA = numpy.array([a.face_vertices(face) for face in a.faces()], dtype=numpy.int32)

VB = numpy.array(b.get_vertices_attributes('xyz'), dtype=numpy.float64)
FB = numpy.array([b.face_vertices(face) for face in b.faces()], dtype=numpy.int32)

VC = numpy.array(c.get_vertices_attributes('xyz'), dtype=numpy.float64)
FC = numpy.array([c.face_vertices(face) for face in c.faces()], dtype=numpy.int32)

VD = numpy.array(d.get_vertices_attributes('xyz'), dtype=numpy.float64)
FD = numpy.array([d.face_vertices(face) for face in d.faces()], dtype=numpy.int32)

VE = numpy.array(e.get_vertices_attributes('xyz'), dtype=numpy.float64)
FE = numpy.array([e.face_vertices(face) for face in e.faces()], dtype=numpy.int32)

result = igl.mesh_csgtree(VA, FA, VB, FB, VC, FC, VD, FD, VE, FE)

m = Mesh.from_vertices_and_faces(result.vertices, result.faces)

viewer = MeshViewer()
viewer.mesh = m
viewer.show()
