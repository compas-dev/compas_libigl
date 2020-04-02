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

tri = mesh.copy()
mesh_quads_to_triangles(tri)

# ==============================================================================
# Isolines
# ==============================================================================

M = tri.to_vertices_and_faces()
S = mesh.vertices_attribute('z')

vertices, edges = igl.trimesh_isolines(M, S, 50)

levels = groupby(sorted(edges, key=lambda edge: vertices[edge[0]][2]), key=lambda edge: vertices[edge[0]][2])

# ==============================================================================
# Visualisation
# ==============================================================================

smin = min(S)
smax = max(S)

lines = []
for value, edges in levels:
    for i, j in edges:
        lines.append({
            'start' : vertices[i],
            'end'   : vertices[j],
            'color' : i_to_rgb((value - smin) / (smax - smin))
        })

artist = MeshArtist(mesh, layer="IGL::Isolines")
artist.clear_layer()
artist.draw_faces()

compas_rhino.draw_lines(lines, layer=artist.layer, clear=False)
