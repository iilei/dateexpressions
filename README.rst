.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

.. image:: https://github.com/iilei/dateexpressions/actions/workflows/python-package.yml/badge.svg
    :alt: Python package
    :target: https://github.com/iilei/dateexpressions/actions/workflows/python-package.yml


.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit


===============
dateexpressions
===============


    Allows for expressing relative date-times in a human friendly way.


Inspired by Grafana Date Picker.

Parses relative date expressions so that you can say things like: ``now/d`` for the beginning of the day.


.. code-block:: python

   from dateexpressions import parse

   # give me the last saturday of last month --
   # returning predictable results regardless of
   # when it get executed
   parse("""
            now /M :sat -1w
            /*
                ^ last saturday of previous month
            */
    """)

------------------------------------

Parser Details
====================================

.. image:: src/dateexpressions/svg/to_relative_date.svg
    :alt: How the Syntax is interpreted - Diagram
    :target: src/dateexpressions/to_relative_date.puml

------------


.. list-table:: Basic Syntax
   :widths: 30 70
   :header-rows: 1

   * - Pattern
     - Description
   * - ``now``
     - UTC Timezone-Aware Reference point to start with
   * - ``now(Europe/Berlin)``
     - Timezone-Aware Reference point to start with, as per value given
   * - ``now(timezone=Europe/Amsterdam)``
     - Timezone-Aware Reference point to start with, as per value given
   * - ``/s``
     - Beginning of the second
   * - ``/m``
     - Beginning of the minute
   * - ``/h``
     - Beginning of the hour
   * - ``/d``
     - Beginning of the day
   * - ``/w``
     - Beginning of the week
   * - ``/M``
     - Beginning of the month
   * - ``/y``
     - Beginning of the year

.. list-table:: Time-Delta Syntax
   :widths: 30 70
   :header-rows: 1

   * - Pattern
     - Description
   * - ``<INT>[smhdw]``
     - Time Delta to apply. (second, minute, hour, day, week)
       <INT> ~> positive or negative number
   * - ``/M<INT>M``
     - Month Delta to apply, once the beginning of the respective month is determined.
       <INT> ~> positive or negative number
   * - ``/M:(mon|tue|wed|thu|fri|sat|sun)``
     - Beginning of the month, first respective day of the month.
   * - ``/M<INT>M:(mon|tue|wed|thu|fri|sat|sun)``
     - Beginning of the month, Delta applied, first respective day of the month.
   * - ``/y<INT>y``
     - Year Delta to apply, once the beginning of the respective year is determined.
       <INT> ~> positive or negative number



CLI Usage: isoformat
======================

The above via cli:

``date-expression isoformat 'now /M :sat -1w'``

CLI Usage: preflight
======================

The Optional ``preflight`` module can be installed on-demand, like ``pip install dateexpressions[preflight]``.

This allows to verify a date-expression:
``date-expression preflight --cron '0 3 1,2,17,30,31 1-12 *' 'now-78h/h'``

Scenarios covered
======================

Check out the `Specs </tests>`_ for a variety of usage scenarios.

Local Development
----------------------

Run all Tests, all Python Versions:

.. code-block:: sh

   tox


Credits
---------------------------
* `textX <https://github.com/textX/textX>`_ which is used for building the Domain-Specific Language Interpreter
* Date range Picker keywords as seen in `Grafana <https://grafana.com/grafana/>`_
