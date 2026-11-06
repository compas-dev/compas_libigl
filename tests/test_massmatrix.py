import compas
from compas_libigl.massmatrix import trimesh_massmatrix
from compas.datastructures import Mesh


def test_trimesh_massmatrix():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    mass = trimesh_massmatrix(triangle_mesh.to_vertices_and_faces())
    assert len(mass) == mesh.number_of_vertices()
