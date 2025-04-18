from compas.colors import Color
from compas.datastructures import Mesh
from compas_viewer import Viewer
from compas_viewer.config import Config
from tessagon.adaptors.list_adaptor import ListAdaptor
from tessagon.types.hex_tessagon import HexTessagon

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
    "u_range": [-0.255, 1.33],
    "v_range": [-0.34, 1.33],
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
# Mapping: 3D Mesh, 2D Pattern, UV
# ==============================================================================

mv, mf = igl.map_mesh((v, f), (pv, pf))
mesh_mapped = Mesh.from_vertices_and_faces(mv, mf)

# ==============================================================================
# Viewer
# ==============================================================================

config = Config()
config.camera.target = [2, 2, 0.25]
config.camera.position = [5, 2, 1.5]

viewer = Viewer(config=config)
viewer.scene.add(mesh, name="mesh", show_faces=False, linecolor=Color.grey(), opacity=0.2)
viewer.scene.add(Mesh.from_vertices_and_faces(pv, pf), name="pattern2d")
viewer.scene.add(mesh_mapped, name="mesh_mapped", facecolor=Color.red())

# To see where the pattern is mapped:
uv = igl.trimesh_lsc_mapping((v, f))
mesh_flattened = mesh.copy()
for i in range(mesh.number_of_vertices()):
    mesh_flattened.vertex_attributes(i, "xyz", [uv[i][0], uv[i][1], 0])

viewer.scene.add(mesh_flattened, name="mesh_flattened")
viewer.show()
