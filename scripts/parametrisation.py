import os
from compas.datastructures import Mesh
from compas.utilities import Colormap
from compas_plotters import MeshPlotter
import compas_libigl as igl

# ==============================================================================
# Input geometry
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'camelhead.off')

mesh = Mesh.from_off(FILE)
mesh_harmonic = mesh.copy()
mesh_lscm = mesh.copy()

# ==============================================================================
# Boundaries
# ==============================================================================

M = mesh.to_vertices_and_faces()

harmonic_uv = igl.trimesh_harmonic_map(M)
lscm_uv = igl.trimesh_lscm(M)

for index, key in enumerate(mesh.vertices()):
    mesh_harmonic.vertex_attributes(key, 'xy', harmonic_uv[index])

for index, key in enumerate(mesh.vertices()):
    mesh_lscm.vertex_attributes(key, 'xy', lscm_uv[index])

# ==============================================================================
# Visualization
# ==============================================================================

plotter = MeshPlotter(mesh_lscm, figsize=(8, 5))
plotter.draw_faces()
plotter.show()
