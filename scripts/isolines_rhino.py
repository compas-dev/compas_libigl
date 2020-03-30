import os
import compas_rhino
from itertools import groupby
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.utilities import i_to_rgb
from compas_rhino.artists import MeshArtist
from compas.rpc import Proxy

# ==============================================================================
# RPC
# ==============================================================================

igl = Proxy('compas_libigl')
igl.stop_server()
igl.start_server()

# ==============================================================================
# Input geometry
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh = Mesh.from_json(FILE)
mesh_quads_to_triangles(mesh)

# ==============================================================================
# Isolines
# ==============================================================================

key_index = mesh.key_index()

V = mesh.vertices_attributes('xyz')
F = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]
S = mesh.vertices_attribute('z')
N = 50

vertices, levels = igl.trimesh_isolines(V, F, S, N)

# ==============================================================================
# Visualisation
# ==============================================================================

smin = min(S)
smax = max(S)

lines = []
for scalar, edges in levels:
    for i, j in edges:
        lines.append({
            'start' : vertices[i],
            'end'   : vertices[j],
            'color' : i_to_rgb((scalar - smin) / (smax - smin))
        })

artist = MeshArtist(mesh, layer="IGL::Isolines")
artist.draw_faces()

compas_rhino.draw_lines(lines, layer=artist.layer, clear=False)
