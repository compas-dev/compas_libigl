import compas
from compas.colors import Color
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Point
from compas_viewer import Viewer

from compas_libigl.geodistance import trimesh_geodistance_multiple

# ==============================================================================
# Input
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

trimesh = mesh.copy()
trimesh.quads_to_triangles()

# ==============================================================================
# Get boundary vertices as source points
# ==============================================================================

boundary_vertices = list(trimesh.vertices_on_boundary())

# ==============================================================================
# Compute geodesic distances from all boundary vertices at once
# ==============================================================================

# Calculate geodesic distances using the new multiple source points function
distances = trimesh_geodistance_multiple(trimesh.to_vertices_and_faces(), boundary_vertices, method="exact")

# ==============================================================================
# Visualization
# ==============================================================================

viewer = Viewer(width=1600, height=900)

# Add base mesh
viewer.scene.add(mesh, show_points=False, show_lines=True, linewidth=1)

# Create color gradient
cmap = ColorMap.from_mpl("viridis")

# Visualize distances as colored points
for vertex, dist in zip(mesh.vertices(), distances):
    point = Point(*mesh.vertex_attributes(vertex, "xyz"))
    viewer.scene.add(point, pointsize=10, pointcolor=cmap(dist, min(distances), max(distances)))

# Highlight boundary vertices
for vertex in boundary_vertices:
    point = Point(*mesh.vertex_attributes(vertex, "xyz"))
    viewer.scene.add(point, pointsize=20, pointcolor=Color.black())

viewer.show()
