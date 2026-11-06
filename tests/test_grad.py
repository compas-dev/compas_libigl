import compas
from compas_libigl.grad import trimesh_grad
from compas.datastructures import Mesh
from compas.geometry import FaceTriangulation


def test_trimesh_grad():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.triangulate(FaceTriangulation())
    M = mesh.to_vertices_and_faces()
    G = trimesh_grad(M=M)
    # Gradient operator is (3*F) x V sparse matrix
    # When multiplied by V-length scalar field, produces 3F gradient components
    assert G.shape is not None
    assert G.shape[0] == 3 * mesh.number_of_faces()
    assert G.shape[1] == mesh.number_of_vertices()
