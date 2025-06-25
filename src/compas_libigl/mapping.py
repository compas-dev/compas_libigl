import numpy as np
from compas.datastructures import Mesh
from tessagon.adaptors.list_adaptor import ListAdaptor
from tessagon.types.brick_tessagon import BrickTessagon
from tessagon.types.dissected_hex_quad_tessagon import DissectedHexQuadTessagon
from tessagon.types.dissected_hex_tri_tessagon import DissectedHexTriTessagon
from tessagon.types.dissected_square_tessagon import DissectedSquareTessagon
from tessagon.types.dissected_triangle_tessagon import DissectedTriangleTessagon
from tessagon.types.dodeca_tessagon import DodecaTessagon
from tessagon.types.floret_tessagon import FloretTessagon
from tessagon.types.hex_big_tri_tessagon import HexBigTriTessagon
from tessagon.types.hex_tessagon import HexTessagon
from tessagon.types.hex_tri_tessagon import HexTriTessagon
from tessagon.types.octo_tessagon import OctoTessagon
from tessagon.types.pythagorean_tessagon import PythagoreanTessagon
from tessagon.types.rhombus_tessagon import RhombusTessagon
from tessagon.types.square_tessagon import SquareTessagon
from tessagon.types.square_tri_tessagon import SquareTriTessagon
from tessagon.types.tri_tessagon import TriTessagon
from tessagon.types.weave_tessagon import WeaveTessagon
from tessagon.types.zig_zag_tessagon import ZigZagTessagon

from compas_libigl import _mapping  # type: ignore

TESSAGON_TYPES = {
    "Hex": HexTessagon,
    "Tri": TriTessagon,
    "Octo": OctoTessagon,
    "Square": SquareTessagon,
    "Rhombus": RhombusTessagon,
    "HexTri": HexTriTessagon,
    "DissectedSquare": DissectedSquareTessagon,
    "DissectedTriangle": DissectedTriangleTessagon,
    "DissectedHexQuad": DissectedHexQuadTessagon,
    "DissectedHexTri": DissectedHexTriTessagon,
    "Floret": FloretTessagon,
    "Pythagorean": PythagoreanTessagon,
    "Brick": BrickTessagon,
    "Weave": WeaveTessagon,
    "ZigZag": ZigZagTessagon,
    "HexBigTri": HexBigTriTessagon,
    "Dodeca": DodecaTessagon,
    "SquareTri": SquareTriTessagon,
}


def map_mesh(target_mesh, pattern_mesh, clip_boundaries=True, simplify_borders=True, fixed_vertices=None, tolerance=1e-6):
    """
    Map a 2D pattern mesh onto a 3D target.

    Parameters
    ----------
    target_mesh : tuple[list[list[float]], list[list[int]]]
        A tuple of (vertices, faces) representing the target mesh.
    pattern_mesh : tuple[list[list[float]], list[list[int]]]
        A tuple of (vertices, faces) representing the pattern mesh.
    clip_boundaries : bool, optional
        Whether to clip the pattern mesh to the boundaries of the target mesh.
        Default is True.
    simplify_borders : bool, optional
        Whether to simplify the border of the pattern mesh.
        Default is True.
    fixed_vertices : list[list[float]], optional
        A list of fixed points on the target mesh.
        Default is None.
    tolerance : float, optional
        The tolerance for point comparison, to remove duplicates.
        Default is 1e-6.

    Returns
    -------
    tuple[ndarray, VectorVectorInt, ndarray, VectorBool, VectorInt]
        A tuple containing:

        * vertices: ndarray - The 3D coordinates of the mapped mesh vertices
        * faces: VectorVectorInt - The faces of the mapped mesh
        * normals: ndarray - The normal vectors at each vertex
        * boundary_flags: VectorBool - Boolean flags indicating if vertices are on the boundary
        * polygon_groups: VectorInt - Grouping indices for polygons (to form holes)
    """
    # Unpack mesh tuples
    v, f = target_mesh
    pv, pf = pattern_mesh

    # Convert to numpy arrays
    v_numpy = np.array(v, dtype=np.float64)
    f_numpy = np.array(f, dtype=np.int32)
    pattern_v_numpy = np.array(pv, dtype=np.float64)

    # Handle fixed_vertices - provide empty array if None

    fixed_vertices_vectorint = []
    if fixed_vertices is None:
        fixed_vertices_vectorint = []
    else:
        fixed_vertices_vectorint = fixed_vertices

    # Convert pattern_f from Python list to VectorVectorInt which is expected by C++ code

    pattern_f_vec = []
    for face in pf:
        pattern_f_vec.append(face)

    # Perform the mapping
    pv_numpy_copy, pf_numpy_cleaned, p_normals, pattern_is_boundary, pattern_groups = _mapping.map_mesh_with_automatic_parameterization(
        v_numpy, f_numpy, pattern_v_numpy, pattern_f_vec, clip_boundaries, simplify_borders, fixed_vertices_vectorint, tolerance
    )

    # Return the result as a tuple
    return pv_numpy_copy, pf_numpy_cleaned, p_normals, pattern_is_boundary, pattern_groups


def map_pattern_to_mesh(name, mesh, clip_boundaries=True, tolerance=1e-6, pattern_u=16, pattern_v=16, simplify_borders=True, fixed_vertices=None):
    """
    Map a 2D pattern mesh onto a 3D target.

    Parameters
    ----------
    name : str
        The name of the pattern to be created. Options are:

        * "Hex"
        * "Tri"
        * "Octo"
        * "Square"
        * "Rhombus"
        * "HexTri"
        * "DissectedSquare"
        * "DissectedTriangle"
        * "DissectedHexQuad"
        * "DissectedHexTri"
        * "Floret"
        * "Pythagorean"
        * "Brick"
        * "Weave"
        * "ZigZag"
        * "HexBigTri"
        * "Dodeca"
        * "SquareTri"

    mesh : compas.datastructures.Mesh
        The target mesh.
    clip_boundaries : bool, optional
        Whether to clip the pattern mesh to the boundaries of the target mesh.
        Default is True.
    tolerance : float, optional
        The tolerance for point comparison, to remove duplicates.
        Default is 1e-6.
    pattern_u : int, optional
        The number of pattern vertices in the u direction.
        Default is 16.
    pattern_v : int, optional
        The number of pattern vertices in the v direction.
        Default is 16.
    simplify_borders : bool, optional
        Whether to simplify the border of the pattern mesh.
        Default is True.
    fixed_vertices : list[list[float]], optional
        A list of fixed points on the target mesh.
        Default is None.

    Returns
    -------
    compas.datastructures.Mesh
        The mapped pattern mesh.

    Raises
    ------
    ValueError
        If the specified pattern name is not supported.
    """

    # Check if the provided pattern name is supported
    if name not in TESSAGON_TYPES:
        supported_names = list(TESSAGON_TYPES.keys())
        raise ValueError(f"Pattern name '{name}' is not supported. Choose from: {', '.join(supported_names)}")

    options = {
        "function": lambda u, v: [u * 1, v * 1, 0],
        "u_range": [-0.255, 1.33],
        "v_range": [-0.34, 1.33],
        "u_num": pattern_u,
        "v_num": pattern_v,
        "u_cyclic": False,
        "v_cyclic": False,
        "adaptor_class": ListAdaptor,
    }

    # Create the selected tessagon pattern
    pattern_class = TESSAGON_TYPES[name]
    tessagon = pattern_class(**options)
    tessagon_mesh = tessagon.create_mesh()
    pv = tessagon_mesh["vert_list"]
    pf = tessagon_mesh["face_list"]

    v, f = mesh.to_vertices_and_faces()
    mapped_vertices, mapped_faces, mapped_normals, mapped_is_boundary, mapped_groups = map_mesh(
        (v, f), (pv, pf), clip_boundaries=clip_boundaries, simplify_borders=simplify_borders, fixed_vertices=fixed_vertices, tolerance=tolerance
    )

    return Mesh.from_vertices_and_faces(mapped_vertices, mapped_faces)
