import compas
import compas_libigl as igl
from compas.colors import Color
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness
from compas_viewer import Viewer

# ==============================================================================
# Input
# ==============================================================================

TOL = 0.02
MAXDEV = 0.005
KMAX = 500

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

# ==============================================================================
# Planarize
# ==============================================================================

V, F = mesh.to_vertices_and_faces()
V2 = igl.quadmesh_planarize((V, F), KMAX, MAXDEV)

# ==============================================================================
# Visualize
# ==============================================================================

mesh = Mesh.from_vertices_and_faces(V2, F)
dev = mesh_flatness(mesh, maxdev=TOL)

cmap = ColorMap.from_two_colors(Color.white(), Color.blue())

viewer = Viewer(width=1600, height=900)
# viewer.view.camera.position = [1, -6, 2]
# viewer.view.camera.look_at([1, 1, 1])

viewer.scene.add(
    mesh,
    facecolor={face: (cmap(dev[face]) if dev[face] <= 1.0 else Color.red()) for face in mesh.faces()},
    show_points=False,
)
viewer.show()
