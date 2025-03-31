import compas
import compas_libigl as igl
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector
from compas_viewer import Viewer

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

viewer = Viewer(width=1600, height=900)
# viewer.view.camera.position = [1, -6, 2]
# viewer.view.camera.look_at([1, 1, 1])

viewer.scene.add(mesh, opacity=0.7, show_points=False)

for vertex in mesh.vertices():
    if mesh.is_vertex_on_boundary(vertex):
        continue

    point = Point(*mesh.vertex_coordinates(vertex))
    normal = Vector(*mesh.vertex_normal(vertex))
    c = curvature[vertex]
    normal.scale(10 * c)

    viewer.scene.add(
        Line(point, point + normal),
        linecolor=(Color.red() if c > 0 else Color.blue()),
        linewidth=2,
    )

viewer.show()
