import compas_libigl as igl

from compas.datastructures import Mesh
from compas.datastructures import mesh_flatness
from compas_plotters import MeshPlotter
from compas.utilities import i_to_rgb

# ==============================================================================
# Input
# ==============================================================================

TOL = 0.02
MAXDEV = 0.005
KMAX = 500

mesh = Mesh.from_off(igl.get('tubemesh.off'))

# ==============================================================================
# Planarize
# ==============================================================================

V, F = mesh.to_vertices_and_faces()
V2 = igl.quadmesh_planarize((V, F), KMAX, MAXDEV)

# ==============================================================================
# Visualize
# ==============================================================================

mesh = Mesh.from_vertices_and_faces(V2, F)
dev = mesh_flatness(mesh, maxdev=TOL)

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces(facecolor={fkey: i_to_rgb(dev[fkey]) for fkey in mesh.faces()})
plotter.show()
