import compas
from compas.colors import Color
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Point
from compas_viewer import Viewer

import compas_libigl as igl

# ==============================================================================
# Input
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

trimesh = mesh.copy()
trimesh.quads_to_triangles()

# ==============================================================================
# Geodesic distance
# ==============================================================================

source = trimesh.vertex_sample(size=1)[0]
distance = igl.trimesh_geodistance(trimesh.to_vertices_and_faces(), source, method="exact")

# ==============================================================================
# Visualize
# ==============================================================================

cmap = ColorMap.from_color(Color.red())

viewer = Viewer(width=1600, height=900)
# viewer.view.camera.position = [1, -6, 2]
# viewer.view.camera.look_at([1, 1, 1])

viewer.scene.add(mesh, show_points=False)

for d, vertex in zip(distance, mesh.vertices()):
    point = Point(*mesh.vertex_attributes(vertex, "xyz"))
    viewer.scene.add(point, pointsize=10, pointcolor=cmap(d, min(distance), max(distance)))

viewer.scene.add(Point(*mesh.vertex_attributes(source, "xyz")), pointsize=30, pointcolor=Color.black())

viewer.show()
