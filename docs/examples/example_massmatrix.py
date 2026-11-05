import compas
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import FaceTriangulation
from compas_viewer import Viewer

from compas_libigl.massmatrix import trimesh_massmatrix

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

tessellation = mesh.triangulated(FaceTriangulation())

# ==============================================================================
# Mass matrix
# ==============================================================================

mass = trimesh_massmatrix(tessellation.to_vertices_and_triangles())

# ==============================================================================
# Visualisation
# ==============================================================================

cmap = ColorMap.from_rgb()

minval = min(mass)
maxval = max(mass)

viewer = Viewer(width=1600, height=900)
# viewer.view.camera.position = [1, -6, 2]
# viewer.view.camera.look_at([1, 1, 1])

viewer.scene.add(mesh, show_points=False)

for m, vertex in zip(mass, mesh.vertices()):
    point = mesh.vertex_point(vertex)
    viewer.scene.add(point, pointsize=30, pointcolor=cmap(m, minval, maxval))

viewer.show()
