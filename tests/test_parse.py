import datetime as dt

import pytest
import time_machine

from dateexpressions.parse import ZoneInfo, parse

UTC_ZONEINFO = ZoneInfo(key="UTC")
SOME_DAY = dt.datetime(2024, 1, 24, 14, 15, 16, tzinfo=UTC_ZONEINFO)


def test_parse_given_time():
    assert parse("", SOME_DAY).isoformat() == "2024-01-24T14:15:16+00:00"


@time_machine.travel(SOME_DAY, tick=False)
def test_parse_system_time():
    assert parse("now").isoformat() == "2024-01-24T14:15:16+00:00"


@time_machine.travel(SOME_DAY, tick=False)
def test_parse_floor_units():
    assert parse("now/m").isoformat() == "2024-01-24T14:15:00+00:00"
    assert parse("now/h").isoformat() == "2024-01-24T14:00:00+00:00"
    assert parse("now/d").isoformat() == "2024-01-24T00:00:00+00:00"
    assert parse("now/w").isoformat() == "2024-01-22T00:00:00+00:00"
    assert parse("now/M").isoformat() == "2024-01-01T00:00:00+00:00"
    assert parse("now/y").isoformat() == "2024-01-01T00:00:00+00:00"


@time_machine.travel(SOME_DAY, tick=False)
def test_parse_floor_and_shift_units():
    assert parse("now/m+1m").isoformat() == "2024-01-24T14:16:00+00:00"
    assert parse("now/h+1h").isoformat() == "2024-01-24T15:00:00+00:00"
    assert parse("now/d+1d").isoformat() == "2024-01-25T00:00:00+00:00"
    assert parse("now/w+1w").isoformat() == "2024-01-29T00:00:00+00:00"
    assert parse("now/M+1M").isoformat() == "2024-02-01T00:00:00+00:00"
    assert parse("now/y+1y").isoformat() == "2025-01-01T00:00:00+00:00"


@time_machine.travel(SOME_DAY, tick=False)
def test_shift_units():
    assert parse("now+1s").isoformat() == "2024-01-24T14:15:17+00:00"
    assert parse("now+1m").isoformat() == "2024-01-24T14:16:16+00:00"
    assert parse("now+1h").isoformat() == "2024-01-24T15:15:16+00:00"
    assert parse("now+1d").isoformat() == "2024-01-25T14:15:16+00:00"
    assert parse("now+1w").isoformat() == "2024-01-31T14:15:16+00:00"


@time_machine.travel(SOME_DAY, tick=False)
def test_weekdays():
    assert parse("now/M+1M:mon").isoformat() == "2024-02-05T00:00:00+00:00"
    assert parse("now/M+1M:tue").isoformat() == "2024-02-06T00:00:00+00:00"
    assert parse("now/M+1M:wed").isoformat() == "2024-02-07T00:00:00+00:00"
    assert parse("now/M+1M:thu").isoformat() == "2024-02-01T00:00:00+00:00"
    assert parse("now/M+1M:fri").isoformat() == "2024-02-02T00:00:00+00:00"
    assert parse("now/M+1M:sat").isoformat() == "2024-02-03T00:00:00+00:00"
    assert parse("now/M+1M:sun").isoformat() == "2024-02-04T00:00:00+00:00"


@time_machine.travel(SOME_DAY, tick=False)
def test_tz_aware():
    assert parse("now(Europe/Berlin)") == dt.datetime.now(ZoneInfo(key="Europe/Berlin"))


@time_machine.travel(SOME_DAY, tick=False)
def test_tz_aware_named_param():
    assert parse("now(timezone=Europe/Amsterdam)") == dt.datetime.now(ZoneInfo(key="Europe/Amsterdam"))


def test_no_naive_month():
    with pytest.raises(Exception):
        # Because a month is not a fixed duration, Deltas with unit=Month are only
        # applicable directly after a `Floor to Month` Operation
        parse("now-1M")


def test_no_naive_year():
    with pytest.raises(Exception):
        # Because a year is not a fixed duration, Deltas with unit=year are only
        # applicable directly after a `Floor to Year` Operation
        parse("now-1y")


@time_machine.travel(SOME_DAY, tick=False)
def test_multiline_inline_comments():
    assert (
        parse(
            """
                now /h
                /*
                beginning of the current hour
                */
                +2m
                /* just because */
                -0h
                /* ... */
                +3s
        """
        )
        == dt.datetime(2024, 1, 24, 14, 2, 3, tzinfo=UTC_ZONEINFO)
    )


@time_machine.travel(SOME_DAY, tick=False)
def test_scenarios_as_documented():
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
