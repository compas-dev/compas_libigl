import numpy
import os
import compas

from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness

from compas_plotters import MeshPlotter
from compas.utilities import i_to_rgb
import project2D
import sys


sys.append()

mesh1 = Mesh.from_ply(compas.get('bunny.ply'))

vertices, faces = mesh1.to_vertices_and_faces()
faces.append([1,0,0,1])
project2D.loadMesh(vertices, faces)
