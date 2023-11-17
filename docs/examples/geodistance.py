import compas
import compas_libigl as igl
from compas.geometry import Point
from compas.datastructures import Mesh
from compas.colors import Color, ColorMap
from compas_view2.app import App

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
distance = igl.trimesh_geodistance(
    trimesh.to_vertices_and_faces(), source, method="heat"
)

# ==============================================================================
# Visualize
# ==============================================================================

cmap = ColorMap.from_color(Color.red())

viewer = App(width=1600, height=900)
viewer.view.camera.position = [1, -6, 2]
viewer.view.camera.look_at([1, 1, 1])

viewer.add(mesh)

for d, vertex in zip(distance, mesh.vertices()):
    point = Point(*mesh.vertex_attributes(vertex, "xyz"))
    viewer.add(point, pointsize=30, pointcolor=cmap(d, min(distance), max(distance)))

viewer.run()
