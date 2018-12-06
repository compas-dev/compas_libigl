import numpy

import compas
from compas.datastructures import Mesh
from compas.plotters import MeshPlotter
from compas.utilities import i_to_rgb
from compas.geometry import mesh_flatness

import planarize


m1 = Mesh.from_json(compas.get('tubemesh.json'))

v1, faces = m1.to_vertices_and_faces()

v2 = planarize.planarize(numpy.array(v1), numpy.array(faces))

print(type(v2))

m2 = Mesh.from_vertices_and_faces(v2, faces)

d1 = mesh_flatness(m1, maxdev=0.02)
d2 = mesh_flatness(m2, maxdev=0.02)

plotter = MeshPlotter(m2)

plotter.draw_faces(facecolor={fkey: i_to_rgb(d2[fkey]) for fkey in m2.faces()})

plotter.show()
