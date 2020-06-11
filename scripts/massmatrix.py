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
# Mass matrix
# ==============================================================================

mass = igl.trimesh_massmatrix(mesh)

# ==============================================================================
# Visualisation
# ==============================================================================

cmap = Colormap(mass, 'red')

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_vertices(
    radius=0.2,
    facecolor={key: cmap(mass[index]) for index, key in enumerate(mesh.vertices())})
plotter.draw_faces()
plotter.show()
