import compas
from compas.datastructures import Mesh
from compas.geometry import FaceTriangulation
from compas_libigl.parametrisation import trimesh_harmonic
from compas_libigl.parametrisation import trimesh_lscm


def test_trimesh_harmonic():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    tessellation = mesh.triangulated(FaceTriangulation())
    uv = trimesh_harmonic(tessellation)
    assert len(uv) == mesh.number_of_vertices()
    assert len(uv[0]) == 2  # Each UV coordinate should be 2D


def test_trimesh_lscm():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    tessellation = mesh.triangulated(FaceTriangulation())
    uv = trimesh_lscm(tessellation)
    assert len(uv) == mesh.number_of_vertices()
    assert len(uv[0]) == 2  # Each UV coordinate should be 2D
