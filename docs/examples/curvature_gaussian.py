import compas
import numpy as np
import compas_libigl as igl
from compas.colors import Color
from compas.colors.colormap import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Point, Line, Vector
from compas_viewer import Viewer
from compas_viewer.scene import BufferGeometry

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
trimesh = mesh.copy()
trimesh.quads_to_triangles()

# ==============================================================================
# Gaussian Curvature
# ==============================================================================

vertices, faces = trimesh.to_vertices_and_faces()
gaussian_curvature = igl.trimesh_gaussian_curvature((vertices, faces))

# Get non-boundary vertex indices
non_boundary_vertices = [i for i in range(len(vertices)) if not trimesh.is_vertex_on_boundary(i)]

# Prepare vertex colors based on Gaussian curvature (excluding boundary vertices)
min_gaussian = min(gaussian_curvature[i] for i in non_boundary_vertices)
max_gaussian = max(gaussian_curvature[i] for i in non_boundary_vertices)
print(f"Gaussian curvature range: {min_gaussian:.3f} to {max_gaussian:.3f}")

# Scale factor for normal vectors
normal_scale = -10

# Create two-color maps for negative and positive curvature
cmap_negative = ColorMap.from_two_colors(Color.blue(), Color.yellow())
cmap_positive = ColorMap.from_two_colors(Color.yellow(), Color.magenta())

# Convert mesh to numpy arrays for BufferGeometry
vertices = np.array(vertices, dtype=np.float32)
faces = np.array(faces, dtype=np.float32)

# Create vertex colors array (Nx4 for RGBA)
vertex_colors = np.zeros((len(vertices), 4), dtype=np.float32)
for i, k in enumerate(gaussian_curvature):
    if trimesh.is_vertex_on_boundary(i):
        # Set boundary vertices to a neutral color
        vertex_colors[i] = [0, 0, 0, 1.0]
    else:
        if k < 0:
            color = cmap_negative(k, minval=min_gaussian, maxval=0)
        else:
            color = cmap_positive(k, minval=0, maxval=max_gaussian)
        vertex_colors[i] = (color[0], color[1], color[2], 1.0)

# Create geometry for the mesh with vertex colors
faces_for_buffer = np.array([vertices[f] for f in faces.astype(int)]).reshape(-1, 3)
vertex_colors_for_buffer = np.array([vertex_colors[i] for i in faces.astype(int)]).reshape(-1, 4)

geometry = BufferGeometry(
    faces=faces_for_buffer,
    facecolor=vertex_colors_for_buffer
)

# ==============================================================================
# Visualization
# ==============================================================================

viewer = Viewer()
viewer.scene.add(geometry)

# Add normal vectors colored by Gaussian curvature
for vertex_idx, point in enumerate(vertices):
    if not trimesh.is_vertex_on_boundary(vertex_idx):
        point = Point(*point)
        normal = Vector(*trimesh.vertex_normal(vertex_idx))
        k = gaussian_curvature[vertex_idx]
        
        # Scale normal by absolute curvature value
        scaled_normal = normal.scaled(normal_scale * k)
        
        viewer.scene.add(
            Line(point, point + scaled_normal),
            linecolor=Color.black(),
            linewidth=2
        )
viewer.show()
