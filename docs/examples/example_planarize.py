import compas
from compas.colors import Color
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas_viewer import Viewer

from compas_libigl.planarize import quadmesh_planarize

# ==============================================================================
# Input
# ==============================================================================

TOL = 0.02
MAXDEV = 0.005
KMAX = 500

mesh_not_planarized = Mesh.from_obj(compas.get("tubemesh.obj"))
mesh_not_planarized.name = "Not Planarized"

# ==============================================================================
# Planarize
# ==============================================================================

V, F = mesh_not_planarized.to_vertices_and_faces()
V2 = quadmesh_planarize((V, F), KMAX, MAXDEV)

# ==============================================================================
# Visualize
# ==============================================================================

mesh_planarized = Mesh.from_vertices_and_faces(V2, F)
mesh_planarized.name = "Planarized"

cmap = ColorMap.from_two_colors(Color.white(), Color.blue())

viewer = Viewer(width=1600, height=900)
viewer.scene.add(mesh_not_planarized, show_faces=False)
viewer.scene.add(mesh_planarized)
viewer.show()
