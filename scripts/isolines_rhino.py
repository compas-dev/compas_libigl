import os
from itertools import groupby
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.utilities import i_to_rgb
from compas_rhino.artists import MeshArtist
from compas.rpc import Proxy

igl = Proxy('compas_libigl')
igl.stop_server()
igl.start_server()

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '..', 'data', 'tubemesh.json')

mesh = Mesh.from_json(FILE)
mesh_quads_to_triangles(mesh)

vertices, faces = mesh.to_vertices_and_faces()
scalarfield = mesh.get_vertices_attribute('z')
iso = igl.trimesh_isolines_proxy(vertices, faces, scalarfield, 30)
levels = groupby(iso[1], key=lambda e: iso[0][e[0]][2])

smin = min(scalarfield)
smax = max(scalarfield)
sspn = smax - smin

lines = []
for s, edges in levels:
    color = i_to_rgb((s - smin) / sspn)
    for i, j in edges:
        lines.append({
            'start' : iso[0][i],
            'end'   : iso[0][j],
            'color' : color
        })

artist = MeshArtist(mesh, layer="IGL::Isolines")
artist.draw_faces()
artist.draw_lines(lines)
