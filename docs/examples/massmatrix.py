import compas
import compas_libigl as igl
from compas.datastructures import Mesh
from compas.colors import ColorMap
from compas_view2.app import App

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

trimesh = mesh.copy()
trimesh.quads_to_triangles()

# ==============================================================================
# Mass matrix
# ==============================================================================

mass = igl.trimesh_massmatrix(trimesh.to_vertices_and_faces())

# ==============================================================================
# Visualisation
# ==============================================================================

cmap = ColorMap.from_rgb()

minval = min(mass)
maxval = max(mass)

viewer = App(width=1600, height=900)
viewer.view.camera.position = [1, -6, 2]
viewer.view.camera.look_at([1, 1, 1])

viewer.add(mesh)

for m, vertex in zip(mass, mesh.vertices()):
    point = mesh.vertex_point(vertex)
    viewer.add(point, pointsize=30, pointcolor=cmap(m, minval, maxval))

viewer.run()
