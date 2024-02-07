import datetime as dt
import json
from unittest.mock import patch
from zoneinfo import ZoneInfo

import pytest
import time_machine

from dateexpressions.parse import main, parse, run

UTC_ZONEINFO = ZoneInfo(key="UTC")
SOME_DAY = dt.datetime(2024, 1, 24, 14, 15, 16, tzinfo=UTC_ZONEINFO)


@time_machine.travel(SOME_DAY, tick=False)
def test_parse():
    """API Tests"""
    assert (
        parse("", dt.datetime(1984, 1, 1, tzinfo=UTC_ZONEINFO)).isoformat()
        == "1984-01-01T00:00:00+00:00"
    )
    assert parse("now") == SOME_DAY
    assert (
        parse(
            "now/s", SOME_DAY + dt.timedelta(microseconds=234, milliseconds=23)
        ).isoformat()
        == "2024-01-24T14:15:16+00:00"
    )
    assert parse("now/m").isoformat() == "2024-01-24T14:15:00+00:00"
    assert parse("now/h").isoformat() == "2024-01-24T14:00:00+00:00"
    assert parse("now/d").isoformat() == "2024-01-24T00:00:00+00:00"
    assert parse("now/w").isoformat() == "2024-01-22T00:00:00+00:00"
    assert parse("now/M").isoformat() == "2024-01-01T00:00:00+00:00"
    assert parse("now/y").isoformat() == "2024-01-01T00:00:00+00:00"

    assert parse("now/m+1m").isoformat() == "2024-01-24T14:16:00+00:00"
    assert parse("now/h+1h").isoformat() == "2024-01-24T15:00:00+00:00"
    assert parse("now/d+1d").isoformat() == "2024-01-25T00:00:00+00:00"
    assert parse("now/w+1w").isoformat() == "2024-01-29T00:00:00+00:00"
    assert parse("now/M+1M").isoformat() == "2024-02-01T00:00:00+00:00"
    assert parse("now/y+1y").isoformat() == "2025-01-01T00:00:00+00:00"

    # use case as described at the docs:
    assert (
        parse(
            """
    now /M :sat -1w
    /*
      last saturday of last month
    */
    """
        ).isoformat()
        == "2023-12-30T00:00:00+00:00"
    )
    assert (
        parse(
            """
    now /M+1M :sat -1w +1d
    /*
      last saturday of the current month,
      full day (by adding one day)
    */
    """
        ).isoformat()
        == "2024-01-28T00:00:00+00:00"
    )
    # ****************

    assert (
        parse("now/M+1M:sat-1w /** last saturday of the month **/").isoformat()
        == "2024-01-27T00:00:00+00:00"
    )

    assert parse("now(Europe/Berlin)") == dt.datetime.now(ZoneInfo(key="Europe/Berlin"))
    assert parse("now(timezone=Europe/Amsterdam)") == dt.datetime.now(
        ZoneInfo(key="Europe/Amsterdam")
    )

    assert parse("now/M+1M:tue") == dt.datetime(2024, 2, 6, tzinfo=UTC_ZONEINFO)
    assert parse("now+20d/M:sat") == dt.datetime(2024, 2, 3, tzinfo=UTC_ZONEINFO)
    assert parse(
        "now/h+30m+15s /* beginning of the current hour, added 30m and 15s */"
    ) == dt.datetime(2024, 1, 24, 14, 30, 15, tzinfo=UTC_ZONEINFO)

    assert (
        parse(
            """
        /h
        /*
           beginning of the current hour
           -- 'now' and UTC both are implicit,
           no need to state it
        */
        +2m
        """
        )
        == dt.datetime(2024, 1, 24, 14, 2, tzinfo=UTC_ZONEINFO)
    )

    with pytest.raises(Exception):
        # Because a month is not a fixed duration, Deltas with unit=Month are only
        # applicable directly after a `Floor to Month` Operation
        parse("now-1M")

    with pytest.raises(Exception):
        # Because a month is not a fixed duration, Deltas with unit=Month are only
        # applicable directly after a `Floor to Month` Operation
        parse("now-1y")


@time_machine.travel(dt.datetime(2024, 1, 2, 14, 15, 16, tzinfo=UTC_ZONEINFO), tick=False)
def test_main_a(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["isoformat", "now-78h/h"])
    captured = capsys.readouterr()
    assert "2023-12-30T08:00:00+00:00" in captured.out


@time_machine.travel(dt.datetime(2024, 1, 2, 14, 15, 16, tzinfo=UTC_ZONEINFO))
def test_main_b(capsys):
    """CLI Tests"""

    main(
        [
            "preflight",
            "--cron",
            "13 3 * * *",
            "--max-results",
            "3",
            "now/d+13h+17m",
        ]
    )
    captured = capsys.readouterr()

    assert json.loads(captured.out) == {
        "expression": "now/d+13h+17m",
        "cron": "13 3 * * *",
        "yields": [
            "2024-01-03T13:17:00+00:00",
            "2024-01-04T13:17:00+00:00",
            "2024-01-05T13:17:00+00:00",
        ],
    }


@time_machine.travel(dt.datetime(2024, 1, 28, 1, 1, 1, tzinfo=UTC_ZONEINFO))
def test_main_c(capsys):
    """CLI Tests"""

    main(
        [
            "preflight",
            "--cron",
            "13 3 28-31 * *",
            "--max-results",
            "12",
            "now/M+1M:sat-1w /* last saturday of the month */",
        ]
    )
    captured = capsys.readouterr()

    assert json.loads(captured.out) == {
        "expression": "now/M+1M:sat-1w /* last saturday of the month */",
        "cron": "13 3 28-31 * *",
        "yields": [
            *["2024-01-27T00:00:00+00:00"] * 4,
            *["2024-02-24T00:00:00+00:00"] * 2,
            *["2024-03-30T00:00:00+00:00"] * 4,
            *["2024-04-27T00:00:00+00:00"] * 2,
        ],
    }


@patch(
    "sys.argv",
    [
        "",
        "preflight",
        "--cron",
        "13 3 28-31 * *",
        "--max-results",
        "1",
        "now/M+1M:sat-1w",
    ],
)
@time_machine.travel(dt.datetime(2024, 1, 28, 1, 1, 1, tzinfo=UTC_ZONEINFO))
def test_main_d(capsys):
    """CLI Tests"""

    run()
    captured = capsys.readouterr()

    assert json.loads(captured.out) == {
        "expression": "now/M+1M:sat-1w",
        "cron": "13 3 28-31 * *",
        "yields": ["2024-01-27T00:00:00+00:00"],
    }
