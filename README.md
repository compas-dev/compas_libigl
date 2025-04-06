# compas_libigl

COMPAS-compatible bindings for top-level algorithms of libigl generated with Pybind.
Many of the functions provided by `compas_libigl` are based on the examples in the libigl tutorial.

## Installation

### Stable

The stable version of `compas_libigl` can now be installed from conda-forge.

```bash
conda create -n igl compas_libigl
```

### Dev install

A dev version of `compas_libigl` can be installed using a combination of conda and pip.

```bash
conda create -n igl-dev python=3.9 --yes
conda activate igl
pip install --no-build-isolation -ve .
```

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
