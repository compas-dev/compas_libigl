import math
from pathlib import Path

from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Rotation
from compas.geometry import Scale
from compas_viewer import Viewer

from compas_libigl.isolines import groupsort_isolines
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
minval = min(scalars)
maxval = max(scalars)

# Create evenly spaced values
num_isolines = 100
isovalues = [minval + i * (maxval - minval) / (num_isolines - 1) for i in range(num_isolines)]

vertices, edges, indices = trimesh_isolines(mesh.to_vertices_and_faces(), scalars, isovalues)

isolines = groupsort_isolines(vertices, edges, indices)

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = Viewer()

minval = min(scalars) + 0.01
maxval = max(scalars) - 0.01

values = [(v - minval) / (maxval - minval) for v in scalars]

cmap = ColorMap.from_mpl("viridis")

for i, isolines in enumerate(isolines):
    color = cmap(values[i], minval, maxval)
    for isoline in isolines:
        viewer.scene.add(isoline, linecolor=color, linewidth=3)

viewer.show()
