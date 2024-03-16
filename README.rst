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


.. CAUTION::

   Regardless of what is stated in the text below, at the moment this Package has not yet been released on pypi.org.

************************************

*Why?*

Dealing with recurring tasks, be it on a regular schedule or upon irregular events
can be a source for confusion, especially when the 'regualar' and 'irregular' triggers
happen to both initiate the same task.

The user friendly and simple kind of *date expressions* at the `Grafana <https://grafana.com/grafana/>`_ Web Frontend with its date
picker component gave the inspiration for this python package.

With dateexpressions the same ease-of-use is at hand to be put to use by the simplicity
of text-based configuration files interpreted by any kind of server side software.



************************************

parse
====================================

Interprets a date expression and returns a timezone-aware datetime object.

.. code:: python

   from dateexpressions import parse

   # Last saturday of last month
   parse("""
            now /M :sat -1w
            /*
                ^ last saturday of previous month
            */
    """)


************************************

Parser details
====================================

.. image:: src/dateexpressions/svg/to_relative_date.svg
    :alt: How the syntax is interpreted - Diagram
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
   * - ``/M``
     - Beginning of the month.
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
   * -
     - **Note:** Except from the ability to clamp to weekdays, the syntax
       for year- and month-deltas is interchangable.

The requirement to *floor* to the beginning of Year or Month before adding a delta is to rule
out any potential for confusion.

************************************

CLI Usage: isoformat
#########################

Parses a given expression and returns the result ain ISO format.

Example:

.. code:: shell

   date-expression isoformat 'now /M :sat -1w'

CLI Usage: preflight
#########################

The Optional ``preflight`` module is to be requested explicitly if desired: ``pip install dateexpressions[preflight]``.

To verify a date expression invoke the ``preflight`` job with a ``cron`` expression, optional ``max-results``
and the date expression you wish to see in action:

.. code:: shell

   date-expression preflight \
      --cron '13 3 28-31 * *' \
      --max-results 9 \
      'now/M+1M:sat-1w'


Example Result, prettified (by piping it to ``jq '.'``):

.. code:: json

   {
     "expression": "now/M+1M:sat-1w",
     "cron": "13 3 28-31 * *",
     "yields": [
       "2024-02-24T00:00:00+00:00",
       "2024-02-24T00:00:00+00:00",
       "2024-03-30T00:00:00+00:00",
       "2024-03-30T00:00:00+00:00",
       "2024-03-30T00:00:00+00:00",
       "2024-03-30T00:00:00+00:00",
       "2024-04-27T00:00:00+00:00",
       "2024-04-27T00:00:00+00:00",
       "2024-04-27T00:00:00+00:00"
     ]
   }


Scenarios covered
----------------------

Check out the `Specs </tests>`_ for a variety of usage scenarios.

***************************
Local development and testing
---------------------------

Install all Dependencies


```shell
python -m pip install tox
python -m pip install -e '.[testing]'
```

Run all Tests, all Python Versions:

.. code-block:: sh

   tox

***************************

Acknowledgments
---------------------------

*core parser*

* `textX <https://github.com/textX/textX>`_, which is used for building the Domain-Specific Language Interpreter

*'preflight' functionality*

* `croniter <https://pypi.org/project/croniter/>`_ crontab parser
* `time-machine <https://pypi.org/project/time-machine/>`_ for simulating different points in time for execution
