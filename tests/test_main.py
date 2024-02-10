import datetime as dt
import json
import os
from unittest.mock import patch

import pytest
import time_machine

from dateexpressions.parse import main


@time_machine.travel(dt.datetime(2024, 1, 2, 14, 15, 16), tick=False)
def test_main_isoformat(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["isoformat", "now-78h/h"])
    captured = capsys.readouterr()
    assert "2023-12-30T08:00:00+00:00" in captured.out


@pytest.mark.skipif(
    os.environ.get("PREFLIGHT") != "true",
    reason="applicable only if installed with [preflight]",
)
@time_machine.travel(dt.datetime(2024, 1, 28, 1, 1, 1))
def test_main_preflight(capsys):
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
