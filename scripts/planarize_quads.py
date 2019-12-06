import numpy
import os
import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness
from compas_plotters import MeshPlotter
from compas.utilities import i_to_rgb
from compas_libigl import planarize_quads

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

MAXDEV = 0.005
KMAX = 500

mesh1 = Mesh.from_json(FILE)

vertices, faces = mesh1.to_vertices_and_faces()

V1 = numpy.array(vertices, dtype=numpy.float64)
F1 = numpy.array(faces, dtype=numpy.int32)

V2 = planarize_quads(V1, F1, KMAX, MAXDEV)

mesh2 = Mesh.from_vertices_and_faces(V2, faces)
dev2 = mesh_flatness(mesh2, maxdev=MAXDEV)

plotter = MeshPlotter(mesh2, figsize=(8, 5))
plotter.draw_faces(facecolor={fkey: i_to_rgb(dev2[fkey]) for fkey in mesh2.faces()})
plotter.show()
