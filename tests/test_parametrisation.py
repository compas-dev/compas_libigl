import compas
import compas_libigl as igl
from compas.datastructures import Mesh


def test_trimesh_harmonic():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    uv = igl.trimesh_harmonic(M)
    assert len(uv) == mesh.number_of_vertices()
    assert len(uv[0]) == 2  # Each UV coordinate should be 2D


def test_trimesh_lscm():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    uv = igl.trimesh_lscm(M)
    assert len(uv) == mesh.number_of_vertices()
    assert len(uv[0]) == 2  # Each UV coordinate should be 2D
