import os
import compas_rhino
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

tri = mesh.copy()
mesh_quads_to_triangles(tri)

M = tri.to_vertices_and_faces()
source = tri.get_any_vertex()

# ==============================================================================
# Geodistance
# ==============================================================================

D = igl.trimesh_geodistance(M, source)

# ==============================================================================
# Visualization
# ==============================================================================

Dmin = min(D)
Dmax = max(D)

cmap = Colormap(D, 'red')

artist = MeshArtist(mesh, layer="IGL::GeoDistance")
artist.clear_layer()
artist.draw_mesh()

spheres = []
for key, d in zip(mesh.vertices(), D):
    radius = 0.5 * (d - Dmin) / (Dmax - Dmin)
    spheres.append({
        'pos': mesh.vertex_coordinates(key),
        'radius': radius if key != source else 0.5,
        'color': cmap(d) if key != source else (255, 255, 255)
    })

compas_rhino.draw_spheres(spheres, layer=artist.layer, clear=False, redraw=True)
