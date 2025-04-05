import compas
import compas_libigl as libigl
from compas.datastructures import Mesh


def test_trimesh_gaussian_curvature():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    K = libigl.trimesh_gaussian_curvature(M)
    assert len(K) == mesh.number_of_vertices()


def test_trimesh_principal_curvature():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    PD1, PD2, PV1, PV2 = libigl.trimesh_principal_curvature(M)
    assert len(PV1) == mesh.number_of_vertices()
