import numpy as np
import pytest
from typing import Any
from typing import cast

from compas.geometry import Tessellation
from compas_libigl._tessellation import as_libigl_tessellation


def test_libigl_tessellation_boundary_uses_native_dtypes_and_layout():
    mesh = Tessellation(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        [[0, 1, 2]],
    )

    vertices, triangles = as_libigl_tessellation(mesh)

    assert vertices.dtype == np.float64
    assert triangles.dtype == np.int32
    assert vertices.flags.c_contiguous
    assert triangles.flags.c_contiguous


def test_libigl_tessellation_boundary_rejects_public_tuple_input():
    with pytest.raises(TypeError):
        invalid_mesh = cast(Any, ([[0.0, 0.0, 0.0]], []))
        as_libigl_tessellation(invalid_mesh)
