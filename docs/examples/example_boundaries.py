import math

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Polyline
from compas.geometry import Rotation
from compas.geometry import Scale
from compas_viewer import Viewer

import compas_libigl as libigl

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

viewer = Viewer(width=1600, height=900)
# viewer.view.camera.position = [8, -7, 1]
# viewer.view.camera.look_at([1, 0, 0])


for vertices in boundaries:
    vertices = list(vertices)
    vertices.append(vertices[0])
    points = mesh.vertices_attributes("xyz", keys=vertices)
    polyline = Polyline(points)
    viewer.scene.add(polyline, linecolor=Color.red(), linewidth=3)

viewer.scene.add(
    mesh,
    facecolor=Color.green(),
    linecolor=Color.green().darkened(20),
    opacity=0.7,
    show_points=False,
    show_lines=False,
)

viewer.show()
