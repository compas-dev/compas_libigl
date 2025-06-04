import math
from pathlib import Path

from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Rotation
from compas.geometry import Scale
from compas_viewer import Viewer

from compas_libigl.geodistance import trimesh_geodistance_multiple
from compas_libigl.meshing import trimesh_remesh_along_isolines

# ==============================================================================
# Input geometry
# ==============================================================================
mesh = Mesh.from_off(Path(__file__).parent.parent.parent / "data" / "camelhead.off")


R = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
S = Scale.from_factors([10, 10, 10])
mesh.transform(S * R)

# Convert to triangle mesh
trimesh = mesh.copy()
trimesh.quads_to_triangles()

# ==============================================================================
# Compute geodesic distances from boundary
# ==============================================================================

# Get boundary vertices
boundary_vertices = list(trimesh.vertices_on_boundary())

# Calculate geodesic distances using multiple source points
distances = trimesh_geodistance_multiple(trimesh.to_vertices_and_faces(), boundary_vertices, method="exact")

# ==============================================================================
# Create isolines and remesh
# ==============================================================================

# Get range and create isolines
min_dist, max_dist = min(distances), max(distances)
num_isolines = 5
isovalues = [min_dist + i * (max_dist - min_dist) / num_isolines for i in range(1, num_isolines + 1)]

# Split mesh along isolines of geodesic distance
V, F, S, G = trimesh_remesh_along_isolines(trimesh.to_vertices_and_faces(), distances, isovalues)

# ==============================================================================
# Visualization
# ==============================================================================

viewer = Viewer(width=1600, height=900)

# Create separate mesh for each geodesic distance group
color_map = ColorMap.from_mpl("viridis")
for i, group_id in enumerate(sorted(set(G))):
    faces = [F[j] for j in range(len(F)) if G[j] == group_id]
    if faces:
        piece = Mesh.from_vertices_and_faces(V, faces)
        viewer.scene.add(piece, facecolor=color_map(i / (num_isolines + 1)), show_lines=False, linewidth=1, linecolor=(0.2, 0.2, 0.2))

# Highlight boundary vertices
for vertex in boundary_vertices:
    point = Point(*trimesh.vertex_attributes(vertex, "xyz"))
    viewer.scene.add(point, pointsize=20, pointcolor=(1, 0, 0))

viewer.show()
