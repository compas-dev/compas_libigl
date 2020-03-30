import os
import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.utilities import Colormap
from compas_plotters import MeshPlotter
import compas_libigl as igl

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh = Mesh.from_json(FILE)
mesh_quads_to_triangles(mesh)

key_index = mesh.key_index()
index_key = mesh.index_key()

V = mesh.vertices_attributes('xyz')
F = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

root = mesh.get_any_vertex()

# D = igl.trimesh_geodistance_exact(V, F, 0)
D = igl.trimesh_geodistance_heat(V, F, key_index[root])

cmap = Colormap(D, 'red')

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.draw_vertices(text={root: 'root'}, radius=0.2, facecolor={key: cmap(d) for key, d in zip(mesh.vertices(), D)})
plotter.show()
