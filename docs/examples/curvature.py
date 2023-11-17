import compas
import compas_libigl as igl

from compas.geometry import Point, Vector, Line
from compas.datastructures import Mesh
from compas.colors import Color

from compas_view2.app import App

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

trimesh = mesh.copy()
trimesh.quads_to_triangles()

# ==============================================================================
# curvature
# ==============================================================================

curvature = igl.trimesh_gaussian_curvature(trimesh.to_vertices_and_faces())

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = App(width=1600, height=900)
viewer.view.camera.position = [1, -6, 2]
viewer.view.camera.look_at([1, 1, 1])

viewer.add(mesh, opacity=0.7)

for vertex in mesh.vertices():
    if mesh.is_vertex_on_boundary(vertex):
        continue

    point = Point(*mesh.vertex_coordinates(vertex))
    normal = Vector(*mesh.vertex_normal(vertex))
    c = curvature[vertex]
    normal.scale(10 * c)

    viewer.add(
        Line(point, point + normal),
        linecolor=(Color.red() if c > 0 else Color.blue()),
        linewidth=2,
    )

viewer.run()
