import compas
from compas_libigl.curvature import trimesh_gaussian_curvature, trimesh_principal_curvature
from compas.datastructures import Mesh


def test_trimesh_gaussian_curvature():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    M = triangle_mesh.to_vertices_and_faces()
    K = trimesh_gaussian_curvature(M=M)
    assert len(K) == mesh.number_of_vertices()


def test_trimesh_principal_curvature():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    M = triangle_mesh.to_vertices_and_faces()
    PD1, PD2, PV1, PV2 = trimesh_principal_curvature(M=M)
    assert len(PV1) == mesh.number_of_vertices()
