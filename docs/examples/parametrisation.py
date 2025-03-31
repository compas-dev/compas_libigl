import compas_libigl as igl
from compas.datastructures import Mesh
from compas.geometry import Scale
from compas.geometry import Translation
from compas_viewer import Viewer

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_off(igl.get("camelhead.off"))

mesh_lscm = mesh.copy()
mesh_lscm.vertices_attribute("z", 0)

# ==============================================================================
# Least-squares conformal map
# ==============================================================================

lscm_uv = igl.trimesh_lscm(mesh.to_vertices_and_faces())

for index, key in enumerate(mesh.vertices()):
    mesh_lscm.vertex_attributes(key, "xy", lscm_uv[index])

mesh_lscm.transform(Scale.from_factors([3, 3, 3]))

# ==============================================================================
# Visualization
# ==============================================================================

X = Translation.from_vector([2.5, 1.5, 0]) * Scale.from_factors([3, 3, 3])

mesh.transform(X)

viewer = Viewer()
viewer.scene.add(mesh, show_points=False)
viewer.scene.add(mesh_lscm, show_points=False)
viewer.show()
