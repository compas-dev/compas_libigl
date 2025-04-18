from math import pi

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Polygon
from compas_viewer import Viewer
from compas_viewer.config import Config
from tessagon.adaptors.list_adaptor import ListAdaptor
from tessagon.types.hex_tessagon import HexTessagon

import compas_libigl as igl

# ==============================================================================
# Input geometry: 3D Mesh
# ==============================================================================

mesh = Mesh.from_obj("data/minimal_surface.obj")
for key, attr in mesh.vertices(True):
    y = attr["y"]
    attr["y"] = -attr["z"]
    attr["z"] = y
mesh.translate([2, 2, 0.5])

v, f = mesh.to_vertices_and_faces()

# ==============================================================================
# Flattening
# ==============================================================================

# To see where the pattern is mapped:
uv = igl.trimesh_lsc_mapping((v, f))
mesh_flattened = mesh.copy()
for i in range(mesh.number_of_vertices()):
    mesh_flattened.vertex_attributes(i, "xyz", [uv[i][0], uv[i][1], 0])


# ==============================================================================
# Input geometry: 2D Pattern creation using Tessagon library, can be other mesh.
# ==============================================================================

options = {
    "function": lambda u, v: [u, v, 0],
    "u_range": [-0.255, 1.33],
    "v_range": [-0.34, 1.33],
    "u_num": 16,
    "v_num": 10,
    "u_cyclic": False,
    "v_cyclic": False,
    "adaptor_class": ListAdaptor,
}
tessagon = HexTessagon(**options)
tessagon_mesh = tessagon.create_mesh()
pv = tessagon_mesh["vert_list"]
pf = tessagon_mesh["face_list"]

# rotate the pattern
rotated_mesh = Mesh.from_vertices_and_faces(pv, pf)
rotated_mesh.rotate(0 * pi / 180, [0, 0, 1])

pv, pf = rotated_mesh.to_vertices_and_faces()

# ==============================================================================
# Boundaries
# ==============================================================================

boundaries = igl.trimesh_boundaries(mesh_flattened.to_vertices_and_faces())

polygons = []
for vertices in boundaries:
    vertices = list(vertices)
    vertices.pop()
    vertices.append(vertices[0])
    points = mesh_flattened.vertices_attributes("xyz", keys=vertices)
    polygons.append(Polygon(points))

# ==============================================================================
# 2D Boolean Intersection using Shapely
# ==============================================================================

polygons_cut = []
for face in pf:
    points = []
    for vertex in face:
        points.append(pv[vertex])
    polygon_cut = Polygon(points)
    if len(points) > 2:
        polygons_cut.append(polygon_cut)


# Polygon.boolean_intersection
intersections = []
for polygon_cut in polygons_cut:
    for polygon in polygons:
        from compas.geometry import boolean_intersection_polygon_polygon

        coords = boolean_intersection_polygon_polygon(polygon, polygon_cut)
        if len(coords) > 0:
            intersection = Polygon([[x, y, 0] for x, y in coords])  # type: ignore
            intersections.append(intersection)

mesh_cropped = Mesh.from_polygons(intersections)
pv, pf = mesh_cropped.to_vertices_and_faces()


# ==============================================================================
# Place the pattern mesh at the bottom left corner of the meshpattern_uv
# ==============================================================================

mv, mf = igl.map_mesh((v, f), (pv, pf))
mesh_mapped = Mesh.from_vertices_and_faces(mv, mf)

# ==============================================================================
# Viewer
# ==============================================================================

config = Config()
config.camera.target = [2, 2, 0.25]
config.camera.position = [5, 2, 1.5]

viewer = Viewer(config=config)
viewer.scene.add(mesh, name="mesh", show_faces=False, linecolor=Color.grey(), opacity=0.2)
viewer.scene.add(mesh_mapped, name="mesh_mapped", facecolor=Color.red())
viewer.scene.add(rotated_mesh, linecolor=Color.red(), linewidth=3)
viewer.scene.add(intersections, linecolor=Color.red(), linewidth=3)
viewer.scene.add(mesh_flattened, name="mesh_flattened0")
viewer.show()
