import datetime as dt
import json
from unittest.mock import patch
from zoneinfo import ZoneInfo

import pytest
import time_machine

from dateexpressions.parse import main, parse, run

UTC_ZONEINFO = ZoneInfo(key="UTC")


@time_machine.travel(
    dt.datetime(2024, 1, 24, 14, 15, 16, tzinfo=UTC_ZONEINFO), tick=False
)
def test_parse():
    """API Tests"""
    assert (
        parse("", dt.datetime(1984, 1, 1, tzinfo=UTC_ZONEINFO)).isoformat()
        == "1984-01-01T00:00:00+00:00"
    )

    assert parse("now") == dt.datetime(2024, 1, 24, 14, 15, 16, tzinfo=UTC_ZONEINFO)
    assert parse("now(Europe/Berlin)") == dt.datetime.now(ZoneInfo(key="Europe/Berlin"))
    assert parse("now(timezone=Europe/Amsterdam)") == dt.datetime.now(
        ZoneInfo(key="Europe/Amsterdam")
    )

    assert parse("now/M+1M:sat-1w /* last saturday this month */") == dt.datetime(
        2024, 1, 27, tzinfo=UTC_ZONEINFO
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
            "now/d+13h+13m",
        ]
    )
    captured = capsys.readouterr()

    assert json.loads(captured.out) == {
        "expression": "now/d+13h+13m",
        "cron": "13 3 * * *",
        "yields": [
            "2024-01-03T13:13:00+00:00",
            "2024-01-04T13:13:00+00:00",
            "2024-01-05T13:13:00+00:00",
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
            "now/M+1M:sat-1w",
        ]
    )
    captured = capsys.readouterr()

    assert json.loads(captured.out) == {
        "expression": "now/M+1M:sat-1w",
        "cron": "13 3 28-31 * *",
        "yields": [
            "2024-01-27T00:00:00+00:00",
            "2024-01-27T00:00:00+00:00",
            "2024-01-27T00:00:00+00:00",
            "2024-01-27T00:00:00+00:00",
            "2024-02-24T00:00:00+00:00",
            "2024-02-24T00:00:00+00:00",
            "2024-03-30T00:00:00+00:00",
            "2024-03-30T00:00:00+00:00",
            "2024-03-30T00:00:00+00:00",
            "2024-03-30T00:00:00+00:00",
            "2024-04-27T00:00:00+00:00",
            "2024-04-27T00:00:00+00:00",
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
