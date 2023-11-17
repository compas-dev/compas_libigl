import math
import compas_libigl as libigl

from compas.datastructures import Mesh
from compas.geometry import Polyline, Rotation, Scale
from compas.colors import Color
from compas_view2.app import App

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_off(libigl.get_beetle())

Rx = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
Rz = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))
S = Scale.from_factors([10, 10, 10])

mesh.transform(S * Rz * Rx)

# ==============================================================================
# Boundaries
# ==============================================================================

boundaries = libigl.trimesh_boundaries(mesh.to_vertices_and_faces())

# ==============================================================================
# Visualize
# ==============================================================================

viewer = App(width=1600, height=900)
viewer.view.camera.position = [8, -7, 1]
viewer.view.camera.look_at([1, 0, 0])

viewer.add(
    mesh,
    facecolor=Color.green(),
    linecolor=Color.green().darkened(20),
    opacity=0.7,
)

for vertices in boundaries:
    points = mesh.vertices_attributes("xyz", keys=vertices)
    polyline = Polyline(points)
    viewer.add(polyline, linecolor=Color.red(), linewidth=3)

viewer.run()
