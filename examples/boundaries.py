import math
import compas_libigl as igl

from compas.datastructures import Mesh
from compas.geometry import Point, Polyline, Rotation, Scale
from compas_viewers.objectviewer import ObjectViewer

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_off(igl.get_beetle())

Rx = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
Rz = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))
S = Scale.from_factors([10, 10, 10])

mesh.transform(S * Rz * Rx)

# ==============================================================================
# Boundaries
# ==============================================================================

boundaries = igl.trimesh_boundaries(mesh)

# ==============================================================================
# Visualize
# ==============================================================================

viewer = ObjectViewer()

viewer.add(mesh, settings={'color': '#00ff00', 'opacity': 0.7, 'edges.on': False, 'vertices.on': False})

for indices in boundaries:
    points = mesh.vertices_attributes('xyz', keys=indices)
    polyline = Polyline(points)
    viewer.add(polyline, settings={
        'edges.color': '#ff0000',
        'edges.width': 5,
        'vertices.on': False
    })

viewer.update()
viewer.show()
