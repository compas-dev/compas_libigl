# Installation

COMPAS libigl requires Python 3.12 or newer.

## Stable release

Install a published wheel with pip:

```bash
python -m pip install compas_libigl
```

Install `compas-viewer` separately if you want to run the visual examples:

```bash
python -m pip install compas-viewer
```

## Source installation

Building from source requires a C++20 compiler and platform SDK. CMake downloads the pinned libigl, Eigen, and Clipper2 sources during configuration. See the [development environment](devguide/environment.md) and [compiler requirements](devguide/compiler.md) for details.
