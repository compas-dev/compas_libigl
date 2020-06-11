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

# ==============================================================================
# Boundaries
# ==============================================================================

boundary = tri.vertices_on_boundary(ordered=True)

M = tri.to_vertices_and_faces()

boundaries = igl.trimesh_boundaries(M)

print(boundary)
print(boundaries[0])
