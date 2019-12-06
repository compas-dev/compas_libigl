import compas
from compas.geometry import Box
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.datastructures import mesh_subdivide_quad
from compas.rpc import Proxy
from compas_rhino.artists import MeshArtist


igl = Proxy('compas_libigl')
# igl.stop_server()
# igl.start_server()
mesh_union = igl.mesh_union_proxy

box = Box.from_width_height_depth(5.0, 3.0, 1.0)
a = Mesh.from_shape(box)
# a = mesh_subdivide_quad(a, k=2)
mesh_quads_to_triangles(a)

box = Box.from_width_height_depth(1.0, 5.0, 3.0)
b = Mesh.from_shape(box)
# b = mesh_subdivide_quad(b, k=2)
mesh_quads_to_triangles(b)

c = mesh_union(a, b)

artist = MeshArtist(c, layer="IGL::MeshUnion")
artist.clear_layer()
artist.draw_mesh()
