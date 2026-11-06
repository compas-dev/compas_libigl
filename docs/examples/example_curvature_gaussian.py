import compas
from compas.colors import Color
from compas.colors.colormap import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Line
from compas_viewer import Viewer

from compas_libigl.curvature import trimesh_gaussian_curvature

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
triangle_mesh = mesh.triangulated()

# ==============================================================================
# Gaussian Curvature
# ==============================================================================

vertices, faces = triangle_mesh.to_vertices_and_faces()
gaussian_curvature = trimesh_gaussian_curvature((vertices, faces))

# Get non-boundary vertex indices
non_boundary_vertices = [i for i in range(len(vertices)) if not mesh.is_vertex_on_boundary(i)]

# Prepare vertex colors based on Gaussian curvature (excluding boundary vertices)
min_gaussian = min(gaussian_curvature[i] for i in non_boundary_vertices)
max_gaussian = max(gaussian_curvature[i] for i in non_boundary_vertices)


# Create two-color maps for negative and positive curvature
cmap_negative = ColorMap.from_two_colors(Color.blue(), Color.yellow())
cmap_positive = ColorMap.from_two_colors(Color.yellow(), Color.magenta())

# Create vertex colors dictionary
vertex_colors = {}
for i, k in enumerate(gaussian_curvature):
    if mesh.is_vertex_on_boundary(i):
        # Set boundary vertices to black
        vertex_colors[i] = Color.black()
    else:
        if k < 0:
            vertex_colors[i] = cmap_negative(k, minval=min_gaussian, maxval=0)
        else:
            vertex_colors[i] = cmap_positive(k, minval=0, maxval=max_gaussian)

# ==============================================================================
# Visualization
# ==============================================================================

viewer = Viewer()

# Add the colored mesh
viewer.scene.add(mesh, use_vertexcolors=True, pointcolor=vertex_colors)

# Add normal vectors scaled by Gaussian curvature
normal_scale = -10
for vertex in mesh.vertices():
    if not mesh.is_vertex_on_boundary(vertex):
        point = mesh.vertex_point(vertex)
        normal = mesh.vertex_normal(vertex)
        k = gaussian_curvature[vertex]
        end_point = point + normal.scaled(normal_scale * k)

        viewer.scene.add(Line(point, end_point), linecolor=Color.black(), linewidth=2)

viewer.show()
