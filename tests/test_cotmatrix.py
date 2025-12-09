import compas
from compas_libigl.cotmatrix import trimesh_cotmatrix, trimesh_cotmatrix_entries
from compas.datastructures import Mesh


def test_trimesh_cotmatrix():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    L = trimesh_cotmatrix(M)
    # Cotmatrix is V x V sparse matrix
    assert L.shape[0] == mesh.number_of_vertices()
    assert L.shape[1] == mesh.number_of_vertices()


def test_trimesh_cotmatrix_entries():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    C = trimesh_cotmatrix_entries(M)
    # Cotmatrix entries is F x 3 (one cotan per edge per face)
    assert C.shape[0] == mesh.number_of_faces()
    assert C.shape[1] == 3
