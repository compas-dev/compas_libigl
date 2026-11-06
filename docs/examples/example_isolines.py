import math
from pathlib import Path

from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Rotation
from compas.geometry import Scale
from compas_viewer import Viewer

from compas_libigl.isolines import trimesh_isolines

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_off(Path(__file__).parent.parent.parent / "data" / "beetle.off")

Rx = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
Rz = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))
S = Scale.from_factors([10, 10, 10])

mesh.transform(S * Rz * Rx)

# ==============================================================================
# Isolines
# ==============================================================================

scalars = mesh.vertices_attribute("z")

num_isolines = 100
triangle_mesh = mesh.triangulated()
vertices, edges = trimesh_isolines(
    triangle_mesh.to_vertices_and_faces(),
    scalars,
    num_isolines,
)

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = Viewer()

cmap = ColorMap.from_mpl("viridis")

for index, edge in enumerate(edges):
    color = cmap(index, 0, max(1, len(edges) - 1))
    viewer.scene.add(Line(vertices[edge[0]], vertices[edge[1]]), linecolor=color, linewidth=3)

viewer.show()
