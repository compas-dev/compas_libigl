import math
import compas_libigl as igl
from compas.datastructures import Mesh
from compas.utilities import Colormap, rgb_to_hex
from compas.geometry import Line, Polyline, Rotation, Scale
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
# Isolines
# ==============================================================================

scalars = mesh.vertices_attribute('z')
vertices, edges = igl.trimesh_isolines(mesh, scalars, 10)
isolines = igl.groupsort_isolines(vertices, edges)

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = ObjectViewer()

viewer.add(mesh, settings={'color': '#ffffff', 'vertices.on': False, 'edges.on': False})

cmap = Colormap(scalars, 'rgb')
for value, paths in isolines:
    for path in paths:
        points = [vertices[path[0][0]]]
        for i, j in path:
            points.append(vertices[j])
        viewer.add(
            Polyline(points),
            settings={'edges.color': rgb_to_hex(cmap(value)), 'edges.width': 5, 'vertices.on': False})

viewer.update()
viewer.show()
