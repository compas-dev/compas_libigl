import numpy as np
from compas_libigl_parametrisation import (
    trimesh_harmonic_map as _harmonic,
    trimesh_lscm as _lscm,
)
from compas.plugins import plugin


@plugin(category="trimesh")
def trimesh_harmonic(M):
    """Compute the harmonic parametrisation of a triangle mesh within a fixed circular boundary.

    Parameters
    ----------
    M : tuple
        A mesh represented by a list of vertices and a list of faces
        or by a COMPAS mesh object.

    Returns
    -------
    array
        The u, v parameters per vertex.

    Examples
    --------
    >>> import compas_libigl as igl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(igl.get('camelhead.off'))
    >>> mesh_uv = mesh.copy()
    >>> mesh_uv.vertices_attribute('z', 0)
    >>> M = mesh.to_vertices_and_faces()
    >>> uv = igl.trimesh_harmonic(M)
    >>> for key in mesh.vertices():
    ...     mesh_uv.vertex_attributes(key, 'xy', uv[key])
    ...
    >>>

    Notes
    -----
    ``camelhead.off`` can be downloaded from https://raw.githubusercontent.com/libigl/libigl-tutorial-data/master/camelhead.off

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _harmonic(V, F)


@plugin(category="trimesh")
def trimesh_lscm(M):
    """Compute the least squares conformal map of a triangle mesh.

    Parameters
    ----------
    M : tuple
        A mesh represented by a list of vertices and a list of faces
        or by a COMPAS mesh object.

    Returns
    -------
    array
        The u, v parameters per vertex.

    Examples
    --------
    >>> import compas_libigl as igl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(igl.get('camelhead.off'))
    >>> mesh_uv = mesh.copy()
    >>> mesh_uv.vertices_attribute('z', 0)
    >>> M = mesh.to_vertices_and_faces()
    >>> uv = igl.trimesh_lscm(M)
    >>> for key in mesh.vertices():
    ...     mesh_uv.vertex_attributes(key, 'xy', uv[key])
    ...
    >>>

    Notes
    -----
    ``camelhead.off`` can be downloaded from https://raw.githubusercontent.com/libigl/libigl-tutorial-data/master/camelhead.off

    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _lscm(V, F)
