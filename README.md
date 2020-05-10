# compas_libigl

Opinionated COMPAS-compatible bindings for top-level algorithms of libigl.

## Installation

`compas_libigl` can be installed from source with pip in a conda environment with `CMake`, `Boost` and `Eigen3`.

```bash
conda create -n igl python=3.7 cmake">=3.14" boost eigen COMPAS --yes
conda activate igl
pip install path/to/compas_libigl
```

> Don't forget to also install python.app on OSX.

Optionally, install the COMPAS viewer for visualisation.

```bash
conda install PySide2 PyOpenGL --yes
pip install git+https://github.com/compas-dev/compas_viewers.git#egg=compas_viewers
```

Detailed installation instructions are available through the viewer repo:
<https://github.com/compas-dev/compas_viewers>

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
