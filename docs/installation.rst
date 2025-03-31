********************************************************************************
Installation
********************************************************************************

Stable
======

On ``conda-forge``, ``compas_libigl`` is available for Python 3.8, 3.9, and 3.10 on Windows, macOS, and Linux.

.. code-block:: bash

    conda install -c conda-forge compas_libigl


Dev Install
===========

Adevelopment version of :mod:`compas_libigl` can be installed "from source" using a combination of ``conda`` and ``pip``.

Create a ``conda`` environment with the required dependencies and activate it.
Note that you can choose a different name for the environment than ``igl-dev``.

.. code-block:: bash

    conda create -n igl-dev python=3.9 git cmake">=3.14" boost eigen=3.3 pybind11
    conda activate igl

Get a local copy of the source code of :mod:`compas_libigl` with all submodules.

.. code-block:: bash

    git clone --recursive https://github.com/compas-dev/compas_libigl.git

Install the package in "editable" mode using ``pip``.
Note that this will automatically build the C++ extension.

.. code-block:: bash

    cd compas_libigl
    pip install -e .
