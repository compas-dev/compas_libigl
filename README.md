# compas_libigl

Opinionated COMPAS-compatible bindings for top-level algorithms of libigl.

## Installation

`compas_libigl` can be installed from source with pip in a conda environment with `Boost` and `Eigen3`.

```bash
conda create -n igl python=3.7 boost eigen COMPAS --yes
conda activate igl
pip install path/to/compas_libigl
```

## Libigl functions

Currently the following functionalities of Libigl are included in the wrapper

* Boolean operations (CGAL)
* Geodesic distance calculation
* Scalarfield isolines
* Quad mesh planarization
* 2D Triangulations (Triangle)

> The boolean operations are currently not available on Windows.

## Contribute

If you want to contribute, developer guidelines are available here [Developer Guide](DEVGUIDE.md).

## License

Libigl is licensed under MPL-2.
Free use of CGAL is licensed under LGPL and GPL-3.
Free use of Triangle is limited to personal and academic use and governed by a specific license agreement.

All licenses are included.
