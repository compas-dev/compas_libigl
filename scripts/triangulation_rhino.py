import os
import json
import compas_rhino
from compas.geometry import centroid_points_xy
from compas.utilities import geometric_key
from compas.utilities import pairwise
from compas.datastructures import Mesh
from compas_rhino.geometry import RhinoCurve
from compas_rhino.artists import MeshArtist
from compas.rpc import Proxy

# from compas.external import igl
igl = Proxy("compas_libigl")

# ==============================================================================
# Input
# ==============================================================================

# boundary
guids = compas_rhino.select_curves()
curve = RhinoCurve.from_guid(guids[0])
points = [list(point) for point in curve.points]
boundary = points

# segments
guids = compas_rhino.select_curves()
curve = RhinoCurve.from_guid(guids[0])
points = curve.divide(10, over_space=True)
segments = points

# hole
guids = compas_rhino.select_curves()
curve = RhinoCurve.from_guid(guids[0])
points = curve.divide(10, over_space=True)
hole = points

# ==============================================================================
# Clean
# ==============================================================================

gkey_xyz = {geometric_key(point): point for point in boundary}
gkey_xyz.update({geometric_key(point): point for point in segments})
gkey_xyz.update({geometric_key(point): point for point in hole})

gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz.keys())}

xyz = list(gkey_xyz.values())

edges = []
edges += [(gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]) for a, b in pairwise(boundary)]
edges += [(gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]) for a, b in pairwise(segments)]
edges += [(gkey_index[geometric_key(a)], gkey_index[geometric_key(b)]) for a, b in pairwise(hole)]

holes = []
holes += [centroid_points_xy([xyz[gkey_index[geometric_key(point)]] for point in hole[:-1]])]

# ==============================================================================
# Triangulate
# ==============================================================================

vertices, faces = igl.conforming_delaunay_triangulation(xyz, edges, holes, area=0.5)

mesh = Mesh.from_vertices_and_faces(vertices, faces)

# ==============================================================================
# Visualize
# ==============================================================================

lines = []
for u, v in edges:
    lines.append({'start': xyz[u], 'end': xyz[v], 'color': '#ff0000'})

artist = MeshArtist(mesh, layer="IGL::Triangulation")
artist.clear_layer()
artist.draw_mesh()
artist.draw_edges(keys=edges, color=(255, 0, 0))
