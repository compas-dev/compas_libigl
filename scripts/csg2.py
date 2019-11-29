from math import sqrt

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
from compas.datastructures import mesh_subdivide_quad

from compas_viewers.multimeshviewer import MultiMeshViewer
from compas_viewers.multimeshviewer.model import MeshObject

import compas_libigl as igl

origin = Point(0.0, 0.0, 0.0)

cube = Box.from_width_height_depth(1.0, 1.0, 1.0)
sphere = Sphere(origin, 0.95 * sqrt(0.5 ** 2 + 0.5 ** 2))

xcyl = Cylinder(Circle(Plane(origin, Vector(1.0, 0.0, 0.0)), 0.35), 2.0)
ycyl = Cylinder(Circle(Plane(origin, Vector(0.0, 1.0, 0.0)), 0.35), 2.0)
zcyl = Cylinder(Circle(Plane(origin, Vector(0.0, 0.0, 1.0)), 0.35), 2.0)

a = Mesh.from_vertices_and_faces(cube.vertices, cube.faces)
a = mesh_subdivide_quad(a, k=3)
b = Mesh.from_vertices_and_faces(* sphere.to_vertices_and_faces(u=30, v=30))
c = Mesh.from_vertices_and_faces(* xcyl.to_vertices_and_faces(u=30))
d = Mesh.from_vertices_and_faces(* ycyl.to_vertices_and_faces(u=30))
e = Mesh.from_vertices_and_faces(* zcyl.to_vertices_and_faces(u=30))

mesh_quads_to_triangles(a)
mesh_quads_to_triangles(b)
mesh_quads_to_triangles(c)
mesh_quads_to_triangles(d)
mesh_quads_to_triangles(e)

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

viewer = MultiMeshViewer()
# viewer.meshes = [MeshObject(a, '#ff0000'), MeshObject(b, '#00ff00'), MeshObject(c, '#0000ff'), MeshObject(d, '#0000ff'), MeshObject(e, '#0000ff')]
viewer.meshes = [MeshObject(m, '#cccccc')]
viewer.show()
