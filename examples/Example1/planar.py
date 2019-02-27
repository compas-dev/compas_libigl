import os
import bpy
import sys
filepath = bpy.data.filepath
directory = os.path.dirname(filepath)
sys.path.append(directory)

import numpy
import compas
import compas.datastructures
from compas.datastructures import Mesh
from compas.plotters import MeshPlotter
from compas.utilities import i_to_rgb
import planarize

mesh1 = Mesh.from_json('tubemesh.json')

vertices, faces = mesh1.to_vertices_and_faces()

V1 = numpy.array(vertices, dtype=numpy.float64)
F1 = numpy.array(faces, dtype=numpy.int32)
V2 = planarize.planarize(V1, F1)

#mesh2 = Mesh.from_vertices_and_faces(V2, faces)

#dev2 = mcompas.datastructures.esh_flatness(mesh2, maxdev=0.02)

#plotter = MeshPlotter(mesh2)
#plotter.draw_faces(facecolor={fkey: i_to_rgb(dev2[fkey]) for fkey in mesh2.faces()})
#plotter.show()