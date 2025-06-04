from pathlib import Path

from compas.colors import Color
from compas.datastructures import Mesh
from compas_viewer import Viewer
from compas_viewer.config import Config

from compas_libigl.mapping import map_pattern_to_mesh



# ==============================================================================
# Input geometry: 3D Mesh
# ==============================================================================

mesh = Mesh.from_obj(Path(__file__).parent.parent.parent / "data" / "minimal_surface.obj")

for vertex in mesh.vertices():
    x, y, z = mesh.vertex_attributes(vertex, "xyz")  # type: ignore
    mesh.vertex_attributes(vertex, "xyz", [x, -z, y])

# ==============================================================================
# Mapping: 3D Mesh, 2D Pattern, UV
# ==============================================================================

mesh_mapped = map_pattern_to_mesh("ZigZag", mesh, clip_boundaries=True, tolerance=1e-6, pattern_u=16, pattern_v=16)

# ==============================================================================
# Viewer
# ==============================================================================

config = Config()
config.camera.target = [0, 0, 0]
config.camera.position = [0.75, 0, 0.75]

viewer = Viewer(config=config)

# viewer.scene.add(mesh, name="mesh", show_faces=False, linecolor=Color.grey(), opacity=0.2)
viewer.scene.add(mesh_mapped, name="mesh_mapped", facecolor=Color.red())

viewer.show()
