import numpy
import compas

from compas.datastructures import Mesh
from compas_viewers.multimeshviewer import MultiMeshViewer

import compas_libigl as igl

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

viewer = MultiMeshViewer()
viewer.meshes = [m]
viewer.show()
