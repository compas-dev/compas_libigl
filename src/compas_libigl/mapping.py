import numpy as np

from compas_libigl import _mapping


def trimesh_map_simple(M_target, M_pattern, UV_target):
    """Map a 2D pattern mesh onto a 3D target mesh using simple UV parameterization.

    Parameters
    ----------
    M_target : tuple[list[list[float]], list[list[int]]]
        A target mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles
    M_pattern : tuple[list[list[float]], list[list[int]]]
        A pattern mesh represented by a tuple of (vertices, faces)
        where vertices are 2D or 3D points and faces are triangles
    UV_target : list[list[float]]
        UV coordinates for the target mesh vertices

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        The mapped pattern mesh as a tuple of (vertices, faces)
    """
    V_target, F_target = M_target
    V_pattern, F_pattern = M_pattern
    
    V_target = np.asarray(V_target, dtype=np.float64)
    F_target = np.asarray(F_target, dtype=np.int32)
    V_pattern = np.asarray(V_pattern, dtype=np.float64)
    F_pattern = np.asarray(F_pattern, dtype=np.int32)
    UV_target = np.asarray(UV_target, dtype=np.float64)
    
    V_result, F_result = _mapping.mapMesh3D_simple(
        V_target, F_target, V_pattern, F_pattern, UV_target)
    
    return V_result.tolist(), F_result.tolist()


def trimesh_map_aabb(M_target, M_pattern, UV_target):
    """Map a 2D pattern mesh onto a 3D target mesh using AABB tree for faster point lookup.

    Parameters
    ----------
    M_target : tuple[list[list[float]], list[list[int]]]
        A target mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles
    M_pattern : tuple[list[list[float]], list[list[int]]]
        A pattern mesh represented by a tuple of (vertices, faces)
        where vertices are 2D or 3D points and faces are triangles
    UV_target : list[list[float]]
        UV coordinates for the target mesh vertices

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        The mapped pattern mesh as a tuple of (vertices, faces)
    """
    V_target, F_target = M_target
    V_pattern, F_pattern = M_pattern
    
    V_target = np.asarray(V_target, dtype=np.float64)
    F_target = np.asarray(F_target, dtype=np.int32)
    V_pattern = np.asarray(V_pattern, dtype=np.float64)
    F_pattern = np.asarray(F_pattern, dtype=np.int32)
    UV_target = np.asarray(UV_target, dtype=np.float64)
    
    V_result, F_result = _mapping.mapMesh3D_AABB(
        V_target, F_target, V_pattern, F_pattern, UV_target)
    
    return V_result.tolist(), F_result.tolist()