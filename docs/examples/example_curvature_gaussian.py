import compas
from compas.colors import Color
from compas.colors.colormap import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Point
from compas_viewer import Viewer

from compas_libigl.curvature import trimesh_gaussian_curvature

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
gaussian_curvature = trimesh_gaussian_curvature((vertices, faces))

# Get non-boundary vertex indices
non_boundary_vertices = [i for i in range(len(vertices)) if not trimesh.is_vertex_on_boundary(i)]

# Prepare vertex colors based on Gaussian curvature (excluding boundary vertices)
min_gaussian = min(gaussian_curvature[i] for i in non_boundary_vertices)
max_gaussian = max(gaussian_curvature[i] for i in non_boundary_vertices)


# Create two-color maps for negative and positive curvature
cmap_negative = ColorMap.from_two_colors(Color.blue(), Color.yellow())
cmap_positive = ColorMap.from_two_colors(Color.yellow(), Color.magenta())

# Create vertex colors dictionary
vertex_colors = {}
for i, k in enumerate(gaussian_curvature):
    if trimesh.is_vertex_on_boundary(i):
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
viewer.scene.add(trimesh, use_vertexcolors=True, pointcolor=vertex_colors)

# Add normal vectors scaled by Gaussian curvature
normal_scale = -10
for vertex in trimesh.vertices():
    if not trimesh.is_vertex_on_boundary(vertex):
        point = Point(*trimesh.vertex_coordinates(vertex))
        normal = trimesh.vertex_normal(vertex)
        k = gaussian_curvature[vertex]

        scaled_normal = [n * normal_scale * k for n in normal]
        end_point = Point(*(p + n for p, n in zip(point, scaled_normal)))

        viewer.scene.add(Line(point, end_point), linecolor=Color.black(), linewidth=2)

viewer.show()
