"""Release contracts checked offline; Docker execution recorded separately."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
BASE = "python:3.12.15-slim-bookworm@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258"


def test_closed_runtime_context_and_pinned_install():
    docker = (ROOT / "Dockerfile").read_text()
    assert docker.splitlines()[0] == "FROM " + BASE
    assert "--require-hashes" in docker and "https://pypi.org/simple" in docker
    copies = [line for line in docker.splitlines() if line.startswith("COPY ")]
    assert copies == ["COPY requirements.lock ./", "COPY coworking_nearby/*.py ./coworking_nearby/", "COPY data/coworkings.json ./data/coworkings.json"]
    assert "USER 10001:10001" in docker
    assert 'CMD ["python", "-m", "coworking_nearby"]' in docker
    assert "EXPOSE" not in docker and "apt" not in docker
    assert "requirements-dev" not in docker and "BOT_TOKEN" not in docker
    manifest = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert manifest["project"]["requires-python"] == ">=3.12,<3.13"
    lock = (ROOT / "requirements.lock").read_text()
    for pin in manifest["project"]["dependencies"]:
        assert pin in lock
    assert "pytest==" not in lock and "--hash=sha256:" in lock


def test_compose_image_only_readonly_directory_and_single_poller():
    # JSON is a YAML subset; parse without adding a release dependency.
    compose = json.loads((ROOT / "compose.yaml").read_text())
    assert set(compose) == {"services", "volumes"}
    assert compose["volumes"] == {"community_state": {}}
    assert len(compose["services"]) == 1
    service = next(iter(compose["services"].values()))
    assert service["image"] == "coworking-nearby:local"
    assert "build" not in service and "ports" not in service
    assert service["env_file"] == [".env"]
    assert service["stop_grace_period"] == "20s"
    assert service["volumes"] == [{"type": "bind", "source": "./data", "target": "/app/data", "read_only": True},
                                  {"type": "volume", "source": "community_state", "target": "/app/state"}]


def test_real_empty_synthetic_separate_blank_template():
    assert json.loads((ROOT / "data/coworkings.json").read_text()) == []
    synthetic = json.loads((ROOT / "examples/coworkings.synthetic.json").read_text())
    assert synthetic and all("synthetic" in row["id"].lower() for row in synthetic)
    assert (ROOT / ".env.example").read_text().splitlines()[0] == "BOT_TOKEN="


def test_inert_import_and_standalone_cli_without_sdk_or_network():
    code = r"""
import importlib.abc, runpy, socket, sys
class Deny(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, *args):
        if fullname.split('.')[0] in {'aiogram', 'aiohttp'}:
            raise AssertionError('SDK imported')
sys.meta_path.insert(0, Deny())
def denied(*args, **kwargs):
    raise AssertionError('network attempted')
socket.getaddrinfo = denied
socket.socket.connect = denied
import coworking_nearby
assert 'coworking_nearby.config' not in sys.modules
sys.argv = ['catalog', 'data/coworkings.json']
runpy.run_module('coworking_nearby.catalog', run_name='__main__')
"""
    result = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
        env={"PATH": os.environ.get("PATH", ""), "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr


def test_blank_token_executable_safe_failure_before_network():
    code = r"""
import socket
from coworking_nearby.__main__ import main
def denied(*args, **kwargs):
    raise AssertionError('NETWORK_SENTINEL')
socket.getaddrinfo = denied
socket.socket.connect = denied
raise SystemExit(main())
"""
    result = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
        env={"PATH": os.environ.get("PATH", ""), "BOT_TOKEN": "", "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True, text=True, timeout=15)
    assert result.returncode == 1 and result.stdout == ""
    records = [json.loads(line) for line in result.stderr.splitlines()]
    assert len(records) == 1
    assert records[0]["event"] == "fail" and records[0]["stage"] == "startup"
    assert "NETWORK_SENTINEL" not in result.stderr
