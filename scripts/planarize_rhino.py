import os
import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness
from compas.utilities import i_to_rgb
from compas_rhino.artists import MeshArtist
from compas.rpc import Proxy

maxdev = 0.005
kmax = 500

igl = Proxy('compas_libigl')
# igl.stop_server()
# igl.start_server()

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh = Mesh.from_json(FILE)

vertices, faces = mesh.to_vertices_and_faces()
vertices = igl.planarize_quads(vertices, faces, kmax, maxdev)

mesh = Mesh.from_vertices_and_faces(vertices, faces)

dev = mesh_flatness(mesh, maxdev=maxdev)

artist = MeshArtist(mesh, layer="IGL::PlanarizeQuads")
artist.clear_layer()
artist.draw_faces(color={fkey: i_to_rgb(dev[fkey]) for fkey in mesh.faces()})
