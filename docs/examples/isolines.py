import math

import compas_libigl as igl
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Polyline
from compas.geometry import Rotation
from compas.geometry import Scale

# from compas_view2.objects import Collection
from compas_viewer import Viewer

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

scalars = mesh.vertices_attribute("z")
vertices, edges = igl.trimesh_isolines(mesh.to_vertices_and_faces(), scalars, 100)
isolines = igl.groupsort_isolines(vertices, edges)

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = Viewer(width=1600, height=900)
# viewer.view.camera.position = [8, -7, 1]
# viewer.view.camera.look_at([1, 0, 0])

viewer.scene.add(mesh, opacity=0.7, show_lines=False, show_points=False)

minval = min(scalars) - 0.01
maxval = max(scalars) + 0.01

cmap = ColorMap.from_rgb()

for value, paths in isolines:
    polylines = []
    for path in paths:
        points = [vertices[path[0][0]]]
        for i, j in path:
            points.append(vertices[j])
        polylines.append(Polyline(points))

    # viewer.scene.add(
    #     Collection(polylines),
    #     linecolor=cmap(value, minval=minval, maxval=maxval),
    #     linewidth=3,
    # )

viewer.show()
