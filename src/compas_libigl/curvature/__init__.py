import numpy as np
from compas_libigl_curvature import trimesh_gaussian_curvature as _gaussian
from compas.plugins import plugin


@plugin(category="trimesh")
def trimesh_gaussian_curvature(M):
    """Compute the discrete gaussian curvature of a triangle mesh.

    Parameters
    ----------
    M : (list, list)
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    array
        The discrete gaussian curvature per vertex.

    Examples
    --------
    >>> import compas_libigl as igl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(igl.get('tubemesh.off'))
    >>> mesh.quads_to_triangles()
    >>> curvature = igl.trimesh_curvature(mesh)
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    return _gaussian(V, F)


def trimesh_principal_curvature():
    pass


__all__ = [_ for _ in dir() if not _.startswith('_')]
