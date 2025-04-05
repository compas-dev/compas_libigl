import compas
import compas_libigl as libigl
from compas.datastructures import Mesh


def test_trimesh_geodistance():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    source = 0
    distances = libigl.trimesh_geodistance(M, source, method="exact")
    assert len(distances) == mesh.number_of_vertices()
    distances = libigl.trimesh_geodistance(M, source, method="heat")
    assert len(distances) == mesh.number_of_vertices()


def test_trimesh_geodistance_multiple():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    sources = [0, 1]
    distances = libigl.trimesh_geodistance_multiple(M, sources, method="exact")
    assert len(distances) == mesh.number_of_vertices()
    distances = libigl.trimesh_geodistance_multiple(M, sources, method="heat")
    assert len(distances) == mesh.number_of_vertices()
