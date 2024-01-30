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

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

===============
dateexpressions
===============


    Parses relative date expressions so that you can say things like: `now/d` for the beginning of the day.


Inspired by Grafana Date Picker.

Allows for expressing relative date-times in a human friendly way.

.. role:: python(code)
   :language: python

   from dateexpressions import parse

   parse("now")
   parse("now/d")
   parse("now/d+12h")

   # Month simply added like `+6M` ~> Exception
   # -- as a guard against ambigous expressions
   # Solvable by doing `/M` so to get deterministic results
   parse("now/M")
   parse("now/M+6M")


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
