import numpy as np
from compas.plugins import plugin

from compas_libigl import _geodistance


@plugin(category="trimesh")
def trimesh_geodistance(M, source, method="exact"):
    """Compute the geodesic distance from a source point to all vertices.

    Calculates the geodesic distance from a single source vertex to all other
    vertices in the mesh using either exact or heat method.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles
    source : int
        The index of the source vertex.
    method : str, optional
        The method to use for geodesic distance computation.
        Options:
        * 'exact': Use exact geodesic algorithm
        * 'heat': Use heat method (faster but approximate)
        Default is 'exact'.

    Returns
    -------
    list[float]
        The geodesic distances from the source to all vertices.

    Raises
    ------
    NotImplementedError
        If method is not one of {'exact', 'heat'}.
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    # Extract single integer from source array if needed
    source = int(source)  # Ensure it's a scalar
    return _geodistance.trimesh_geodistance(V, F, source, method)


@plugin(category="trimesh")
def trimesh_geodistance_multiple(M, sources, method="exact"):
    """Compute the geodesic distance from multiple source points.

    Calculates the minimum geodesic distance from any of the source vertices
    to all other vertices in the mesh.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles
    sources : list[int]
        The indices of the source vertices.
    method : str, optional
        The method to use for geodesic distance computation.
        Options:
        * 'exact': Use exact geodesic algorithm
        * 'heat': Use heat method (faster but approximate)
        Default is 'exact'.

    Returns
    -------
    list[float]
        The minimum geodesic distances from any source to all vertices.

    Raises
    ------
    NotImplementedError
        If method is not one of {'exact', 'heat'}.
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    sources = np.asarray(sources, dtype=np.int32)
    return _geodistance.trimesh_geodistance_multiple(V, F, sources, method)
