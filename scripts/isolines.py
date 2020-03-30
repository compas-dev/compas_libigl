import os
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas_plotters import MeshPlotter
from compas.utilities import i_to_rgb
import compas_libigl as igl

# ==============================================================================
# Input geometry
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh = Mesh.from_json(FILE)
mesh_quads_to_triangles(mesh)

# ==============================================================================
# Isolines
# ==============================================================================

key_index = mesh.key_index()

V = mesh.vertices_attributes('xyz')
F = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]
S = mesh.vertices_attribute('z')
N = 50

vertices, levels = igl.trimesh_isolines(V, F, S, N)

# ==============================================================================
# Visualisation
# ==============================================================================

smin = min(S)
smax = max(S)

lines = []
for scalar, edges in levels:
    for i, j in edges:
        lines.append({
            'start' : vertices[i],
            'end'   : vertices[j],
            'color' : i_to_rgb((scalar - smin) / (smax - smin))
        })

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.draw_lines(lines)
plotter.show()
