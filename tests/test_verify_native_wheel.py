from __future__ import annotations

import importlib.util
from pathlib import Path
from zipfile import ZipFile

import pytest

SCRIPT = Path(__file__).parents[1] / ".github" / "scripts" / "verify_native_wheel.py"
SPEC = importlib.util.spec_from_file_location("verify_native_wheel", SCRIPT)
assert SPEC
assert SPEC.loader
verify_native_wheel = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify_native_wheel)


def make_wheel(
    tmp_path: Path,
    *,
    filename_tag: str = "cp312-abi3-manylinux_2_28_x86_64",
    internal_tags: tuple[str, ...] = ("cp312-abi3-manylinux_2_28_x86_64",),
    omitted_module: str | None = None,
    omitted_stub: str | None = None,
    include_typing_marker: bool = True,
    include_metadata: bool = True,
    dependencies: tuple[str, ...] = ("compas<4,>=3.0", "numpy>=1.24", "tessagon"),
) -> Path:
    wheel = tmp_path / f"compas_libigl-0.7.6-{filename_tag}.whl"
    with ZipFile(wheel, "w") as archive:
        if include_typing_marker:
            archive.writestr(verify_native_wheel.TYPING_MARKER, b"")
        for module in verify_native_wheel.NATIVE_MODULES:
            if module != omitted_module:
                archive.writestr(f"compas_libigl/{module}.abi3.so", b"")
            if module != omitted_stub:
                archive.writestr(f"compas_libigl/{module}.pyi", b"")
        if include_metadata:
            requires_dist = "".join(f"Requires-Dist: {dependency}\n" for dependency in dependencies)
            archive.writestr(
                "compas_libigl-0.7.6.dist-info/METADATA",
                f"Metadata-Version: 2.4\nName: compas_libigl\nVersion: 0.7.6\n{requires_dist}\n",
            )
        archive.writestr(
            "compas_libigl-0.7.6.dist-info/WHEEL",
            "Wheel-Version: 1.0\nRoot-Is-Purelib: false\n" + "".join(f"Tag: {internal_tag}\n" for internal_tag in internal_tags),
        )
    return wheel


def test_verify_wheel_accepts_complete_abi3_wheel(tmp_path: Path) -> None:
    verify_native_wheel.verify_wheel(make_wheel(tmp_path))


def test_verify_wheel_rejects_filename_internal_tag_mismatch(tmp_path: Path) -> None:
    wheel = make_wheel(tmp_path, internal_tags=("cp312-abi3-macosx_11_0_arm64",))
    with pytest.raises(SystemExit, match="do not match WHEEL tags"):
        verify_native_wheel.verify_wheel(wheel)


def test_verify_wheel_accepts_compressed_platform_tags(tmp_path: Path) -> None:
    wheel = make_wheel(
        tmp_path,
        filename_tag="cp312-abi3-manylinux_2_27_x86_64.manylinux_2_28_x86_64",
        internal_tags=(
            "cp312-abi3-manylinux_2_27_x86_64",
            "cp312-abi3-manylinux_2_28_x86_64",
        ),
    )
    verify_native_wheel.verify_wheel(wheel)


def test_verify_wheel_rejects_incomplete_compressed_platform_tags(tmp_path: Path) -> None:
    wheel = make_wheel(
        tmp_path,
        filename_tag="cp312-abi3-manylinux_2_27_x86_64.manylinux_2_28_x86_64",
        internal_tags=("cp312-abi3-manylinux_2_28_x86_64",),
    )
    with pytest.raises(SystemExit, match="do not match WHEEL tags"):
        verify_native_wheel.verify_wheel(wheel)


def test_verify_wheel_rejects_missing_native_module(tmp_path: Path) -> None:
    wheel = make_wheel(tmp_path, omitted_module="_mapping")
    with pytest.raises(SystemExit, match="_mapping"):
        verify_native_wheel.verify_wheel(wheel)


def test_verify_wheel_rejects_missing_native_stub(tmp_path: Path) -> None:
    wheel = make_wheel(tmp_path, omitted_stub="_mapping")
    with pytest.raises(SystemExit, match="_mapping.pyi"):
        verify_native_wheel.verify_wheel(wheel)


def test_verify_wheel_rejects_missing_typing_marker(tmp_path: Path) -> None:
    wheel = make_wheel(tmp_path, include_typing_marker=False)
    with pytest.raises(SystemExit, match="PEP 561 marker"):
        verify_native_wheel.verify_wheel(wheel)


def test_verify_wheel_rejects_missing_metadata(tmp_path: Path) -> None:
    wheel = make_wheel(tmp_path, include_metadata=False)
    with pytest.raises(SystemExit, match="0 METADATA files"):
        verify_native_wheel.verify_wheel(wheel)


def test_verify_wheel_rejects_missing_dependency(tmp_path: Path) -> None:
    wheel = make_wheel(tmp_path, dependencies=("compas<4,>=3.0", "numpy>=1.24"))
    with pytest.raises(SystemExit, match="tessagon"):
        verify_native_wheel.verify_wheel(wheel)
