from __future__ import annotations

from contextlib import nullcontext
import importlib.util
import json
from pathlib import Path
import subprocess

import pytest


SCRIPT = Path(__file__).parents[1] / ".github" / "scripts" / "smoke_test_wheel.py"
SPEC = importlib.util.spec_from_file_location("smoke_test_wheel", SCRIPT)
assert SPEC
assert SPEC.loader
smoke_test_wheel = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(smoke_test_wheel)


def prepare_environment(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        smoke_test_wheel.tempfile,
        "TemporaryDirectory",
        lambda **kwargs: nullcontext(str(tmp_path)),
    )

    def create(environment: Path) -> None:
        smoke_test_wheel.environment_python(environment).parent.mkdir(parents=True)

    monkeypatch.setattr(smoke_test_wheel.venv.EnvBuilder, "create", lambda self, environment: create(environment))


def test_consumer_branch_builds_strict_pyright_command(monkeypatch, tmp_path: Path) -> None:
    prepare_environment(monkeypatch, tmp_path)
    calls = []
    monkeypatch.setattr(smoke_test_wheel.subprocess, "run", lambda command, **kwargs: calls.append((command, kwargs)))

    wheel = tmp_path / "package.whl"
    constraint = tmp_path / "constraint.txt"
    consumer = tmp_path / "consumer.py"
    smoke_test_wheel.smoke_test(wheel, constraint, consumer)

    environment = tmp_path / "environment"
    python = smoke_test_wheel.environment_python(environment)
    assert calls[0][0][-3:] == [str(wheel), "pyright==1.1.414", "scipy-stubs==1.18.1.1"]
    assert calls[2] == (
        [
            str(python),
            "-m",
            "pyright",
            "--pythonpath",
            str(python),
            "--project",
            str(environment / "pyrightconfig.json"),
            str(consumer),
        ],
        {"check": True, "cwd": environment},
    )
    verify_command, verify_kwargs = calls[3]
    assert verify_command == [
        str(python),
        "-m",
        "pyright",
        "--pythonpath",
        str(python),
        "--project",
        str(environment / "pyrightconfig.json"),
        "--verifytypes",
        "compas_libigl",
        "--ignoreexternal",
    ]
    assert verify_kwargs["check"] is True
    assert verify_kwargs["cwd"] == environment
    assert verify_kwargs["env"]["PYTHONPATH"] == str(smoke_test_wheel.environment_site_packages(environment))
    assert json.loads((environment / "pyrightconfig.json").read_text(encoding="utf-8")) == {
        "typeCheckingMode": "strict",
        "pythonVersion": "3.12",
        "venvPath": str(tmp_path),
        "venv": "environment",
    }


def test_consumer_branch_propagates_pyright_failure(monkeypatch, tmp_path: Path) -> None:
    prepare_environment(monkeypatch, tmp_path)

    def run(command, **kwargs):
        if "pyright" in command:
            raise subprocess.CalledProcessError(1, command)

    monkeypatch.setattr(smoke_test_wheel.subprocess, "run", run)

    with pytest.raises(subprocess.CalledProcessError):
        smoke_test_wheel.smoke_test(tmp_path / "package.whl", tmp_path / "constraint.txt", tmp_path / "consumer.py")
