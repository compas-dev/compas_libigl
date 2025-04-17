from compas.datastructures import Mesh
from tessagon.types.hex_tessagon import HexTessagon
from tessagon.adaptors.list_adaptor import ListAdaptor
from compas_viewer import Viewer
import compas_libigl as igl
from compas_libigl import _mapping
import numpy as np

viewer = Viewer()

# ==============================================================================
# Input geometry: 3D Mesh
# ==============================================================================

# Load the mesh
mesh = Mesh.from_obj("data/minimal_surface.obj")
for key, attr in mesh.vertices(True):
    y = attr["y"]
    attr["y"] = -attr["z"]
    attr["z"] = y

v, f = mesh.to_vertices_and_faces()

viewer.scene.add(mesh, name="mesh")

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
# Parametrization: choose between simple, lcsm and harmonic methods.
# ==============================================================================

uv = igl.trimesh_simple((v, f))
# uv = igl.trimesh_lscm((v, f))
# uv = igl.trimesh_harmonic((v, f))

mesh_flattened = mesh.copy()
mesh_flattened.vertices_attribute("z", 0)

for i in range(mesh.number_of_vertices()):
    mesh_flattened.vertex_attributes(i, "xy", uv[i])

viewer.scene.add(mesh_flattened, name="mesh_flattened")

# ==============================================================================
# Mapping: 3D Mesh, 2D Pattern, UV
# Eigen::Ref<const compas::RowMatrixXd> v, 
# Eigen::Ref<const compas::RowMatrixXi> f, 
# Eigen::Ref<const compas::RowMatrixXd> uv,
# Eigen::Ref<compas::RowMatrixXd>  pattern_v, 
# Eigen::Ref<const compas::RowMatrixXi> pattern_f, 
# Eigen::Ref<const compas::RowMatrixXd> pattern_uv, 
# std::vector<std::vector<int>>& pattern_polygonal_faces
# ==============================================================================

v_numpy = np.array(v, dtype=np.float64)
f_numpy = np.array(f, dtype=np.int32)
uv_numpy = np.array(uv, dtype=np.float64)
pattern_v_numpy = np.array(pv, dtype=np.float64)
pattern_f_numpy = np.array(pf, dtype=np.int32)
pattern_uv = igl.trimesh_simple((pv, pf))
pattern_uv_numpy = np.array(pattern_uv, dtype=np.float64)
pattern_polygonal_faces = pf

print("Before mapping")
print(pattern_v_numpy[0])
_mapping.mapMesh3D_AABB(v_numpy, f_numpy, uv_numpy, pattern_v_numpy, pattern_f_numpy, pattern_uv_numpy, pattern_polygonal_faces)
print("After mapping")

for i in range(100):
    print(pattern_v_numpy[i])

mapped_mesh = Mesh.from_vertices_and_faces(pattern_v_numpy, pattern_f_numpy)
viewer.scene.add(mapped_mesh, name="mapped_mesh")



# ==============================================================================
# Viewer
# ==============================================================================


viewer.show()