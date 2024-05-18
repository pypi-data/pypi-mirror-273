Base library providing basic pathfinder REST api access utilities.

Documentation and examples available under the `docs` directory, 
can be built via sphinx for easy reading::

    cd docs
    pip install -U sphinx
    make html
    firefox _build/index.html

# Packaging

Creating a simple wheel file for a python2.7 environment.

> python setup.py bdist_wheel
> Archive the artifact under dist/*
