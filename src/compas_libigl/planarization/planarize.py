import numpy

import compas

from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness

from compas.plotters import MeshPlotter
from compas.utilities import i_to_rgb

import planarize


m1 = Mesh.from_json(compas.get('tubemesh.json'))

v1, f = m1.to_vertices_and_faces()

V1 = numpy.array(v1, dtype=numpy.float64)
F = numpy.array(f, dtype=numpy.int32)

V2 = planarize.planarize(V1, F)

m2 = Mesh.from_vertices_and_faces(V2, f)

d1 = mesh_flatness(m1, maxdev=0.02)
d2 = mesh_flatness(m2, maxdev=0.02)

plotter = MeshPlotter(m2)

plotter.draw_faces(facecolor={fkey: i_to_rgb(d2[fkey]) for fkey in m2.faces()})

plotter.show()
