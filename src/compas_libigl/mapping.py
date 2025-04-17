import numpy as np
from compas.datastructures import Mesh

from compas_libigl import _mapping


def map_mesh(v, f, uv, pv, pf, p_uv):
    """Map a 2D pattern mesh onto a 3D target mesh using simple UV parameterization.

    Parameters
    ----------
    v : list[list[float]]
        The vertices of the target mesh.
    f : list[list[int]]
        The faces of the target mesh.
    uv : list[list[float]]
        The UV coordinates of the target mesh.
    pv : list[list[float]]
        The vertices of the pattern mesh.
    pf : list[list[int]]
        The faces of the pattern mesh.
    p_uv : list[list[float]]
        The UV coordinates of the pattern mesh.

    Returns
    -------
    pattern_mapped_cleaned : compas.datastructures.Mesh
        The mapped pattern mesh.
    """

    v_numpy = np.array(v, dtype=np.float64)
    f_numpy = np.array(f, dtype=np.int32)
    uv_numpy = np.array(uv, dtype=np.float64)
    pattern_v_numpy = np.array(pv, dtype=np.float64)
    pattern_f_numpy = np.array(pf, dtype=np.int32)
    p_uv_numpy = np.array(p_uv, dtype=np.float64)

    # Call the mapping function with the new signature (returns a tuple)
    pattern_f_numpy_cleaned = _mapping.map_mesh(v_numpy, f_numpy, uv_numpy, pattern_v_numpy, pattern_f_numpy, p_uv_numpy)

    pattern_mapped_cleaned = Mesh.from_vertices_and_faces(pattern_v_numpy, pattern_f_numpy_cleaned)
    return pattern_mapped_cleaned
