import compas_libigl as igl
from compas.datastructures import Mesh

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_off(igl.get('tubemesh.off'))
mesh.quads_to_triangles()

# ==============================================================================
# Boundaries
# ==============================================================================

boundary = mesh.vertices_on_boundary(ordered=True)
boundaries = igl.trimesh_boundaries(mesh)

print(boundary)
print(boundaries[0])
