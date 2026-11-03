import compas
from compas_libigl.massmatrix import trimesh_massmatrix
from compas.datastructures import Mesh
from compas.geometry import FaceTriangulation


def test_trimesh_massmatrix():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    tessellation = mesh.triangulated(FaceTriangulation())
    mass = trimesh_massmatrix(tessellation)
    assert len(mass) == mesh.number_of_vertices()
