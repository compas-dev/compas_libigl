********************************************************************************
Overview
********************************************************************************

`libigl <https://github.com/libigl/libigl>`_ integration uses `nanobind <https://github.com/wjakob/nanobind>`_ for Python bindings for COMPAS. The contribution guide is found in the "Contribute" section, which explains how to create a pull-request and implement new methods in both C++ and Python. Additional sections explain technical aspects of the repository that are useful during the binding process.

File and Folder Structure
-------------------------

The compas_libigl package contains numerous files and folders. For a simpler reference, check out the minimal `nanobind binding example <https://github.com/wjakob/nanobind_example>`_. Comparing it with compas_libigl helps understand the additional features provided by the COMPAS framework. For basic libigl bindings, you'll mainly work with the ``src`` folder, ``tests``, and ``examples``. The ``CMakeLists.txt`` is pre-configured to automatically include any new C++ source files, so you typically won't need to modify it.

Source Code
^^^^^^^^^^^
* ``src/`` - C++ backend code
* ``src/compas_libigl/`` - Python frontend code

Build & Dependencies
^^^^^^^^^^^^^^^^^^^^
* ``build/`` - Distributables e.g. for PyPi package
* ``external/`` - External C++ dependencies, downloaded via CMake ExternalProject module
* ``CMakeLists.txt`` - C++ project configuration
* ``pyproject.toml`` - Python project configuration (pip install -e .)
* ``requirements.txt`` - Runtime requirements (pip install -r requirements.txt)
* ``requirements-dev.txt`` - Development requirement (pip install -r requirements-dev.txt)
* ``tasks.py`` - Development tasks (invoke test, invoke docs, invoke format, invoke lint)

Tests & Examples
^^^^^^^^^^^^^^^^
* ``examples/`` - Example files
* ``tests/`` - Test files

Documentation
^^^^^^^^^^^^^
* ``docs/`` - Source code documentation
* ``dist/`` - Documentation build output

Data & Temporary Files
^^^^^^^^^^^^^^^^^^^^^^
* ``data/`` - Data sets (.obj, .off, .ply, .stl)
* ``temp/`` - Temporary files

Project Info
^^^^^^^^^^^^
* ``README.md`` - Project overview
* ``CHANGELOG.md`` - Feature changelog
* ``LICENSE`` - License information
