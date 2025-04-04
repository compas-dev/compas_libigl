import math

from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Rotation
from compas.geometry import Scale
from compas_viewer import Viewer

import compas_libigl as igl

# Load mesh
mesh = Mesh.from_off(igl.get_beetle())
R = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
S = Scale.from_factors([10, 10, 10])
mesh.transform(S * R)

# Get z-coordinates as scalar field
scalar_values = mesh.vertices_attribute("z")
min_val, max_val = min(scalar_values), max(scalar_values)

# Create 4 isolines
num_isolines = 4
isovalues = [min_val + i * (max_val - min_val) / num_isolines for i in range(1, num_isolines + 1)]

# Split mesh along isolines
V, F, S, G = igl.trimesh_remesh_along_isolines(mesh.to_vertices_and_faces(), scalar_values, isovalues)

# Visualize each piece in a different color
color_map = ColorMap.from_mpl("viridis")
viewer = Viewer()

# Create separate mesh for each group
for i, group_id in enumerate(set(G)):
    faces = [F[j] for j in range(len(F)) if G[j] == group_id]
    if faces:
        piece = Mesh.from_vertices_and_faces(V, faces)
        viewer.scene.add(piece, facecolor=color_map(i / (num_isolines + 1)), show_lines=False)

viewer.show()
