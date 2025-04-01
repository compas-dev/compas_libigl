import compas
import numpy as np
import compas_libigl as igl
from compas.colors import Color
from compas.colors.colormap import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Line, Point, Vector
from compas_viewer import Viewer
from compas_viewer.scene import BufferGeometry

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
trimesh = mesh.copy()
trimesh.quads_to_triangles()

# ==============================================================================
# Principal Curvature
# ==============================================================================

vertices, faces = trimesh.to_vertices_and_faces()
PD1, PD2, PV1, PV2 = igl.trimesh_principal_curvature((vertices, faces))

# ==============================================================================
# Visualization
# ==============================================================================

viewer = Viewer()

# Add the colored mesh
viewer.scene.add(mesh)

# Scale factor for principal direction lines
principal_scale = 0.3

# Add principal direction lines
for vertex_idx, point in enumerate(vertices):
    if not trimesh.is_vertex_on_boundary(vertex_idx):
        point = Point(*point)
        
        # Scale lines by curvature magnitude
        pd1 = Vector(*PD1[vertex_idx]).scaled(principal_scale * abs(PV1[vertex_idx]))
        pd2 = Vector(*PD2[vertex_idx]).scaled(principal_scale * abs(PV2[vertex_idx]))
        
        # Maximum principal direction (black)
        viewer.scene.add(
            Line(point - pd1, point + pd1),
            linecolor=Color.black(),
            linewidth=20
        )
        # Minimum principal direction (black)
        viewer.scene.add(
            Line(point - pd2, point + pd2),
            linecolor=Color.black(),
            linewidth=20
        )


viewer.show()
