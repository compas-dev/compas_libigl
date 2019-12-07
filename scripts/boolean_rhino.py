import compas
from compas.geometry import Box
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.datastructures import mesh_subdivide_quad
from compas.rpc import Proxy
from compas_rhino.artists import MeshArtist

# make a proxy object for RP calls
# (this will reconnect to an existing proxy server or start a new server)
# set 'compas_libigl' as namespace for the calls

igl = Proxy('compas_libigl')

# if necessary, restart the server
# for example any of the libraries loaded by the server have changed
# or, if the existing server was started from a different environment

# note: this should be replaced by `restart_server`
# igl.stop_server()
# igl.start_server()

# assign a proxy for the original function to `mesh_union`

mesh_union = igl.mesh_union_proxy

# create a box mesh around the center of the world
# -2.5 =< x =< +2.5
# -1.5 =< y =< +1.5
# -0.5 =< z =< +0.5

box = Box.from_width_height_depth(5.0, 3.0, 1.0)
a = Mesh.from_shape(box)
# a = mesh_subdivide_quad(a, k=2)
mesh_quads_to_triangles(a)

# create a box mesh around the center of the world
# -0.5 =< x =< +0.5
# -2.5 =< y =< +2.5
# -1.5 =< z =< +1.5

box = Box.from_width_height_depth(1.0, 5.0, 3.0)
b = Mesh.from_shape(box)
# b = mesh_subdivide_quad(b, k=2)
mesh_quads_to_triangles(b)

# create the union of a and b

c = mesh_union(a, b)

# draw the result

artist = MeshArtist(c, layer="IGL::MeshUnion")
artist.clear_layer()
artist.draw_mesh()
