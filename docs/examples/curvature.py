import compas
import compas_libigl as igl
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line, Point, Vector, Scale, Rotation
from compas_viewer import Viewer

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
trimesh = mesh.copy()
trimesh.quads_to_triangles()

# ==============================================================================
# Curvature
# ==============================================================================

vertices, faces = trimesh.to_vertices_and_faces()
gaussian_curvature = igl.trimesh_gaussian_curvature((vertices, faces))
PD1, PD2, PV1, PV2 = igl.trimesh_principal_curvature((vertices, faces))

# Normalize curvature values for better visualization
max_gaussian = max(abs(k) for k in gaussian_curvature)
max_principal = max(max(abs(k) for k in PV1), max(abs(k) for k in PV2))

# Scale factors for visualization
gaussian_scale = 0.5 / max_gaussian if max_gaussian > 0 else 0.5
principal_scale = 0.3 / max_principal if max_principal > 0 else 0.3

# ==============================================================================
# Visualization
# ==============================================================================

viewer = Viewer(width=1600, height=900)

# Add base mesh
viewer.scene.add(
    mesh,
    opacity=0.7,
    show_points=False
)

# Visualize curvature at each vertex
for vertex in mesh.vertices():
    if mesh.is_vertex_on_boundary(vertex):
        continue
        
    # Get vertex position and normal
    point = Point(*mesh.vertex_coordinates(vertex))
    normal = Vector(*mesh.vertex_normal(vertex))
    
    # Gaussian curvature visualization (vertical lines)
    k = gaussian_curvature[vertex]
    scaled_normal = normal.scaled(gaussian_scale * k)
    viewer.scene.add(
        Line(point, point + scaled_normal*100),
        linecolor=Color.blue(),
        linewidth=3
    )
    
    # Principal curvature visualization (cross lines)
    pd1 = Vector(*PD1[vertex]).scaled(2*principal_scale * abs(PV1[vertex]))
    pd2 = Vector(*PD2[vertex]).scaled(2*principal_scale * abs(PV2[vertex]))
    
    # Create lines for principal directions
    viewer.scene.add(
        Line(point - pd1, point + pd1),
        linecolor=Color.black(),
        linewidth=4
    )
    viewer.scene.add(
        Line(point - pd2, point + pd2),
        linecolor=Color.black(),
        linewidth=2
    )


viewer.show()
