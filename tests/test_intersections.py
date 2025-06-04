import compas
from compas_libigl.intersections import intersection_ray_mesh, intersection_rays_mesh
from compas.datastructures import Mesh
from compas.geometry import add_vectors, scale_vector


def test_intersection_ray_mesh():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    centroid = mesh.centroid()
    ray = [centroid[0], centroid[1], 0], [0, 0, 1.0]
    hits = intersection_ray_mesh(ray, M)
    assert len(hits) == 1
    # Test computing intersection point
    point = add_vectors(ray[0], scale_vector(ray[1], hits[0][3]))
    assert len(point) == 3


def test_intersection_rays_mesh():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    centroid = mesh.centroid()
    rays = [([centroid[0], centroid[1], 0], [0, 0, 1.0]), ([centroid[0], centroid[1], 1], [0, 0, -1.0])]
    hits = intersection_rays_mesh(rays, M)
    assert len(hits) == 2
