from compas.datastructures import Mesh
from compas_viewer import Viewer
from tessagon.adaptors.list_adaptor import ListAdaptor
from tessagon.types.hex_tessagon import HexTessagon
from compas.colors import Color

import compas_libigl as igl

# ==============================================================================
# Input geometry: 3D Mesh
# ==============================================================================

mesh = Mesh.from_obj("data/minimal_surface.obj")
for key, attr in mesh.vertices(True):
    y = attr["y"]
    attr["y"] = -attr["z"]
    attr["z"] = y
mesh.translate([2, 2, 0.5])

v, f = mesh.to_vertices_and_faces()


# ==============================================================================
# Input geometry: 2D Pattern creation using Tessagon library, can be other mesh.
# ==============================================================================

options = {
    "function": lambda u, v: [u, v, 0],
    "u_range": [0, 1.0],
    "v_range": [0, 1.0],
    "u_num": 16,
    "v_num": 10,
    "u_cyclic": False,
    "v_cyclic": False,
    "adaptor_class": ListAdaptor,
}
tessagon = HexTessagon(**options)
tessagon_mesh = tessagon.create_mesh()
pv = tessagon_mesh["vert_list"]
pf = tessagon_mesh["face_list"]


# ==============================================================================
# Place the pattern mesh at the center of the 3D mesh
# ==============================================================================
pattern2d = Mesh.from_vertices_and_faces(pv, pf)
c = pattern2d.aabb().corner(0)
pattern2d.translate([-c[0], -c[1], -c[2]])
pv, pf = pattern2d.to_vertices_and_faces()


# ==============================================================================
# Parametrization
# ==============================================================================

uv = igl.trimesh_lscm((v, f))

mesh_flattened = mesh.copy()
mesh_flattened.vertices_attribute("z", 0)

for i in range(mesh.number_of_vertices()):
    mesh_flattened.vertex_attributes(i, "xy", uv[i])

# ==============================================================================
# Rescale the flattened uv mesh to 1x1 scale
# ==============================================================================
box = mesh_flattened.aabb()
c = box.corner(0)
mesh_flattened.translate([-c[0], -c[1], -c[2]])
mesh_flattened.scale(1.0 / box.xsize, 1.0 / box.ysize, 1)

for i in range(mesh.number_of_vertices()):
    uv[i] = mesh_flattened.vertex_attributes(i, "xy")

# ==============================================================================
# Mapping: 3D Mesh, 2D Pattern, UV
# ==============================================================================

p_uv = igl.trimesh_simple((pv, pf))
mesh_mapped = igl.map_mesh(v, f, uv, pv, pf, p_uv)

# ==============================================================================
# Viewer
# ==============================================================================

viewer = Viewer()
viewer.scene.add(mesh, name="mesh", show_faces=False, linecolor=Color.grey(), opacity=0.2)
viewer.scene.add(pattern2d, name="pattern2d")
viewer.scene.add(mesh_flattened, name="mesh_flattened")
viewer.scene.add(mesh_mapped, name="mesh_mapped", facecolor=Color.red())
viewer.show()
