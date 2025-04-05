import compas
import compas_libigl
from compas.datastructures import Mesh


def test_trimesh_boundaries():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    boundaries = compas_libigl.trimesh_boundaries(M)
    assert len(boundaries) == 1
