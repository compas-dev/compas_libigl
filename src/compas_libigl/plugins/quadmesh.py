from __future__ import annotations

from typing import TYPE_CHECKING

from compas.plugins import plugin

if TYPE_CHECKING:
    from compas._typing import MeshType


@plugin(category="quadmesh")
def quadmesh_planarize(M: MeshType, kmax: int = 500, maxdev: float = 0.005) -> list[list[float]]:
    from compas_libigl.planarize import quadmesh_planarize as implementation

    return implementation(M, kmax, maxdev)
