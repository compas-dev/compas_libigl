import compas
from compas_libigl.boundaries import trimesh_boundaries
from compas.datastructures import Mesh
from compas.geometry import FaceTriangulation


def test_trimesh_boundaries():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.triangulate(FaceTriangulation())
    M = mesh.to_vertices_and_faces()
    boundaries = trimesh_boundaries(M)
    assert len(boundaries) == 1
