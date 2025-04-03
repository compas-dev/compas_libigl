import compas
import compas_libigl
from compas.datastructures import Mesh


def test_trimesh_massmatrix():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    mass = compas_libigl.trimesh_massmatrix(M)
    assert mass.shape[0] == mesh.number_of_vertices()  # Use shape[0] for sparse matrix length
