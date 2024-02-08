"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = dateexpressions.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import json
import logging
import sys
import textwrap
from datetime import datetime
from datetime import datetime as dt
from datetime import timedelta
from pathlib import Path
from typing import Union

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

try:
    from types import NoneType
except ImportError:
    NoneType = None.__class__

from croniter import croniter
from textx import metamodel_from_file

from dateexpressions import __version__
from dateexpressions.relative_date import RelativeDate

relative_date_meta_model = metamodel_from_file(
    Path.joinpath(Path(__file__).parent, "to_relative_date.tx"), use_regexp_group=True
)


__author__ = "iilei • jochen preusche"
__copyright__ = "iilei • jochen preusche"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from dateexpressions.parse import parse`,
# when using this Python module as a library.


def parse(expression: str, now: Union[datetime, NoneType] = None):
    relative_date_model = relative_date_meta_model.model_from_str(expression or "now")

    relative_date = RelativeDate(now)
    _logger.debug(f"{expression=}")
    return relative_date.interpret(relative_date_model)


assert parse("", dt(1984, 1, 1))


def preflight(cron: str, expression: str, max_results: int):
    base = datetime.now(ZoneInfo("UTC"))
    itr = croniter(cron, base, max_years_between_matches=3)

    return [
        parse(expression=expression, now=itr.get_next(datetime))
        for _ in range(0, max_results)
    ]


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Parse Relative Date Expressions")

    subparsers = parser.add_subparsers(help="preflight or isoformat")

    parser_preflight = subparsers.add_parser(
        "preflight",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help=textwrap.dedent(
            """\
            Allows for preflight runs to validate a given date-expression.

                Requires installation with sub-command dependencies:
                pip install 'dateexpressions[preflight]'

        """
        ),
    )

    parser_preflight.add_argument(
        "--cron",
        default="0 3 1,2,17,30,31 1-12 *",
        type=str,
        help=textwrap.dedent(
            """\
            crontab to evaluate the datexpression with

            To answer the question:

                Given the corresponding date-expression is parsed at
                that times yielded by this cron tab -- what will be
                returned?

            The default choice is designed so that it covers a good
            range of datetimes which help to verify the intent of a
            date-expression.

            It translates to:

                * At 03:00
                * day-of-month 1, 2, 17, 30, and 31
                * in every month from January through December

        """
        ),
    )
    parser_preflight.add_argument(
        "--max-results", default=3, type=int, help="how many checks to run"
    )
    subparsers.add_parser(
        "isoformat", help="yields the result of a given date expression in isoformat."
    )
    parser.add_argument(
        "expression", help="relative date expression", type=str, metavar="String"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"dateexpressions {__version__}",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`parse` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`parse`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "now/d"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    if hasattr(args, "cron"):
        print(
            json.dumps(
                {
                    "expression": args.expression,
                    "cron": args.cron,
                    "yields": [
                        x.isoformat()
                        for x in preflight(
                            cron=args.cron,
                            expression=args.expression,
                            max_results=args.max_results,
                        )
                    ],
                }
            )
        )
    else:
        print(parse(args.expression).isoformat())


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::

    #     python -m dateexpressions.parse "now/M+2M:sat-1w /* last saturday next month */"

    run()
