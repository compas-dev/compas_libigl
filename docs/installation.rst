********************************************************************************
Installation
********************************************************************************

We are working on a ``conda-forge`` package for :mod:`compas_libigl`.
However, it is currently not available, yet.
In the meantime, :mod:`compas_libigl` can be installed "from source" using a combination of ``conda`` and ``pip``.

Create a ``conda`` environment with the required dependencies and activate it.
Note that you can choose a different name for the environment than ``igl``.

.. code-block:: bash

    conda create -n igl python=3.7 git cmake">=3.14" boost eigen=3.3 compas
    conda activate igl

Get a local copy of the source code of :mod:`compas_libigl` with all submodules.

.. code-block:: bash

    git clone --recursive https://github.com/compas-dev/compas_libigl.git

Install the package in "editable" mode using ``pip``.
Note that this will automatically build the C++ extension.

.. code-block:: bash

    cd compas_libigl
    pip install -e .
