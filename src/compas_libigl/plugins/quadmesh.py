from __future__ import annotations

from typing import TYPE_CHECKING

from compas.plugins import plugin

if TYPE_CHECKING:
    from compas.typing import VerticesFaces

__all__ = ["quadmesh_planarize"]


@plugin(category="quadmesh")
def quadmesh_planarize(M: VerticesFaces, kmax: int = 500, maxdev: float = 0.005) -> list[list[float]]:
    """Delegate quad-mesh planarization to the libigl implementation."""
    from compas_libigl.planarize import quadmesh_planarize as implementation

    return implementation(M, kmax, maxdev)
