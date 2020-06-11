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
# curvature
# ==============================================================================

curvature = igl.trimesh_curvature(mesh)

# ==============================================================================
# Visualisation
# ==============================================================================

boundary = mesh.vertices_on_boundary()
cmap = Colormap([curvature[index] for index, key in enumerate(mesh.vertices()) if key not in boundary], 'red')

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_vertices(
    keys=list(key for key in mesh.vertices() if key not in boundary),
    radius=0.2,
    facecolor={key: cmap(curvature[index]) for index, key in enumerate(mesh.vertices()) if key not in boundary})
plotter.draw_faces()
plotter.show()
