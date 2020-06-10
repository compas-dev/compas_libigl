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

boundary = tri.vertices_on_boundary()

# ==============================================================================
# curvature
# ==============================================================================

M = tri.to_vertices_and_faces()

curvature = igl.trimesh_curvature(M)

# ==============================================================================
# Visualisation
# ==============================================================================

cmap = Colormap([curvature[index] for index, key in enumerate(tri.vertices()) if key not in boundary], 'red')

plotter = MeshPlotter(tri, figsize=(8, 5))
plotter.draw_vertices(
    keys=list(key for key in tri.vertices() if key not in boundary),
    radius=0.2,
    facecolor={key: cmap(curvature[index]) for index, key in enumerate(tri.vertices()) if key not in boundary})
plotter.draw_faces()
plotter.show()
