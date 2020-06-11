********************************************************************************
Getting Started
********************************************************************************

Installation
============

:mod:`compas_libigl` can be installed using a combination of `conda` and `pip`.

.. code-block:: bash

    conda create -n igl python=3.7 git cmake">=3.14" boost eigen COMPAS">=0.16.1" --yes
    conda activate igl
    git clone --recursive https://github.com/BlockResearchGroup/compas_libigl.git
    cd compas_libigl
    rm -rf build
    pip install -e .

.. note::

    If you have `git` or `cmake` installed, this can be omitted from the environment installation.
    On Mac, don't forget to install ``python.app`` as well!


Install COMPAS viewer (optional)
================================

On Mac
------

.. code-block:: bash

    conda install PySide2 PyOpenGL --yes
    pip install -e git+https://github.com/compas-dev/compas_viewers.git#egg=compas_viewers


On Windows
----------

.. code-block:: bash

    conda install PySide2 --yes
    pip install wheels/PyOpenGL-3.1.5-cp37-cp37m-win_amd64.whl
    pip install git+https://github.com/compas-dev/compas_viewers.git#egg=compas_viewers
