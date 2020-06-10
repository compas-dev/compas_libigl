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
# Isolines
# ==============================================================================

M = tri.to_vertices_and_faces()

mass = igl.trimesh_massmatrix(M)

# ==============================================================================
# Visualisation
# ==============================================================================

cmap = Colormap(mass, 'red')

plotter = MeshPlotter(tri, figsize=(8, 5))
plotter.draw_vertices(
    radius=0.2,
    facecolor={key: cmap(mass[index]) for index, key in enumerate(tri.vertices())})
plotter.draw_faces()
plotter.show()
