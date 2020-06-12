import math
from itertools import groupby
import compas_libigl as igl
from compas.datastructures import Mesh
from compas.utilities import Colormap
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
levels = groupby(sorted(edges, key=lambda edge: vertices[edge[0]][2]), key=lambda edge: round(vertices[edge[0]][2], 3))

isolines = []
for value, edges in levels:
    paths = []
    edges = [edge.tolist() for edge in edges]
    edge = edges.pop()
    paths.append([edge])
    while edges:
        for edge in edges:
            found = False
            for path in paths:
                a = path[0][0]
                z = path[-1][1]
                u, v = edge
                if u == z:
                    path.append([u, v])
                    edges.remove(edge)
                    found = True
                    break
                if v == z:
                    path.append([v, u])
                    edges.remove(edge)
                    found = True
                    break
                if v == a:
                    path.insert(0, [u, v])
                    edges.remove(edge)
                    found = True
                    break
                if u == a:
                    path.insert(0, [v, u])
                    edges.remove(edge)
                    found = True
                    break
            if not found:
                paths.append([edge])
                edges.remove(edge)
    isolines.append((value, paths))

# ==============================================================================
# Visualisation
# ==============================================================================

cmap = Colormap(scalars, 'rgb')

viewer = ObjectViewer()

viewer.add(mesh, settings={'color': '#00ff00', 'vertices.on': False, 'edges.on': False})

for value, paths in isolines:
    for path in paths:
        points = [vertices[path[0][0]]]
        for i, j in path:
            points.append(vertices[j])
        viewer.add(Polyline(points), settings={'edges.color': '#ff0000', 'edges.width': 5, 'vertices.on': False})

viewer.update()
viewer.show()
