.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/dateexpressions.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/dateexpressions
    .. image:: https://readthedocs.org/projects/dateexpressions/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://dateexpressions.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/dateexpressions/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/dateexpressions
    .. image:: https://img.shields.io/pypi/v/dateexpressions.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/dateexpressions/
    .. image:: https://img.shields.io/conda/vn/conda-forge/dateexpressions.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/dateexpressions
    .. image:: https://pepy.tech/badge/dateexpressions/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/dateexpressions
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/dateexpressions


.. image:: https://github.com/iilei/dateexpressions/actions/workflows/python-package.yml/badge.svg
    :alt: Python package
    :target: https://github.com/iilei/dateexpressions/actions/workflows/python-package.yml
    :align: right

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/
    :align: right



===============
dateexpressions
===============


    Parses relative date expressions so that you can say things like: `now/d` for the beginning of the day.


Inspired by Grafana Date Picker.

Allows for expressing relative date-times in a human friendly way.

.. code-block:: python

   from dateexpressions import parse

   # give me the last saturday of last month --
   # returning predictable results regardless of
   # when it get executed
   parse("""
            now /M :sat -1w
            /*
                ^ last saturday of last month
            */
    """)


CLI Usage
============

The above via cli: `date-expression isoformat 'now /M :sat -1w'`

The Optional `preflight` module can be installed on-demand, like `pip install dateexpressions[preflight]`.

This allows to verify a date-expression: ``date-expression preflight --cron '0 3 1,2,17,30,31 1-12 *' 'now-78h/h'``

Check out the `Specs </tests>`_ for more usage scenarios.

Local Development
----------------------

Run all Tests, all Python Versions:

.. code-block:: sh

   tox
