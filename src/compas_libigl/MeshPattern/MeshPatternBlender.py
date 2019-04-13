import numpy
import os
import sys
import compas
from compas.datastructures import Mesh
from compas.plotters import MeshPlotter

file_dir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(file_dir)
sys.path.append(file_dir + "/../../../lib/MeshPattern")

from MeshPattern import iglMesh

bunnyOBJ = Mesh.from_ply(compas.get('bunny.ply'))
vertices, faces = bunnyOBJ.to_vertices_and_faces()
mesh = iglMesh()
mesh.loadMesh(vertices, faces)
mesh.make_flat()

compasMesh = Mesh.from_vertices_and_faces(vertices, faces) 
