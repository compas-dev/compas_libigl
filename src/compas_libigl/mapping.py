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

from compas_libigl import _mapping
from compas_libigl._types_std import VectorVectorInt  # noqa: F401


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


def map_pattern_to_mesh(name, mesh, clip_boundaries=True, tolerance=1e-6, pattern_u=16, pattern_v=16):
    """
    Map a 2D pattern mesh onto a 3D target.

    Parameters
    ----------
    name : str
        The name of the pattern to be created. Options are:
        "Hex",
        "Tri",
        "Octo",
        "Square",
        "Rhombus",
        "HexTri",
        "DissectedSquare",
        "DissectedTriangle",
        "DissectedHexQuad",
        "DissectedHexTri",
        "Floret",
        "Pythagorean",
        "Brick",
        "Weave",
        "ZigZag",
        "HexBigTri",
        "Dodeca",
        "SquareTri"
    mesh : compas.datastructures.Mesh
        The target mesh.
    clip_boundaries : bool
        Whether to clip the pattern mesh to the boundaries of the target mesh.
    tolerance : float
        The tolerance for point comparison, to remove duplicates.
    pattern_u : int
        The number of pattern vertices in the u direction.
    pattern_v : int
        The number of pattern vertices in the v direction.

    Returns
    -------
    compas.datastructures.Mesh
        The mapped pattern mesh.
    """

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
    mv, mf = map_mesh((v, f), (pv, pf), clip_boundaries=clip_boundaries, tolerance=tolerance)

    return Mesh.from_vertices_and_faces(mv, mf)
