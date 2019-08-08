import numpy as np
import os
import sys
import compas
from compas.datastructures import Mesh
from compas.plotters import MeshPlotter
from compas_blender.utilities import draw_mesh
from compas.geometry import *

file_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(file_dir)
sys.path.append(file_dir + "/../../../lib/MeshPattern")
sys.path.append(os.path.dirname(file_dir) + "/../../../lib/MeshPattern")

import MeshPattern
from MeshPattern import *

from tessagon.types.hex_tessagon import HexTessagon
from tessagon.adaptors.list_adaptor import ListAdaptor

def drawMeshVF(v, f):
	draw_mesh(v, None, f)

def drawMeshVEF(v, e, f):
	draw_mesh(v, e, f)

def create2DPattern():
	#Create 2D pattern in [-1, 1]x[-1,1]
	options = {
    	'function': lambda u, v: [u, v, 0],
    	'u_range': [0, 1.0],
    	'v_range': [0, 1.0],
    	'u_num': 16,
    	'v_num': 10,
    	'u_cyclic': False,
    	'v_cyclic': False,
    	'adaptor_class' : ListAdaptor
  	}
	tessagon = HexTessagon(**options)
	vertices = tessagon.create_mesh()['vert_list']
	faces = tessagon.create_mesh()['face_list']
	mesh = iglMesh()
	mesh.loadMesh(vertices, faces)
	return mesh


if __name__ == "__main__":
	#create2DPattern()
	
	#Use compas to read obj file 
	surfaceOBJ = Mesh.from_obj(compas.get('minimal_surface.obj'))
	
	vertices, faces = surfaceOBJ.to_vertices_and_faces()
	for key, attr in surfaceOBJ.vertices(True):
		attr['x'] = vertices[key][0]
		attr['y'] = -vertices[key][2]
		attr['z'] = vertices[key][1]

	vertices, faces = surfaceOBJ.to_vertices_and_faces()

	#Create a C++ iglMesh class and enter input OBJ mesh
	mesh = iglMesh()
	mesh.loadMesh(vertices, faces)
	mesh.paramertization_lscm()
	vertices = mesh.getUVs()
	faces = mesh.getFaces()
	#drawMeshVF(vertices, faces)
	
	#Process mesh
	pattern2D = create2DPattern()
	mesh.paramertization_simple()
    
	mesh.mapMesh3D_AABB(pattern2D)
	#Return proccessd mesh and get its vertices and faces
	vertices = pattern2D.getVertices()
	faces = pattern2D.getFaces()
	compasMesh = Mesh.from_vertices_and_faces(vertices, faces)
	#draw_mesh(vertices, list(compasMesh.edges()), faces)