import compas_libigl as igl
from compas.datastructures import Mesh
from compas.utilities import Colormap
from compas_plotters import MeshPlotter

# ==============================================================================
# Input
# ==============================================================================

mesh = Mesh.from_off(igl.get('tubemesh.off'))
mesh.quads_to_triangles()

# ==============================================================================
# Geodesic distance
# ==============================================================================

source = mesh.get_any_vertex()
distance = igl.trimesh_geodistance(mesh, source)

# ==============================================================================
# Visualize
# ==============================================================================

cmap = Colormap(distance, 'red')

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_vertices(
    radius=0.2,
    facecolor={key: cmap(distance[index]) for index, key in enumerate(mesh.vertices())}
)
plotter.draw_faces()
plotter.show()
