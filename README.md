# compas_libigl

Opinionated COMPAS-compatible bindings for top-level algorithms of libigl.

## Installation

`compas_libigl` can be installed from source with `conda-build` using the `conda` recipe in `/recipe`.

```bash
conda create -n igl python=3.7 cmake">=3.14" --yes
conda activate igl
conda build recipe
conda install compas_libigl --use-local
```

> Don't forget to also install python.app on OSX.

Additionally, install the COMPAS viewer for visualisation.

*On Mac.*

```bash
conda install PySide2 PyOpenGL --yes
pip install -e git+https://github.com/compas-dev/compas_viewers.git#egg=compas_viewers
```

*On Windows.*

```bash
conda install PySide2 --yes
pip install wheels/PyOpenGL‑3.1.5‑cp37‑cp37m‑win_amd64.whl
pip install git+https://github.com/compas-dev/compas_viewers.git#egg=compas_viewers
```

## Libigl functions

Currently the following functionalities of Libigl are included in the wrapper

* Boolean operations (CGAL)
* Geodesic distance calculation
* Scalarfield isolines
* Quad mesh planarization
* 2D Triangulations (Triangle)

> The boolean operations are currently not available on Windows.

## Examples

The use of the wrapped functions is illustrated with scripts in the `examples` folder.
Note that the functionality of the package is not directly available in Rhino, but can be used through `compas.rpc`.

## License

Libigl is licensed under MPL-2.
Free use of CGAL is licensed under LGPL and GPL-3.
Free use of Triangle is limited to personal and academic use and governed by a specific license agreement.

All license notices are included.
