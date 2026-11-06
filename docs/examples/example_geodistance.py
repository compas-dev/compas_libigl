import compas
from compas.colors import Color
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas_viewer import Viewer

from compas_libigl.geodistance import trimesh_geodistance

# ==============================================================================
# Input
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

triangle_mesh = mesh.triangulated()

# ==============================================================================
# Geodesic distance
# ==============================================================================

source = mesh.vertex_sample(size=1)[0]
distance = trimesh_geodistance(triangle_mesh.to_vertices_and_faces(), source, method="exact")

# ==============================================================================
# Visualize
# ==============================================================================

cmap = ColorMap.from_color(Color.red())

viewer = Viewer(width=1600, height=900)

viewer.scene.add(mesh, show_points=False)

for d, vertex in zip(distance, mesh.vertices()):
    point = mesh.vertex_point(vertex)
    viewer.scene.add(point, pointsize=10, pointcolor=cmap(d, min(distance), max(distance)))

viewer.scene.add(mesh.vertex_point(source), pointsize=30, pointcolor=Color.black())

viewer.show()
