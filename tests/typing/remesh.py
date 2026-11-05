"""Static consumer coverage for raw remesh-along-isoline buffers."""

import numpy as np

from compas_libigl.meshing import trimesh_remesh_along_isoline

vertices32 = np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)
vertices64 = np.asarray(vertices32, dtype=np.float64)
faces32 = np.asarray([[0, 1, 2]], dtype=np.int32)
faces64 = np.asarray(faces32, dtype=np.int64)

trimesh_remesh_along_isoline((vertices32, faces64), [0.0, 1.0, 2.0], 0.5)
trimesh_remesh_along_isoline((vertices64, faces32), [0.0, 1.0, 2.0], 0.5)
trimesh_remesh_along_isoline((vertices64, faces32), np.asarray([0.0, 1.0, 2.0]), 0.5)
