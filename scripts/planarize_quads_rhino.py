import os
import compas

from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness
from compas.utilities import i_to_rgb

from compas_rhino.artists import MeshArtist

from compas.rpc import Proxy

igl = Proxy('compas_libigl')
# igl.stop_server()
# igl.start_server()

planaryze_quads = igl.planarize_quads_proxy

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh1 = Mesh.from_json(FILE)

V1, F1 = mesh1.to_vertices_and_faces()
V2 = planaryze_quads(V1, F1, 500, 0.005)

mesh2 = Mesh.from_vertices_and_faces(V2, F1)
dev2 = mesh_flatness(mesh2, maxdev=0.005)

artist = MeshArtist(mesh2, layer="IGL::PlanarizeQuads")
artist.clear_layer()

artist.draw_faces(color={fkey: i_to_rgb(dev2[fkey]) for fkey in mesh2.faces()})
