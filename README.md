# compas_libigl

Opinionated COMPAS-compatible bindings for top-level algorithms of libigl.

## Requirements

* Anaconda(3)
* COMPAS
* CMake
* Boost

Anaconda 3 can be obtained from the official website. With `conda` installing COMPAS is as simple as `$ conda install COMPAS`. Make sure you have the latest version of COMPAS. You can check the version by typing `python -c “import compas; print(compas.__version__)` in terminal.

## Git Submodules

* libigl
* PyBind11
* Eigen

These are configured in the `.gitmodules` file and will be cloned into the `ext` folder.

<https://git-scm.com/book/en/v2/Git-Tools-Submodules>
<https://git-scm.com/docs/git-submodule>
<https://git-scm.com/docs/gitmodules>

**Make sure to clone the submodules together with the main repo.**

```bash
git clone --recursive https://github.com/BlockResearchGroup/compas_libigl.git
```

## Modules

The folder `modules` contains the wrapper code per *module* that should be added to `compas_libigl`.
Each module is in a separate folder with its own `CMakeLists.txt` and a `.cpp` file with the wrapper code.

## Environment

As with all things COMPAS, it is recommended to make a separate environment for experimenting with this package.

```bash
conda create -n igl python=3.7 COMPAS --yes
conda activate igl
```

> On Mac, don't forget to add `python.app`

To make sure that you can build the modules that require `CGAL`, you should also install `Boost` into this environment.

```bash
conda install boost
```

> Note that a conda install of Boost into an environment with Python 3.x will install Boost 1.70 and this is only supported since CMake 3.14.

To use the viewers, install `compas_viewers` and its dependencies.

```bash
conda install PySide2 PyOpenGL
pip install git+https://github.com/compas-dev/compas_viewers.git#egg=compas_viewers
```

## Compile & Install

On Mac

* `rm -rf build`
* `pip install -e .`

On Windows

* `rmdir build /s`
* `pip install -e .`

## Check Installation

To verify, start an interactive python session and import the package. This should not throw any errors.

```python
>>> import compas
>>> import compas_libigl
```

## Usage

The compiled libraries are added directly into the `compas_libigl` package.
If you add a new wrapper, make sure to add a corresponding entry in the `__init__.py` file of the package.

Example scripts for simple use cases are located in the `scripts` folder.

**If you make changes to the C++ part of `compas_libigl` you have to rebuild the package before these changes have an effect.**

## Known Issues

Boolean operations and their CSGtree variations depend on CGAL.
On Windows, the installation of CGAL is problematic.
Therefore, support for blooean operations is not enabled by default.
To build `compas_libigl` with support for boolean operations, modify the following files:

* `modules/CMakeLists.txt`:

  * uncomment line 6 (`# add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/csgtree)`)
  * uncomment line 7 (`# add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/booleans)`)

* `src/compas_libigl/__init__.py`:

  * uncomment line 5 (`# from .booleans import *`)
  * uncomment line 6 (`# from .csgtree import *`)

## Cmake

The project has three levels of `CMakeLists.txt` files.

### /CMakeLists.txt

The top level file is located at the root of the project.

### /modules/CMakeLists.txt

The second level file is in the `modules` folder. If you add a new wrapper module, make sure to register it in this file as well.

```make
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/xxx)
```

### /modules/xxx/CMakeLists.txt

Finally there is a `CMakeLists` file per wrapper module. There the most relevant part is to link the correct libraries. For example, the module that wraps `libigl`'s boolean operations requires `CGAL` and this should thus be reflected in the file.

```make
target_link_libraries(booleans PRIVATE igl::cgal)
```

## Notes

### Related projects

* [PyMesh](https://github.com/PyMesh/PyMesh)
* [PyTriangle](https://github.com/pletzer/pytriangle)
* [Triangle](https://github.com/drufat/triangle)
* [CMake Triangle](https://github.com/wo80/Triangle)
* [Projects in C](https://userpages.umbc.edu/~rostamia/cbook/triangle.html)
* [cppimport](https://github.com/tbenthompson/cppimport)

### PyBind

* [PyBind: building with cmake](https://pybind11.readthedocs.io/en/stable/compiling.html#building-with-cmake)
* [PyBind: building manually](https://pybind11.readthedocs.io/en/stable/compiling.html#building-manually)
* <https://github.com/pybind/pybind11/issues/134>
* <https://github.com/pybind/pybind11/issues/1200>
* <https://pybind11.readthedocs.io/en/stable/advanced/cast/stl.html>

### SO

* <https://stackoverflow.com/questions/16439654/how-can-i-compile-triangle-using-makefiles-on-a-windows-machine>
* <https://stackoverflow.com/questions/1099981/why-cant-python-find-shared-objects-that-are-in-directories-in-sys-path>
