import numpy

import compas
import compas_libigl

from compas.datastructures import Mesh

import geodistance as g

mesh = Mesh.from_off('../../../data/libigl-tutorial-data/bunny.off')

V = numpy.array(mesh.get_vertices_attributes('xyz'))
F = numpy.array([mesh.face_vertices(fkey) for fkey in mesh.faces()])

d = g.exact(V, F, 0)

print(d)
