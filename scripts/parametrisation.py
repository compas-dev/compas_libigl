import os
from compas.datastructures import Mesh
from compas.utilities import Colormap
from compas_plotters import MeshPlotter
import compas_libigl as igl

# ==============================================================================
# Input geometry
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh = Mesh.from_json(FILE)

tri = mesh.copy()
tri.quads_to_triangles()

# ==============================================================================
# Boundaries
# ==============================================================================

M = tri.to_vertices_and_faces()

uv = igl.trimesh_harmonic_map(M)

tri_uv = tri.copy()

for index, key in enumerate(tri_uv.vertices()):
    tri_uv.vertex_attributes(key, 'xy', uv[index])

# ==============================================================================
# Visualization
# ==============================================================================

plotter = MeshPlotter(tri_uv, figsize=(8, 5))
plotter.draw_faces()
plotter.show()
