import os
from itertools import groupby
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.utilities import Colormap
from compas_plotters import MeshPlotter
from compas.utilities import i_to_rgb
import compas_libigl as igl

# ==============================================================================
# Input geometry
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh = Mesh.from_json(FILE)

tri = mesh.copy()
mesh_quads_to_triangles(tri)

# ==============================================================================
# Isolines
# ==============================================================================

M = tri.to_vertices_and_faces()
S = tri.vertices_attribute('z')

vertices, edges = igl.trimesh_isolines(M, S, 50)

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
