from pathlib import Path

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Polyline
from compas_viewer import Viewer
from compas_viewer.config import Config
from tessagon.adaptors.list_adaptor import ListAdaptor
from tessagon.types.zig_zag_tessagon import ZigZagTessagon

from compas_libigl.mapping import map_mesh
from compas_libigl.parametrisation import trimesh_lscm

# ==============================================================================
# Input geometry: 3D Mesh
# ==============================================================================

mesh = Mesh.from_off(Path(__file__).parent.parent.parent / "data" / "beetle.off")

for vertex in mesh.vertices():
    point = mesh.vertex_point(vertex)
    mesh.set_vertex_point(vertex, [point.x, -point.z, point.y])

mesh.translate([2, 2, 0.5])

v, f = mesh.to_vertices_and_faces()

# ==============================================================================
# Input geometry: 2D Pattern creation using Tessagon library, can be other mesh.
# ==============================================================================

options = {
    "function": lambda u, v: [u * 1, v * 1, 0],
    "u_range": [-0.255, 1.33],
    "v_range": [-0.34, 1.33],
    "u_num": 20,
    "v_num": 20,
    "u_cyclic": False,
    "v_cyclic": False,
    "adaptor_class": ListAdaptor,
}
tessagon = ZigZagTessagon(**options)
tessagon_mesh = tessagon.create_mesh()
pv = tessagon_mesh["vert_list"]
pf = tessagon_mesh["face_list"]

# ==============================================================================
# Mapping: 3D Mesh, 2D Pattern, UV
# mv - mapped vertices
# mf - mapped faces
# mn - mapped normals
# boundary_flags - one flag per mapped face indicating boundary clipping
# polygon_groups - one source pattern-polygon group per mapped face
# ==============================================================================
mv, mf, mn, boundary_flags, polygon_groups = map_mesh((v, f), (pv, pf))
mesh_mapped = Mesh.from_vertices_and_faces(mv, mf)

# ==============================================================================
# Offset mesh by normals, normals are interpolated from the original mesh.
# ==============================================================================
mesh_mapped_offset = mesh_mapped.copy()
for index, vertex in enumerate(mesh_mapped.vertices()):
    offset = mn[index] * 0.001
    mesh_mapped_offset.set_vertex_point(vertex, mesh_mapped.vertex_point(vertex) + -offset)

# ==============================================================================
# Get Boundary Polylines
# ==============================================================================
boundaries = []
for i in range(len(boundary_flags)):
    if not boundary_flags[i]:
        continue
    points = []
    for j in range(len(mf[i])):
        vertex = mf[i][j]
        points.append(mesh_mapped.vertex_point(vertex) + mn[vertex] * 0.002)
    points.append(points[0])
    polyline = Polyline(points)
    boundaries.append(polyline)


# ==============================================================================
# Viewer
# ==============================================================================

config = Config()
config.camera.target = [2, 2, 0.25]
config.camera.position = [5, 2, 1.5]

viewer = Viewer(config=config)
# viewer.scene.add(mesh, name="mesh", show_faces=False, linecolor=Color.grey(), opacity=0.2)
viewer.scene.add(Mesh.from_vertices_and_faces(pv, pf), name="pattern2d")
viewer.scene.add(mesh_mapped, name="mesh_mapped", facecolor=Color.pink())
viewer.scene.add(mesh_mapped_offset, name="mesh_mapped", facecolor=Color.blue())
for boundary in boundaries:
    viewer.scene.add(boundary, name="boundary", linecolor=Color.yellow(), linewidth=3)

# To see where the pattern is mapped:
uv = trimesh_lscm((v, f))
mesh_flattened = mesh.copy()
for index, vertex in enumerate(mesh.vertices()):
    mesh_flattened.set_vertex_point(vertex, [uv[index][0], uv[index][1], 0])

viewer.scene.add(mesh_flattened, name="mesh_flattened")
viewer.show()
