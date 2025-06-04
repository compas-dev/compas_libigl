import numpy as np

from compas_libigl import _mapping


def map_mesh(target_mesh, pattern_mesh, clip_boundaries=True, tolerance=1e-6):
    """
    Map a 2D pattern mesh onto a 3D target.

    Parameters
    ----------
    target_mesh : tuple
        A tuple of (vertices, faces) representing the target mesh.
        vertices : list[list[float]]
            The vertices of the target mesh.
        faces : list[list[int]]
            The triangle faces of the target mesh.
        clip_boundaries : bool
            Whether to clip the pattern mesh to the boundaries of the target mesh.
        tolerance : float
            The tolerance for point comparison, to remove duplicates.
    pattern_mesh : tuple
        A tuple of (vertices, faces) representing the pattern mesh.
        vertices : list[list[float]]
            The vertices of the pattern mesh.
        faces : list[list[int]]
            The polygonal faces of the pattern mesh.

    Returns
    -------
    tuple
        A tuple containing (vertices, faces) of the mapped pattern mesh.
    """
    # Unpack mesh tuples
    v, f = target_mesh
    pv, pf = pattern_mesh

    # Convert to numpy arrays
    v_numpy = np.array(v, dtype=np.float64)
    f_numpy = np.array(f, dtype=np.int32)
    pattern_v_numpy = np.array(pv, dtype=np.float64)

    # Perform the mapping
    pattern_v_numpy_copy, pattern_f_numpy_cleaned = _mapping.map_mesh_with_automatic_parameterization(v_numpy, f_numpy, pattern_v_numpy, pf, clip_boundaries, tolerance)

    # Return the result as a tuple
    return pattern_v_numpy_copy, pattern_f_numpy_cleaned
