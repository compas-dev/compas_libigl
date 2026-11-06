import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import FaceTriangulation
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector
from compas_viewer import Viewer

from compas_libigl.curvature import trimesh_principal_curvature

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
trimesh = mesh.copy()
trimesh.triangulate(FaceTriangulation())

# ==============================================================================
# Principal Curvature
# ==============================================================================

vertices, faces = trimesh.to_vertices_and_faces()
PD1, PD2, PV1, PV2 = trimesh_principal_curvature((vertices, faces))

# ==============================================================================
# Visualization
# ==============================================================================

viewer = Viewer()

# Add the colored mesh
viewer.scene.add(mesh, show_lines=False, show_points=False)

# Scale factor for principal direction lines
principal_scale = 0.3

# Add principal direction lines
for vertex_idx, point in enumerate(vertices):
    if not trimesh.is_vertex_on_boundary(vertex_idx):
        point = Point(point[0], point[1], point[2])

        # Scale lines by curvature magnitude
        pd1x, pd1y, pd1z = PD1[vertex_idx]
        pd2x, pd2y, pd2z = PD2[vertex_idx]
        pd1 = Vector(pd1x, pd1y, pd1z).scaled(principal_scale * abs(PV1[vertex_idx]))
        pd2 = Vector(pd2x, pd2y, pd2z).scaled(principal_scale * abs(PV2[vertex_idx]))

        # Maximum principal direction (black)
        viewer.scene.add(Line(point - pd1, point + pd1), linecolor=Color.black(), linewidth=20)
        # Minimum principal direction (black)
        viewer.scene.add(Line(point - pd2, point + pd2), linecolor=Color.black(), linewidth=20)


viewer.show()
