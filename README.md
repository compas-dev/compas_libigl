# compas_libigl

Opinionated COMPAS compatible bindings for top-level algorithms of libigl.

## Requirements

* Anaconda(3)
* COMPAS

Anaconda 3 can be obtained from the official website. With `conda` installing COMPAS is as simple as `$ conda install COMPAS`. Make sure you have the latest version of COMPAS. You can check the version by typing `python -c “import compas; print(compas.__version__)` in terminal.

## Git Submodules

* libigl
* PyBind11

## Compile

Before using cmake to compile the file, make sure followings are correct

* cmake version >= 3.12
* confirm your anaconda python location by typing `which python` in terminal
* change the `PYTHON_EXECUTABLE` as well as `PYBIND11_PYTHON_VERSION` in `compas_libigl/CMakeLists.txt` if it does not match your system settings.

In terminal

* `mkdir build`
* `cd build`
* `cmake -DCMAKE_BUILD_TYPE=Release ..`
* `make -j 4`

## Usage

To find the compiled library, please go to `compas_libigl/lib`. Taking `igl::triangulation` as an example, to run it just type `python lib/triangualtion/triangulation.py` in terminal. The program should run correctly without throwing error.

## Notes

### Goals

* Create bindings that can be used in Blender (CPython) and in Rhino (IronPython).
* Provide solutions based on cmake, pybind, Rhino SDK.

### Challenges

* Callbacks
* Live updating
* Dynamic visualisation

**Blender**

Bindings have to be generated for specific versions of Python, corresponding to
the embedded Python of different Blender releases. For example, Blender 2.78 expects
Python version 3.5.2.

**Rhino**

Bindings have to be generated using the Rhino SDK such that .NET compatible code
can be exposed through RhinoCommon.

### Related projects

* [PyMesh](https://github.com/PyMesh/PyMesh)
* [rhino3dm.py](https://github.com/mcneel/rhino3dm/blob/master/RHINO3DM.PY.md)
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
