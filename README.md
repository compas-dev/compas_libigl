# compas_libigl

COMPAS-compatible Python bindings for selected [libigl](https://libigl.github.io/) algorithms, generated with [nanobind](https://nanobind.readthedocs.io/).

## Installation

Install a published wheel with pip:

```bash
python -m pip install compas_libigl
```

## Development

Python 3.12 or newer and a platform C++ toolchain are required. Create the locked development environment with [uv](https://docs.astral.sh/uv/):

```bash
uv sync --frozen --all-groups
```

The authoritative local checks are:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
uv run mkdocs build --strict
uv build
```

Thin Invoke conveniences are also available, for example `uv run invoke test` and `uv run invoke docs`.

## Functionality

The bindings include:

- geodesic distance;
- scalar-field isolines;
- quad-mesh planarisation;
- triangle-mesh mass matrices and curvature;
- ray-mesh intersections and boundary loops;
- harmonic and least-squares conformal parametrisation;
- mapping, remeshing, gradients, and simplification utilities.

See the [documentation](https://compas.dev/compas_libigl/) and the scripts in [`docs/examples`](docs/examples). Visual examples additionally require `compas-viewer`.

## License

`compas_libigl` is distributed under the MIT License. libigl itself is distributed under the Mozilla Public License 2.0; see [`LICENSE.igl`](LICENSE.igl).
