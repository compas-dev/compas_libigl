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
    pip install -e .

.. note::

    On Mac, don't forget to install ``python.app`` as well!
