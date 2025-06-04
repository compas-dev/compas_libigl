import compas
from compas_libigl.geodistance import trimesh_geodistance, trimesh_geodistance_multiple
from compas.datastructures import Mesh


def test_trimesh_geodistance():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    source = 0
    distances = trimesh_geodistance(M, source, method="exact")
    assert len(distances) == mesh.number_of_vertices()
    distances = trimesh_geodistance(M, source, method="heat")
    assert len(distances) == mesh.number_of_vertices()


def test_trimesh_geodistance_multiple():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    sources = [0, 1]
    distances = trimesh_geodistance_multiple(M, sources, method="exact")
    assert len(distances) == mesh.number_of_vertices()
    distances = trimesh_geodistance_multiple(M, sources, method="heat")
    assert len(distances) == mesh.number_of_vertices()
