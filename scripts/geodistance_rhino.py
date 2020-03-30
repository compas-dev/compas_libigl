import os
import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.utilities import Colormap
from compas_rhino.artists import MeshArtist
from compas.rpc import Proxy

# ==============================================================================
# RPC
# ==============================================================================

igl = Proxy('compas_libigl')

igl.stop_server()
igl.start_server()

# ==============================================================================
# Input
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh = Mesh.from_json(FILE)
mesh_quads_to_triangles(mesh)

key_index = mesh.key_index()

V = mesh.vertices_attributes('xyz')
F = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

# ==============================================================================
# Geodistance
# ==============================================================================

root = mesh.get_any_vertex()

# D = igl.trimesh_geodistance_exact(V, F, key_index[root])
D = igl.trimesh_geodistance_heat(V, F, key_index[root])

# ==============================================================================
# Visualization
# ==============================================================================

cmap = Colormap(D, 'red')

artist = MeshArtist(mesh, layer="IGL::GeoDistance")
artist.clear_layer()
artist.draw_mesh()
artist.draw_vertices(color={key: cmap(d) for key, d in zip(mesh.vertices(), D)})
artist.draw_vertexlabels(text={root: "root"}, color={0: (255, 255, 255)})
