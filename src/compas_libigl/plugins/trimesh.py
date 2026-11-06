from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Literal

from compas.plugins import plugin

if TYPE_CHECKING:
    from compas.typing import FloatSequenceLike
    from compas.typing import VerticesFaces

    from compas_libigl._mesh import NativeTriangleMesh

__all__ = [
    "trimesh_geodistance",
    "trimesh_harmonic",
    "trimesh_isolines",
    "trimesh_lscm",
    "trimesh_massmatrix",
    "trimesh_remesh_along_isoline",
]


@plugin(category="trimesh", pluggable_name="_trimesh_geodistance")
def trimesh_geodistance(
    mesh: VerticesFaces,
    source: int,
    method: Literal["exact", "heat"] = "exact",
) -> list[float]:
    """Delegate triangle-mesh geodesic distance to libigl."""
    from compas_libigl.geodistance import trimesh_geodistance as implementation

    return implementation(mesh, source, method)


@plugin(category="trimesh", pluggable_name="_trimesh_isolines")
def trimesh_isolines(
    mesh: VerticesFaces,
    scalarfield: FloatSequenceLike,
    number_of_isolines: int = 50,
) -> tuple[list[list[float]], list[list[int]]]:
    """Delegate triangle-mesh isoline extraction to libigl."""
    from compas_libigl.isolines import trimesh_isolines as implementation

    return implementation(mesh, scalarfield, number_of_isolines)


@plugin(category="trimesh", pluggable_name="_trimesh_massmatrix")
def trimesh_massmatrix(mesh: VerticesFaces) -> list[float]:
    """Delegate triangle-mesh mass computation to libigl."""
    from compas_libigl.massmatrix import trimesh_massmatrix as implementation

    return implementation(mesh)


@plugin(category="trimesh", pluggable_name="_trimesh_remesh_along_isoline")
def trimesh_remesh_along_isoline(
    mesh: VerticesFaces,
    scalarfield: FloatSequenceLike,
    scalar: float,
) -> NativeTriangleMesh:
    """Delegate remeshing along an isoline to libigl."""
    from compas_libigl.meshing import trimesh_remesh_along_isoline as implementation

    return implementation(mesh, scalarfield, scalar)


@plugin(category="trimesh", pluggable_name="_trimesh_harmonic")
def trimesh_harmonic(mesh: VerticesFaces) -> list[list[float]]:
    """Delegate harmonic parameterization to libigl."""
    from compas_libigl.parametrisation import trimesh_harmonic as implementation

    return implementation(mesh)


@plugin(category="trimesh", pluggable_name="_trimesh_lscm")
def trimesh_lscm(mesh: VerticesFaces) -> list[list[float]]:
    """Delegate least-squares conformal mapping to libigl."""
    from compas_libigl.parametrisation import trimesh_lscm as implementation

    return implementation(mesh)
