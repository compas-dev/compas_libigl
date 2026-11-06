"""External installed-package consumer for every public wrapper and plugin."""

from typing import assert_type

import numpy as np
from scipy.sparse import csc_matrix

from compas.datastructures import Mesh
from compas.geometry import PolygonalSurface
from compas.geometry import Tessellation
from compas.typing import Float64Array
from compas.typing import Int32Array
from compas.typing import RayData
from compas.typing import VerticesFaces
from compas_libigl.boundaries import trimesh_boundaries
from compas_libigl.cotmatrix import trimesh_cotmatrix
from compas_libigl.cotmatrix import trimesh_cotmatrix_entries
from compas_libigl.curvature import trimesh_gaussian_curvature
from compas_libigl.curvature import trimesh_principal_curvature
from compas_libigl.geodistance import trimesh_geodistance
from compas_libigl.geodistance import trimesh_geodistance_multiple
from compas_libigl.grad import trimesh_grad
from compas_libigl.intersections import intersection_ray_mesh
from compas_libigl.intersections import intersection_rays_mesh
from compas_libigl.isolines import trimesh_isolines
from compas_libigl.mapping import map_mesh
from compas_libigl.mapping import map_pattern_to_mesh
from compas_libigl.massmatrix import trimesh_massmatrix
from compas_libigl.meshing import trimesh_cut_mesh
from compas_libigl.meshing import trimesh_face_components
from compas_libigl.meshing import trimesh_remesh_along_isoline
from compas_libigl.meshing import trimesh_remesh_along_isolines
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
from compas_libigl.simplify import ramer_douglas_peucker

triangle_mesh: VerticesFaces = (
    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
    [[0, 1, 2]],
)
quad_mesh: VerticesFaces = (
    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
    [[0, 1, 2, 3]],
)
ray: RayData = ((0.0, 0.0, 1.0), (0.0, 0.0, -1.0))
rays_array = np.asarray([[[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]]], dtype=np.float64)
scalarfield = [0.0, 1.0, 2.0]
mesh_object = Mesh.from_vertices_and_faces(*triangle_mesh)

assert_type(trimesh_boundaries(M=triangle_mesh), list[list[int]])
assert_type(trimesh_cotmatrix(M=triangle_mesh), csc_matrix)
assert_type(trimesh_cotmatrix_entries(M=triangle_mesh), Float64Array)
assert_type(trimesh_gaussian_curvature(M=triangle_mesh), Float64Array)
assert_type(
    trimesh_principal_curvature(M=triangle_mesh),
    tuple[list[list[float]], list[list[float]], list[float], list[float]],
)
assert_type(trimesh_geodistance(triangle_mesh, 0), list[float])
assert_type(trimesh_geodistance_multiple(M=triangle_mesh, sources=[0]), Float64Array)
assert_type(trimesh_grad(M=triangle_mesh), csc_matrix)
assert_type(intersection_ray_mesh(ray, triangle_mesh), list[tuple[int, float, float, float]])
assert_type(intersection_rays_mesh(rays=rays_array, M=triangle_mesh), list[list[tuple[int, float, float, float]]])
assert_type(trimesh_isolines(triangle_mesh, scalarfield, 2), tuple[list[list[float]], list[list[int]]])
assert_type(
    map_mesh(triangle_mesh, triangle_mesh),
    tuple[Float64Array, list[list[int]], Float64Array, list[bool], list[int]],
)
assert_type(map_pattern_to_mesh("Hex", mesh_object), Mesh)
assert_type(trimesh_massmatrix(triangle_mesh), list[float])
remeshed = assert_type(trimesh_remesh_along_isoline(triangle_mesh, scalarfield, 0.5), tuple[Float64Array, Int32Array])
assert_type(Mesh.from_vertices_and_faces(*remeshed), Mesh)
assert_type(PolygonalSurface(*remeshed), PolygonalSurface)
assert_type(Tessellation(*remeshed), Tessellation[Float64Array, Int32Array])
assert_type(
    trimesh_remesh_along_isolines(M=triangle_mesh, scalars=scalarfield, isovalues=[0.5]),
    tuple[list[list[float]], list[list[int]], list[float], list[int]],
)
assert_type(trimesh_cut_mesh(M=triangle_mesh, cuts=[[0, 0, 0]]), tuple[list[list[float]], list[list[int]]])
assert_type(trimesh_face_components(M=triangle_mesh), list[int])
assert_type(trimesh_harmonic(triangle_mesh), list[list[float]])
assert_type(trimesh_lscm(triangle_mesh), list[list[float]])
assert_type(quadmesh_planarize(quad_mesh), list[list[float]])
assert_type(
    ramer_douglas_peucker(triangle_mesh[0], 0.1),
    tuple[list[list[float]], list[int], list[list[float]]],
)

assert_type(plugin_intersection_ray_mesh(ray, triangle_mesh), list[tuple[int, float, float, float]])
assert_type(plugin_quadmesh_planarize(quad_mesh), list[list[float]])
assert_type(plugin_trimesh_geodistance(triangle_mesh, 0), list[float])
assert_type(plugin_trimesh_harmonic(triangle_mesh), list[list[float]])
assert_type(plugin_trimesh_isolines(triangle_mesh, scalarfield, 2), tuple[list[list[float]], list[list[int]]])
assert_type(plugin_trimesh_lscm(triangle_mesh), list[list[float]])
assert_type(plugin_trimesh_massmatrix(triangle_mesh), list[float])
assert_type(
    plugin_trimesh_remesh_along_isoline(triangle_mesh, scalarfield, 0.5),
    tuple[Float64Array, Int32Array],
)
