from importlib.metadata import distribution
import subprocess
import sys
from types import ModuleType

from compas.plugins import ExtensionPoint
from compas.plugins import PluginManager


def installed_plugin_entry_points():
    return [entry_point for entry_point in distribution("compas_libigl").entry_points if entry_point.group == "compas.plugins"]


def test_installed_entry_points_discover_all_plugin_implementations():
    entry_points = installed_plugin_entry_points()
    manager = PluginManager(entry_points_provider=lambda *, group: entry_points)

    assert manager.load_plugins() == 8

    registered_modules = {plugin.plugin.__name__ for implementations in manager.registry.values() for plugin in implementations}
    assert registered_modules == {
        "compas_libigl.plugins.intersections",
        "compas_libigl.plugins.quadmesh",
        "compas_libigl.plugins.trimesh",
    }
    assert "compas_libigl.curvature" not in registered_modules

    planarize = manager.select(
        ExtensionPoint(
            domain="https://plugins.compas.dev/",
            category="quadmesh",
            name="quadmesh_planarize",
        )
    )
    assert planarize is not None
    assert planarize.id == "compas_libigl.plugins.quadmesh.quadmesh_planarize"


def test_discovery_does_not_import_implementations_or_native_modules():
    script = """
import sys
from importlib.metadata import distribution
from compas.plugins import PluginManager

implementation_modules = {
    "compas_libigl.geodistance",
    "compas_libigl.intersections",
    "compas_libigl.isolines",
    "compas_libigl.massmatrix",
    "compas_libigl.meshing",
    "compas_libigl.parametrisation",
    "compas_libigl.planarize",
}
entry_points = [entry_point for entry_point in distribution("compas_libigl").entry_points if entry_point.group == "compas.plugins"]
manager = PluginManager(entry_points_provider=lambda *, group: entry_points)
assert manager.load_plugins() == 8
unexpected = sorted(
    name
    for name in sys.modules
    if name in implementation_modules or name.startswith("compas_libigl._")
)
assert not unexpected, unexpected
"""

    subprocess.run([sys.executable, "-c", script], check=True, capture_output=True, text=True)


def test_lightweight_plugins_delegate_lazily(monkeypatch):
    from compas_libigl.plugins import quadmesh
    from compas_libigl.plugins import trimesh

    calls = []
    planarize = ModuleType("compas_libigl.planarize")
    setattr(planarize, "quadmesh_planarize", lambda M, kmax, maxdev: calls.append(("planarize", M, kmax, maxdev)) or [[0.0, 0.0, 0.0]])
    geodistance = ModuleType("compas_libigl.geodistance")
    setattr(geodistance, "trimesh_geodistance", lambda mesh, source, method: calls.append(("geodistance", mesh, source, method)) or [0.0])
    monkeypatch.setitem(sys.modules, "compas_libigl.planarize", planarize)
    monkeypatch.setitem(sys.modules, "compas_libigl.geodistance", geodistance)

    mesh = ([[0.0, 0.0, 0.0]], [[0, 0, 0]])
    assert quadmesh.quadmesh_planarize(mesh, 2, 0.01) == [[0.0, 0.0, 0.0]]
    assert trimesh.trimesh_geodistance(mesh, 0, "exact") == [0.0]
    assert calls == [
        ("planarize", mesh, 2, 0.01),
        ("geodistance", mesh, 0, "exact"),
    ]
