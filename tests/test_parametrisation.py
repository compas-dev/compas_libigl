import compas
import compas_libigl as igl
from compas.datastructures import Mesh


def test_trimesh_harmonic_mapping():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    uv = igl.trimesh_harmonic_mapping(M)
    assert len(uv) == mesh.number_of_vertices()
    assert len(uv[0]) == 2  # Each UV coordinate should be 2D


def test_trimesh_lsc_mapping():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    uv = igl.trimesh_lsc_mapping(M)
    assert len(uv) == mesh.number_of_vertices()
    assert len(uv[0]) == 2  # Each UV coordinate should be 2D
