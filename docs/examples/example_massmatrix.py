import compas
import numpy as np
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas_viewer import Viewer

from compas_libigl.massmatrix import trimesh_massmatrix

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

trimesh = mesh.copy()
trimesh.quads_to_triangles()

# ==============================================================================
# Mass matrix
# ==============================================================================

mass = trimesh_massmatrix(trimesh.to_vertices_and_faces())
# Convert sparse diagonal to dense array
mass_diag = np.array(mass.diagonal())

# ==============================================================================
# Visualisation
# ==============================================================================

cmap = ColorMap.from_rgb()

minval = mass_diag.min()
maxval = mass_diag.max()

viewer = Viewer(width=1600, height=900)
# viewer.view.camera.position = [1, -6, 2]
# viewer.view.camera.look_at([1, 1, 1])

viewer.scene.add(mesh, show_points=False)

for m, vertex in zip(mass_diag, mesh.vertices()):
    point = mesh.vertex_point(vertex)
    viewer.scene.add(point, pointsize=30, pointcolor=cmap(m, minval, maxval))

viewer.show()
