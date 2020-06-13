import compas_libigl as igl

from compas.geometry import Point, Vector, Line
from compas.datastructures import Mesh
from compas.utilities import Colormap

from compas_viewers.objectviewer import ObjectViewer

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_off(igl.get('tubemesh.off'))
mesh.quads_to_triangles()

# ==============================================================================
# curvature
# ==============================================================================

curvature = igl.trimesh_gaussian_curvature(mesh)

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = ObjectViewer()

viewer.add(
    mesh,
    settings={'color': '#cccccc', 'vertices.on': True, 'edges.on': False, 'opacity': 0.7, 'vertices.size': 5})

for vertex in mesh.vertices():
    if mesh.is_vertex_on_boundary(vertex):
        continue

    point = Point(* mesh.vertex_coordinates(vertex))
    normal = Vector(* mesh.vertex_normal(vertex))
    c = curvature[vertex]
    normal.scale(10 * c)

    color = '#ff0000' if c > 0 else '#0000ff'

    viewer.add(
        Line(point, point + normal),
        settings={'vertices.on': False, 'edges.color': color, 'edges.width': 3})

viewer.update()
viewer.show()
