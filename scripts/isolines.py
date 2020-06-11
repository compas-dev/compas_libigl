from itertools import groupby

import compas_libigl as igl

from compas.datastructures import Mesh
from compas.utilities import Colormap
from compas_plotters import MeshPlotter

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_off(igl.get('tubemesh.off'))
mesh.quads_to_triangles()

# ==============================================================================
# Isolines
# ==============================================================================

S = mesh.vertices_attribute('z')
vertices, edges = igl.trimesh_isolines(mesh, S, 50)
levels = groupby(sorted(edges, key=lambda edge: vertices[edge[0]][2]), key=lambda edge: vertices[edge[0]][2])

# ==============================================================================
# Visualisation
# ==============================================================================

cmap = Colormap(S, 'rgb')

lines = []
for value, edges in levels:
    for i, j in edges:
        lines.append({
            'start' : vertices[i],
            'end'   : vertices[j],
            'color' : cmap(value)
        })

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.draw_lines(lines)
plotter.show()
