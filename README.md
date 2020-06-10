# compas_libigl

Opinionated COMPAS-compatible bindings for top-level algorithms of libigl.

## Installation

`compas_libigl` can be installed from source using pip.

1. Create an environment

   ```bash
   conda create -n igl python=3.7 git cmake">=3.14" boost eigen COMPAS">=0.16.1" --yes
   conda activate igl
   ```

   > On OSX, don't forget to also install python.app.

2. Clone the repo

   ```bash
   git clone --recursive https://github.com/BlockResearchGroup/compas_libigl.git
   cd compas_libigl
   ```

3. Install

   ```bash
   pip install -e .
   ```

4. Install the COMPAS viewer for visualisation.

   *On Mac.*

   ```bash
   conda install PySide2 PyOpenGL --yes
   pip install -e git+https://github.com/compas-dev/compas_viewers.git#egg=compas_viewers
   ```

   *On Windows.*

   ```bash
   conda install PySide2 --yes
   pip install wheels/PyOpenGL-3.1.5-cp37-cp37m-win_amd64.whl
   pip install git+https://github.com/compas-dev/compas_viewers.git#egg=compas_viewers
   ```

## Libigl functions

Currently the following functionalities of Libigl are included in the wrapper

* Geodesic distance calculation
* Scalarfield isolines
* Quad mesh planarization
* 2D Triangulations (Triangle)
* Mass matrix of triangle mesh

## Examples

The use of the wrapped functions is illustrated with scripts in the `examples` folder.
Note that the functionality of the package is not directly available in Rhino, but can be used through `compas.rpc`.

## License

Libigl is licensed under MPL-2.
Free use of CGAL is licensed under LGPL and GPL-3.
Free use of Triangle is limited to personal and academic use and governed by a specific license agreement.

All license notices are included.
