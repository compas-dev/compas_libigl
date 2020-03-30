import compas
from compas.geometry import Box
from compas.geometry import Translation
from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.datastructures import mesh_subdivide_quad
from compas_viewers.multimeshviewer import MultiMeshViewer
from compas_viewers.multimeshviewer import MeshObject
import compas_libigl as igl

# ==============================================================================
# Input Geometry
# ==============================================================================

# create a box mesh around the center of the world

box = Box.from_width_height_depth(5.0, 3.0, 1.0)
a = Mesh.from_shape(box)
mesh_quads_to_triangles(a)

# create a box mesh around the center of the world

box = Box.from_width_height_depth(1.0, 5.0, 3.0)
b = Mesh.from_shape(box)
mesh_quads_to_triangles(b)

# ==============================================================================
# Booleans
# ==============================================================================

# convert meshes to data

VA, FA = a.to_vertices_and_faces()
VB, FB = b.to_vertices_and_faces()

# boolean operations

VC, FC = igl.mesh_union(VA, FA, VB, FB)
c_union = Mesh.from_vertices_and_faces(VC, FC)

VC, FC = igl.mesh_intersection(VA, FA, VB, FB)
c_intersection = Mesh.from_vertices_and_faces(VC, FC)

VC, FC = igl.mesh_difference(VA, FA, VB, FB)
c_diff = Mesh.from_vertices_and_faces(VC, FC)

# ==============================================================================
# Visualization
# ==============================================================================

c_union.transform(Translation([7.5, 0, 0]))
c_intersection.transform(Translation([15, 0, 0]))
c_diff.transform(Translation([22.5, 0, 0]))

viewer = MultiMeshViewer()

meshes = [
    MeshObject(a, color='#ff0000'),
    MeshObject(b, color='#0000ff'),
    MeshObject(c_union, color='#ff00ff'),
    MeshObject(c_intersection, color='#00ff00'),
    MeshObject(c_diff, color='#00ff00'),
]

viewer.meshes = meshes
viewer.show()
