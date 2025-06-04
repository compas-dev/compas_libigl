import math
from pathlib import Path

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Plane
from compas.geometry import Rotation
from compas.geometry import Scale
from compas_viewer import Viewer

from compas_libigl.meshing import trimesh_remesh_along_isoline

# Load and transform mesh
mesh = Mesh.from_off(Path(__file__).parent.parent.parent / "data" / "beetle.off")
R = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
S = Scale.from_factors([10, 10, 10])
mesh.transform(S * R)

# Calculate signed distances to plane
plane = Plane([0, 0, 0], [0, 1, 1])
distances = [plane.normal.dot(plane.point - mesh.vertex_coordinates(v)) for v in mesh.vertices()]

# Split mesh along plane
V, F, L = trimesh_remesh_along_isoline(mesh.to_vertices_and_faces(), distances, 0)

# Create meshes for parts below and above plane
below = Mesh.from_vertices_and_faces(V, [F[i] for i, l in enumerate(L) if l == 0])
above = Mesh.from_vertices_and_faces(V, [F[i] for i, l in enumerate(L) if l == 1])

# Visualize
viewer = Viewer()
viewer.scene.add(below, facecolor=Color.red(), show_lines=False)
viewer.scene.add(above, facecolor=Color.blue(), show_lines=False)
viewer.show()
