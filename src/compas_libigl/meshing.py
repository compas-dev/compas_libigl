import numpy as np
from compas.plugins import plugin

from compas_libigl import _meshing


@plugin(category="trimesh")
def trimesh_remesh_along_isoline(M, scalars, isovalue):
    """Remesh a triangle mesh along an isoline.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a list of vertices and a list of faces.
    scalars : list[float]
        A list of scalar values, one per vertex.
    isovalue : float
        The value at which to compute the isoline.

    Returns
    -------
    tuple[list[list[float]], list[list[int]], list[int]]
        A tuple containing the new vertices, faces, and labels.
        Labels indicate which side of the isoline each vertex belongs to (0 or 1).

    Examples
    --------
    >>> import compas
    >>> import compas_libigl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(compas.get("tubemesh.off"))
    >>> mesh.quads_to_triangles()
    >>> M = mesh.to_vertices_and_faces()
    >>> scalars = mesh.vertices_attribute("z")
    >>> mean_z = sum(scalars) / len(scalars)
    >>> V2, F2, L = compas_libigl.trimesh_remesh_along_isoline(M, scalars, mean_z)
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    S = np.asarray(scalars, dtype=np.float64)
    isovalue = float(isovalue)

    return _meshing.trimesh_remesh_along_isoline(V, F, S, isovalue)


@plugin(category="trimesh")
def trimesh_remesh_along_isolines(M, scalars, isovalues):
    """Remesh a triangle mesh along multiple isolines.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a list of vertices and a list of faces.
    scalars : list[float]
        A list of scalar values, one per vertex.
    isovalues : list[float]
        A list of values at which to compute the isolines. Remeshing is performed
        sequentially for each value in the list.

    Returns
    -------
    tuple[list[list[float]], list[list[int]], list[float], list[int]]
        A tuple containing:
        - new vertices
        - faces
        - scalar values per vertex
        - face group IDs (indicates which split region each face belongs to)

    Examples
    --------
    >>> import compas
    >>> import compas_libigl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(compas.get("tubemesh.off"))
    >>> mesh.quads_to_triangles()
    >>> M = mesh.to_vertices_and_faces()
    >>> scalars = mesh.vertices_attribute("z")
    >>> z_min, z_max = min(scalars), max(scalars)
    >>> # Create 5 evenly spaced isolines
    >>> isovalues = [z_min + i * (z_max - z_min) / 5 for i in range(1, 5)]
    >>> V2, F2, S2, G2 = compas_libigl.trimesh_remesh_along_isolines(M, scalars, isovalues)
    >>> # G2 contains group IDs for each face, allowing you to split the mesh into pieces
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    S = np.asarray(scalars, dtype=np.float64)
    values = np.asarray(isovalues, dtype=np.float64)

    return _meshing.trimesh_remesh_along_isolines(V, F, S, values)
