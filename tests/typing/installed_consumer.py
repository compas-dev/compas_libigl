"""External installed-package consumer for public and plugin typing."""

from compas_libigl.geodistance import trimesh_geodistance
from compas_libigl.intersections import intersection_ray_mesh
from compas_libigl.isolines import trimesh_isolines
from compas_libigl.massmatrix import trimesh_massmatrix
from compas_libigl.meshing import trimesh_remesh_along_isoline
from compas_libigl.parametrisation import trimesh_harmonic
from compas_libigl.parametrisation import trimesh_lscm
from compas_libigl.planarize import quadmesh_planarize
from compas_libigl.plugins.intersections import intersection_ray_mesh as plugin_intersection_ray_mesh
from compas_libigl.plugins.quadmesh import quadmesh_planarize as plugin_quadmesh_planarize
from compas_libigl.plugins.trimesh import trimesh_geodistance as plugin_trimesh_geodistance
from compas_libigl.plugins.trimesh import trimesh_harmonic as plugin_trimesh_harmonic
from compas_libigl.plugins.trimesh import trimesh_isolines as plugin_trimesh_isolines
from compas_libigl.plugins.trimesh import trimesh_lscm as plugin_trimesh_lscm
from compas_libigl.plugins.trimesh import trimesh_massmatrix as plugin_trimesh_massmatrix
from compas_libigl.plugins.trimesh import trimesh_remesh_along_isoline as plugin_trimesh_remesh_along_isoline


triangle_mesh = (
    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
    [[0, 1, 2]],
)
quad_mesh = (
    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
    [[0, 1, 2, 3]],
)
ray = ((0.0, 0.0, 1.0), (0.0, 0.0, -1.0))

distances: list[float] = trimesh_geodistance(triangle_mesh, 0)
plugin_distances: list[float] = plugin_trimesh_geodistance(triangle_mesh, 0)
hits = intersection_ray_mesh(ray, triangle_mesh)
plugin_hits = plugin_intersection_ray_mesh(ray, triangle_mesh)
isolines: tuple[list[list[float]], list[list[int]]] = trimesh_isolines(triangle_mesh, [0.0, 1.0, 2.0], 2)
plugin_isolines: tuple[list[list[float]], list[list[int]]] = plugin_trimesh_isolines(triangle_mesh, [0.0, 1.0, 2.0], 2)
masses: list[float] = trimesh_massmatrix(triangle_mesh)
plugin_masses: list[float] = plugin_trimesh_massmatrix(triangle_mesh)
remeshed = trimesh_remesh_along_isoline(triangle_mesh, [0.0, 1.0, 2.0], 0.5)
plugin_remeshed = plugin_trimesh_remesh_along_isoline(triangle_mesh, [0.0, 1.0, 2.0], 0.5)
harmonic: list[list[float]] = trimesh_harmonic(triangle_mesh)
plugin_harmonic: list[list[float]] = plugin_trimesh_harmonic(triangle_mesh)
lscm: list[list[float]] = trimesh_lscm(triangle_mesh)
plugin_lscm: list[list[float]] = plugin_trimesh_lscm(triangle_mesh)
vertices: list[list[float]] = quadmesh_planarize(quad_mesh)
plugin_vertices: list[list[float]] = plugin_quadmesh_planarize(quad_mesh)
