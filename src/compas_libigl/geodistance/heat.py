import numpy
import os
import compas
import compas_libigl

from compas.datastructures import Mesh

import geodistance as g

dir_path = os.path.dirname(os.path.realpath(__file__))
mesh = Mesh.from_off(dir_path + '/bunny.off')

V = numpy.array(mesh.get_vertices_attributes('xyz'))
F = numpy.array([mesh.face_vertices(fkey) for fkey in mesh.faces()])

d = g.exact(V, F, 0)

print(d)
