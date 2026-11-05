"""Verify the ABI and contents of a COMPAS libigl wheel."""

from __future__ import annotations

import argparse
from email.parser import BytesParser
from pathlib import Path
from zipfile import ZipFile

NATIVE_MODULES = (
    "_boundaries",
    "_cotmatrix",
    "_curvature",
    "_geodistance",
    "_grad",
    "_intersections",
    "_isolines",
    "_mapping",
    "_massmatrix",
    "_meshing",
    "_parametrisation",
    "_planarize",
    "_simplify",
)

REQUIRED_DEPENDENCIES = {
    "compas<4,>=3.0",
    "numpy>=1.24",
    "tessagon",
}

TYPING_MARKER = "compas_libigl/py.typed"


def verify_wheel(wheel: Path) -> None:
    """Verify the stable-ABI tag, native modules, and runtime metadata."""
    if wheel.suffix != ".whl":
        raise SystemExit(f"{wheel} does not have a valid wheel filename")
    try:
        _, python_tags, abi_tags, platform_tags = wheel.name.removesuffix(".whl").rsplit("-", 3)
    except ValueError as error:
        raise SystemExit(f"{wheel} does not have a valid wheel filename") from error
    filename_tags = {
        f"{python_tag}-{abi_tag}-{platform_tag}" for python_tag in python_tags.split(".") for abi_tag in abi_tags.split(".") for platform_tag in platform_tags.split(".")
    }
    if not filename_tags or any(not tag.startswith("cp312-abi3-") for tag in filename_tags):
        raise SystemExit(f"{wheel} is not tagged cp312-abi3")

    with ZipFile(wheel) as archive:
        names = set(archive.namelist())
        if TYPING_MARKER not in names:
            raise SystemExit(f"{wheel} is missing the PEP 561 marker: {TYPING_MARKER}")
        metadata_paths = [name for name in names if name.endswith(".dist-info/METADATA")]
        if len(metadata_paths) != 1:
            raise SystemExit(f"{wheel} has {len(metadata_paths)} METADATA files")
        metadata = BytesParser().parsebytes(archive.read(metadata_paths[0]))
        wheel_paths = [name for name in names if name.endswith(".dist-info/WHEEL")]
        if len(wheel_paths) != 1:
            raise SystemExit(f"{wheel} has {len(wheel_paths)} WHEEL files")
        wheel_metadata = BytesParser().parsebytes(archive.read(wheel_paths[0]))

    internal_tags = set()
    for value in wheel_metadata.get_all("Tag", []):
        if len(value.split("-", 2)) != 3:
            raise SystemExit(f"{wheel} has an invalid internal wheel tag: {value!r}")
        internal_tags.add(value)
    if filename_tags != internal_tags:
        raise SystemExit(f"{wheel} filename tags {sorted(filename_tags)} do not match WHEEL tags {sorted(internal_tags)}")

    missing_extensions = []
    for module in NATIVE_MODULES:
        prefix = f"compas_libigl/{module}."
        if not any(name.startswith(prefix) and name.endswith((".so", ".pyd")) for name in names):
            missing_extensions.append(module)
    if missing_extensions:
        raise SystemExit(f"{wheel} is missing native extensions: {missing_extensions}")

    dependencies = set(metadata.get_all("Requires-Dist", []))
    missing_dependencies = sorted(REQUIRED_DEPENDENCIES.difference(dependencies))
    if missing_dependencies:
        raise SystemExit(f"{wheel} is missing runtime dependencies: {missing_dependencies}")


def main() -> None:
    """Verify every wheel passed on the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("wheels", nargs="+", type=Path)
    args = parser.parse_args()
    for wheel in args.wheels:
        verify_wheel(wheel)


if __name__ == "__main__":
    main()
