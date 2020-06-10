import os
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
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
# Ray & Intersections
# ==============================================================================

M = tri.to_vertices_and_faces()

point = tri.centroid()
point[2] = 0
vector = [0, 0, 1.0]

hits = igl.intersection_ray_mesh((point, vector), M)

if hits:
    for hit in hits:
        x = add_vectors(point, scale_vector(vector, hit[3]))
        print(x)
