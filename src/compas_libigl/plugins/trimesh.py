from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Literal

from compas.plugins import plugin

if TYPE_CHECKING:
    from collections.abc import Sequence

    from compas._typing import NumericArray
    from compas._typing import TriangleMeshInput


@plugin(category="trimesh", pluggable_name="_trimesh_geodistance")
def trimesh_geodistance(
    mesh: TriangleMeshInput,
    source: int,
    method: Literal["exact", "heat"] = "exact",
) -> list[float]:
    from compas_libigl.geodistance import trimesh_geodistance as implementation

    return implementation(mesh, source, method)


@plugin(category="trimesh", pluggable_name="_trimesh_isolines")
def trimesh_isolines(
    mesh: TriangleMeshInput,
    scalarfield: Sequence[float] | NumericArray,
    number_of_isolines: int = 50,
) -> tuple[list[list[float]], list[list[int]]]:
    from compas_libigl.isolines import trimesh_isolines as implementation

    return implementation(mesh, scalarfield, number_of_isolines)


@plugin(category="trimesh", pluggable_name="_trimesh_massmatrix")
def trimesh_massmatrix(mesh: TriangleMeshInput) -> list[float]:
    from compas_libigl.massmatrix import trimesh_massmatrix as implementation

    return implementation(mesh)


@plugin(category="trimesh", pluggable_name="_trimesh_remesh_along_isoline")
def trimesh_remesh_along_isoline(
    mesh: TriangleMeshInput,
    scalarfield: Sequence[float] | NumericArray,
    scalar: float,
) -> TriangleMeshInput:
    from compas_libigl.meshing import trimesh_remesh_along_isoline as implementation

    return implementation(mesh, scalarfield, scalar)


@plugin(category="trimesh", pluggable_name="_trimesh_harmonic")
def trimesh_harmonic(mesh: TriangleMeshInput) -> list[list[float]]:
    from compas_libigl.parametrisation import trimesh_harmonic as implementation

    return implementation(mesh)


@plugin(category="trimesh", pluggable_name="_trimesh_lscm")
def trimesh_lscm(mesh: TriangleMeshInput) -> list[list[float]]:
    from compas_libigl.parametrisation import trimesh_lscm as implementation

    return implementation(mesh)
