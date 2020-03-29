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

HERE = os.path.dirname(__file__)
FILE1 = os.path.join(HERE, '..', 'data', 'tubemesh.json')
FILE2 = os.path.join(HERE, '..', 'data', 'tubemesh.off')

mesh = Mesh.from_json(FILE1)
mesh.to_off(FILE2)

mesh = Mesh.from_off(FILE2)

mesh.data = igl.planarize_mesh_proxy(mesh.data)
dev = mesh_flatness(mesh, maxdev=maxdev)

artist = MeshArtist(mesh, layer="IGL::PlanarizeMesh")
artist.clear_layer()
artist.draw_faces(color={fkey: i_to_rgb(dev[fkey]) for fkey in mesh.faces()})
