import compas_libigl as igl
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.datastructures import Mesh

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_off(igl.get('tubemesh.off'))
mesh.quads_to_triangles()

# ==============================================================================
# Ray & Intersections
# ==============================================================================

point = mesh.centroid()
point[2] = 0
vector = [0, 0, 1.0]

hits = igl.intersection_ray_mesh((point, vector), mesh)

if hits:
    for hit in hits:
        x = add_vectors(point, scale_vector(vector, hit[3]))
        print(x)
