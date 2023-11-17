********************************************************************************
Installation
********************************************************************************

We are working on a ``conda`` package for :mod:`compas_libigl`.
However, it is currently not available, yet.

In the meantime, :mod:`compas_libigl` can be installed using a combination of `conda` and `pip`.

.. code-block:: bash

    conda create -n igl python=3.7 git cmake">=3.14" boost eigen=3.3 compas"
    conda activate igl
    git clone --recursive https://github.com/compas-dev/compas_libigl.git
    cd compas_libigl
    pip install -e .
