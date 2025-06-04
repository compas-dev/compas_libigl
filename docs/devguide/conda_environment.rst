********************************************************************************
Conda Environment
********************************************************************************

There are two ways to set up the development environment:

Using environment.yml (recommended)
-----------------------------------

.. code-block:: bash

    conda env create -f environment.yml
    conda activate compas_libigl

Manual setup
------------

.. code-block:: bash

    conda create -n compas_libigl python=3.9 compas -c conda-forge -y
    pip install -r requirements-dev.txt
    pip install --no-build-isolation -ve . -Ceditable.rebuild=true

Both methods will create and configure the same development environment.
