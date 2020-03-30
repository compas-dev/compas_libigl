import compas
from compas.geometry import Box
from compas.geometry import Translation
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.datastructures import mesh_subdivide_quad
from compas_rhino.artists import MeshArtist
from compas.rpc import Proxy

# ==============================================================================
# RPC
# ==============================================================================

# make a proxy object for RP calls
# (this will reconnect to an existing proxy server or start a new server)
# set 'compas_libigl' as namespace for the calls

igl = Proxy('compas_libigl')

# if necessary, restart the server
# for example any of the libraries loaded by the server have changed
# or, if the existing server was started from a different environment

# igl.stop_server()
# igl.start_server()

# ==============================================================================
# Input Geometry
# ==============================================================================

# create a box mesh around the center of the world

box = Box.from_width_height_depth(5.0, 3.0, 1.0)
a = Mesh.from_shape(box)
mesh_quads_to_triangles(a)

# create a box mesh around the center of the world

box = Box.from_width_height_depth(1.0, 5.0, 3.0)
b = Mesh.from_shape(box)
mesh_quads_to_triangles(b)

# ==============================================================================
# Booleans
# ==============================================================================

# convert meshes to data

VA, FA = a.to_vertices_and_faces()
VB, FB = b.to_vertices_and_faces()

# boolean operations

VC, FC = igl.mesh_union(VA, FA, VB, FB)
c_union = Mesh.from_vertices_and_faces(VC, FC)

VC, FC = igl.mesh_intersection(VA, FA, VB, FB)
c_intersection = Mesh.from_vertices_and_faces(VC, FC)

VC, FC = igl.mesh_difference(VA, FA, VB, FB)
c_diff = Mesh.from_vertices_and_faces(VC, FC)

# ==============================================================================
# Visualization
# ==============================================================================

# the original meshes

artist = MeshArtist(a, layer="IGL::A")
artist.clear_layer()
artist.draw_mesh(color=[255, 0, 0])

artist = MeshArtist(b, layer="IGL::B")
artist.clear_layer()
artist.draw_mesh(color=[0, 0, 255])

# the boolean meshes

c_union.transform(Translation([7.5, 0, 0]))
c_intersection.transform(Translation([15, 0, 0]))
c_diff.transform(Translation([22.5, 0, 0]))

artist = MeshArtist(c_union, layer="IGL::Union")
artist.clear_layer()
artist.draw_mesh(color=[225, 0, 255])

artist = MeshArtist(c_intersection, layer="IGL::Intersection")
artist.clear_layer()
artist.draw_mesh(color=[0, 255, 0])

artist = MeshArtist(c_diff, layer="IGL::Diff")
artist.clear_layer()
artist.draw_mesh(color=[0, 255, 0])
