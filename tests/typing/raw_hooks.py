"""Static consumer coverage for raw libigl plugin boundaries."""

import numpy as np

from compas_libigl.geodistance import trimesh_geodistance
from compas_libigl.intersections import intersection_ray_mesh
from compas_libigl.isolines import trimesh_isolines
from compas_libigl.massmatrix import trimesh_massmatrix
from compas_libigl.parametrisation import trimesh_harmonic
from compas_libigl.parametrisation import trimesh_lscm

vertices = np.asarray([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], dtype=np.float32)
triangles = np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64)
mesh = (vertices, triangles)

intersection_ray_mesh(([0.5, 0.5, -1.0], [0.0, 0.0, 1.0]), mesh)
trimesh_geodistance(mesh, 0, "exact")
trimesh_isolines(mesh, np.asarray([0.0, 1.0, 1.0, 0.0]), 2)
trimesh_massmatrix(mesh)
trimesh_harmonic(mesh)
trimesh_lscm(mesh)
