from compas.colors import Color
from compas.datastructures import Mesh
from compas_viewer import Viewer
from compas_viewer.config import Config
from tessagon.adaptors.list_adaptor import ListAdaptor
from tessagon.types.brick_tessagon import BrickTessagon
from tessagon.types.dissected_hex_quad_tessagon import DissectedHexQuadTessagon
from tessagon.types.dissected_hex_tri_tessagon import DissectedHexTriTessagon
from tessagon.types.dissected_square_tessagon import DissectedSquareTessagon
from tessagon.types.dissected_triangle_tessagon import DissectedTriangleTessagon
from tessagon.types.dodeca_tessagon import DodecaTessagon
from tessagon.types.floret_tessagon import FloretTessagon
from tessagon.types.hex_big_tri_tessagon import HexBigTriTessagon

from tessagon.types.hex_tessagon import HexTessagon
from tessagon.types.hex_tri_tessagon import HexTriTessagon
from tessagon.types.octo_tessagon import OctoTessagon
from tessagon.types.pythagorean_tessagon import PythagoreanTessagon
from tessagon.types.rhombus_tessagon import RhombusTessagon
from tessagon.types.square_tessagon import SquareTessagon
from tessagon.types.square_tri_tessagon import SquareTriTessagon
from tessagon.types.tri_tessagon import TriTessagon
from tessagon.types.weave_tessagon import WeaveTessagon
from tessagon.types.zig_zag_tessagon import ZigZagTessagon

import compas_libigl as igl

TESSAGON_TYPES = {
    1: ("Hex", HexTessagon),
    2: ("Tri", TriTessagon),
    3: ("Octo", OctoTessagon),
    4: ("Square", SquareTessagon),
    5: ("Rhombus", RhombusTessagon),
    6: ("HexTri", HexTriTessagon),
    7: ("DissectedSquare", DissectedSquareTessagon),
    8: ("DissectedTriangle", DissectedTriangleTessagon),
    9: ("DissectedHexQuad", DissectedHexQuadTessagon),
    10: ("DissectedHexTri", DissectedHexTriTessagon),
    11: ("Floret", FloretTessagon),
    12: ("Pythagorean", PythagoreanTessagon),
    13: ("Brick", BrickTessagon),
    14: ("Weave", WeaveTessagon),
    15: ("ZigZag", ZigZagTessagon),
    16: ("HexBigTri", HexBigTriTessagon),
    17: ("Dodeca", DodecaTessagon),
    18: ("SquareTri", SquareTriTessagon),
}

# Pattern selection - change this value to use a different pattern
PATTERN_TYPE = 15

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
# Input geometry: 2D Pattern creation using Tessagon library, can be other mesh.
# ==============================================================================

options = {
    "function": lambda u, v: [u, v, 0],
    "u_range": [-0.25, 1.25],
    "v_range": [-0.25, 1.25],
    "u_num": 20,
    "v_num": 20,
    "u_cyclic": False,
    "v_cyclic": False,
    "adaptor_class": ListAdaptor,
}

# Get pattern name and class based on selected pattern type
pattern_name, pattern_class = TESSAGON_TYPES[PATTERN_TYPE]

# Create the selected tessagon pattern
tessagon = pattern_class(**options)
tessagon_mesh = tessagon.create_mesh()
pv = tessagon_mesh["vert_list"]
pf = tessagon_mesh["face_list"]

# ==============================================================================
# Mapping: 3D Mesh, 2D Pattern, UV
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
viewer.scene.add(Mesh.from_vertices_and_faces(pv, pf), name="pattern2d")
viewer.scene.add(mesh_mapped, name="mesh_mapped", facecolor=Color.red())

# To see where the pattern is mapped:
uv = igl.trimesh_lsc_mapping((v, f))
mesh_flattened = mesh.copy()
for i in range(mesh.number_of_vertices()):
    mesh_flattened.vertex_attributes(i, "xyz", [uv[i][0], uv[i][1], 0])

viewer.scene.add(mesh_flattened, name="mesh_flattened")
viewer.show()
