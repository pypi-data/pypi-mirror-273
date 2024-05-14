========
Overview
========

Toolbox for the inverse problem solution to identify sources of pheromone emission.

* Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

Installation
============

You can install the given sources with::

    pip install .

Alternatively, you can install the in-development version with::

    pip install git+ssh://git@forgemia.inra.fr/pherosensor/pherosensor-toolbox.git@main

Development
===========

To run all the tests run::

    tox


Documentation
=============

Documentations are available at ReadTheDocs <https://pherosensor-toolbox.readthedocs.io/en/latest/> _

Building the docs
-----------------

Alternatively, you can compile the documentation of the current code version.

Install sphinx and sphinx-rtd-theme with::

    pip install sphinx sphinx-rtd-theme
    
Then, you can do::

    cd docs

and::

    make html
    
The documentations (in html) are then stored in the folder 'build/html'
