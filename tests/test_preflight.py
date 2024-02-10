import datetime as dt
import os

import pytest
import time_machine

from dateexpressions.parse import ZoneInfo, preflight

UTC_ZONEINFO = ZoneInfo(key="UTC")
SOME_DAY = dt.datetime(2024, 1, 24, 14, 15, 16, tzinfo=UTC_ZONEINFO)


@pytest.mark.skipif(
    os.environ.get("PREFLIGHT") != "true",
    reason="applicable only if installed with [preflight]",
)
@time_machine.travel(dt.datetime(2024, 1, 28, 1, 1, 1, tzinfo=UTC_ZONEINFO))
def test_preflight():
    """CLI Tests"""

    result = preflight(
        expression="now/M+1M:sat-1w", cron="13 3 28-31 * *", max_results=12
    )

    assert result == [
        *[dt.datetime(2024, 1, 27, tzinfo=UTC_ZONEINFO)] * 4,
        *[dt.datetime(2024, 2, 24, tzinfo=UTC_ZONEINFO)] * 2,
        *[dt.datetime(2024, 3, 30, tzinfo=UTC_ZONEINFO)] * 4,
        *[dt.datetime(2024, 4, 27, tzinfo=UTC_ZONEINFO)] * 2,
    ]


@pytest.mark.skipif(
    os.environ.get("PREFLIGHT") == "true",
    reason="applicable only if NOT installed with [preflight]",
)
def test_preflight_raises():
    with pytest.raises(EnvironmentError):
        preflight("13 3 28-31 * *", "", 1)
