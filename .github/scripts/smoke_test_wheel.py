"""Install one wheel into a fresh environment and import every native module."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

IMPORT_MODULES = (
    "compas_libigl",
    "compas_libigl._boundaries",
    "compas_libigl._cotmatrix",
    "compas_libigl._curvature",
    "compas_libigl._geodistance",
    "compas_libigl._grad",
    "compas_libigl._intersections",
    "compas_libigl._isolines",
    "compas_libigl._mapping",
    "compas_libigl._massmatrix",
    "compas_libigl._meshing",
    "compas_libigl._parametrisation",
    "compas_libigl._planarize",
    "compas_libigl._simplify",
)


def environment_python(environment: Path) -> Path:
    """Return the Python executable inside a virtual environment."""
    if sys.platform == "win32":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def environment_site_packages(environment: Path) -> Path:
    """Return the site-packages directory inside a virtual environment."""
    if sys.platform == "win32":
        return environment / "Lib" / "site-packages"
    version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    return environment / "lib" / version / "site-packages"


def smoke_test(wheel: Path, constraint: Path, consumer: Path | None = None) -> None:
    """Install ``wheel`` with ``constraint`` and verify its public surface."""
    if consumer:
        consumer = consumer.resolve()
    with tempfile.TemporaryDirectory(prefix="compas-libigl-wheel-") as directory:
        environment = Path(directory) / "environment"
        venv.EnvBuilder(with_pip=True).create(environment)
        python = environment_python(environment)
        install = [
            str(python),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--constraint",
            str(constraint),
            str(wheel),
        ]
        if consumer:
            install.extend(("pyright==1.1.414", "scipy-stubs==1.18.1.1"))
        subprocess.run(install, check=True)
        imports = "; ".join(f"import {module}" for module in IMPORT_MODULES)
        subprocess.run([str(python), "-c", imports], check=True)
        if consumer:
            config = environment / "pyrightconfig.json"
            config.write_text(
                json.dumps(
                    {
                        "typeCheckingMode": "strict",
                        "pythonVersion": "3.12",
                        "venvPath": str(environment.parent),
                        "venv": environment.name,
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [str(python), "-m", "pyright", "--pythonpath", str(python), "--project", str(config), str(consumer)],
                check=True,
                cwd=environment,
            )
            verify_environment = os.environ.copy()
            verify_environment["PYTHONPATH"] = str(environment_site_packages(environment))
            subprocess.run(
                [
                    str(python),
                    "-m",
                    "pyright",
                    "--pythonpath",
                    str(python),
                    "--project",
                    str(config),
                    "--verifytypes",
                    "compas_libigl",
                    "--ignoreexternal",
                ],
                check=True,
                cwd=environment,
                env=verify_environment,
            )


def main() -> None:
    """Smoke-test the one wheel found in a wheelhouse."""
    parser = argparse.ArgumentParser()
    parser.add_argument("wheelhouse", type=Path)
    parser.add_argument("--constraint", required=True, type=Path)
    parser.add_argument("--consumer", type=Path)
    args = parser.parse_args()
    wheels = sorted(args.wheelhouse.glob("*.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"Expected exactly one wheel in {args.wheelhouse}, found {len(wheels)}")
    smoke_test(wheels[0], args.constraint, args.consumer)


if __name__ == "__main__":
    main()
