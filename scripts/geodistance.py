import os
import compas
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.utilities import Colormap
from compas_plotters import MeshPlotter
import compas_libigl as igl

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh2.json')

mesh = Mesh.from_json(FILE)

tri = mesh.copy()
mesh_quads_to_triangles(tri)

M = tri.to_vertices_and_faces()
source = mesh.get_any_vertex()

D = igl.trimesh_geodistance(M, source)
vertices, edges = igl.trimesh_isolines(M, D, 50)

lines = []
for i, j in edges:
    lines.append({
        'start' : vertices[i],
        'end'   : vertices[j],
        'color' : (255, 0, 0)
    })

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.draw_lines(lines)
plotter.show()
