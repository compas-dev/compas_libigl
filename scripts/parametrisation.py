import compas_libigl as igl

from compas.datastructures import Mesh
from compas.utilities import Colormap
from compas_plotters import MeshPlotter

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_off(igl.get('camelhead.off'))
mesh_harmonic = mesh.copy()
mesh_lscm = mesh.copy()

# ==============================================================================
# Harmonic parametrisation
# ==============================================================================

harmonic_uv = igl.trimesh_harmonic(mesh)

for index, key in enumerate(mesh.vertices()):
    mesh_harmonic.vertex_attributes(key, 'xy', harmonic_uv[index])

# ==============================================================================
# Least-squares conformal map
# ==============================================================================

lscm_uv = igl.trimesh_lscm(mesh)

for index, key in enumerate(mesh.vertices()):
    mesh_lscm.vertex_attributes(key, 'xy', lscm_uv[index])

# ==============================================================================
# Visualization
# ==============================================================================

plotter = MeshPlotter(mesh_lscm, figsize=(8, 5))
plotter.draw_faces()
plotter.show()
