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
distance = igl.trimesh_geodistance(mesh.to_vertices_and_faces(), source, method='heat')

# ==============================================================================
# Visualize
# ==============================================================================

cmap = Colormap(distance, 'red')

plotter = MeshPlotter(mesh, figsize=(16, 9), tight=True)
plotter.draw_vertices(
    radius=0.2,
    facecolor={key: cmap(distance[index]) for index, key in enumerate(mesh.vertices())}
)
plotter.draw_faces()
plotter.save('examples/geodistance.png')
