from typing import Protocol
from typing import TypedDict

import numpy as np
from compas.datastructures import Mesh
from compas.typing import Float64Array
from compas.typing import IndicesLike
from compas.typing import VerticesFaces
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

from compas_libigl._mesh import as_native_index_groups
from compas_libigl._mesh import as_native_index_vector
from compas_libigl._mesh import as_native_mesh

from . import _mapping

__all__ = ["TESSAGON_TYPES", "map_mesh", "map_pattern_to_mesh"]


class _TessagonMesh(TypedDict):
    vert_list: list[list[float]]
    face_list: list[list[int]]


class _TessagonInstance(Protocol):
    def create_mesh(self) -> _TessagonMesh: ...


class _TessagonFactory(Protocol):
    def __call__(self, **kwargs: object) -> _TessagonInstance: ...


TESSAGON_TYPES: dict[str, _TessagonFactory] = {
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


def map_mesh(
    target_mesh: VerticesFaces,
    pattern_mesh: VerticesFaces,
    clip_boundaries: bool = True,
    simplify_borders: bool = True,
    fixed_vertices: IndicesLike | None = None,
    tolerance: float = 1e-6,
) -> tuple[Float64Array, list[list[int]], Float64Array, list[bool], list[int]]:
    """Map a 2D pattern mesh onto a 3D target.

    Parameters
    ----------
    target_mesh
        A tuple of (vertices, faces) representing the target mesh.
    pattern_mesh
        A tuple of (vertices, faces) representing the pattern mesh.
    clip_boundaries
        Whether to clip the pattern mesh to the boundaries of the target mesh.
        Default is True.
    simplify_borders
        Whether to simplify the border of the pattern mesh.
        Default is True.
    fixed_vertices
        Fixed vertex indices on the target mesh.
        Default is None.
    tolerance
        The tolerance for point comparison, to remove duplicates.
        Default is 1e-6.

    Returns
    -------
    tuple[numpy.ndarray, list[list[int]], numpy.ndarray, list[bool], list[int]]
        A tuple containing:

        * `vertices`: the 3D coordinates of the mapped mesh vertices.
        * `faces`: the faces of the mapped mesh.
        * `normals`: the normal vector at every vertex.
        * `boundary_flags`: whether every vertex is on the boundary.
        * `polygon_groups`: grouping indices for polygons that form holes.

    """
    v_numpy, f_numpy = as_native_mesh(target_mesh, "target_mesh")
    pv, pf = pattern_mesh
    pattern_v_numpy = np.ascontiguousarray(pv, dtype=np.float64)
    if pattern_v_numpy.ndim != 2 or pattern_v_numpy.shape[1] not in (2, 3):
        raise ValueError("pattern_mesh vertices should have shape (N, 2) or (N, 3).")
    if not np.isfinite(pattern_v_numpy).all():
        raise ValueError("pattern_mesh vertices should be finite.")
    pattern_f_native = as_native_index_groups(pf, "pattern_mesh faces")

    # Handle fixed_vertices - provide empty array if None

    if fixed_vertices is None:
        fixed_vertices_native: list[int] = []
    else:
        fixed_vertices_native = as_native_index_vector(fixed_vertices, "fixed_vertices")

    # Perform the mapping
    pv_numpy_copy, pf_numpy_cleaned, p_normals, pattern_is_boundary, pattern_groups = _mapping.map_mesh_with_automatic_parameterization(
        v_numpy, f_numpy, pattern_v_numpy, pattern_f_native, clip_boundaries, simplify_borders, fixed_vertices_native, tolerance
    )

    # Return the result as a tuple
    return pv_numpy_copy, pf_numpy_cleaned, p_normals, pattern_is_boundary, pattern_groups


def map_pattern_to_mesh(
    name: str,
    mesh: Mesh,
    clip_boundaries: bool = True,
    tolerance: float = 1e-6,
    pattern_u: int = 16,
    pattern_v: int = 16,
    simplify_borders: bool = True,
    fixed_vertices: IndicesLike | None = None,
) -> Mesh:
    """Map a 2D pattern mesh onto a 3D target.

    Parameters
    ----------
    name
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

    mesh
        The target mesh.
    clip_boundaries
        Whether to clip the pattern mesh to the boundaries of the target mesh.
        Default is True.
    tolerance
        The tolerance for point comparison, to remove duplicates.
        Default is 1e-6.
    pattern_u
        The number of pattern vertices in the u direction.
        Default is 16.
    pattern_v
        The number of pattern vertices in the v direction.
        Default is 16.
    simplify_borders
        Whether to simplify the border of the pattern mesh.
        Default is True.
    fixed_vertices
        Fixed vertex indices on the target mesh.
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

    options: dict[str, object] = {
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
