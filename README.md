# compas_libigl

COMPAS-compatible bindings for top-level algorithms of libigl generated with Pybind.
Many of the functions provided by `compas_libigl` are based on the examples in the libigl tutorial.

## Installation

`compas_libigl` can be installed using a combination of conda and pip.

```bash
conda create -n igl python=3.7 git cmake">=3.14" boost eigen=3.3 COMPAS compas_view2 --yes
conda activate igl
git clone --recursive https://github.com/BlockResearchGroup/compas_libigl.git
cd compas_libigl
rm -rf build
pip install -e .
```

> If you have git/cmake installed, this can be omitted from the environment installation.
> On Mac, don't forget to install `python.app`!

## Libigl functions

Currently the following functionalities of Libigl are included in the wrapper

* Geodesic distance calculation
* Scalarfield isolines
* Quad mesh planarization
* Mass matrix of triangle meshes
* Discrete gaussian curvature
* Ray/mesh intersection
* Boundary loops
* Harmonic parametrisation
* Least-squares conformal maps

## Examples

The use of the wrapped functions is illustrated with scripts in the `examples` folder.
Note that the functionality of the package is not directly available in Rhino, but can be used through `compas.rpc`.

## License

Libigl (and therefore also `compas_libigl`) is licensed under MPL-2.
