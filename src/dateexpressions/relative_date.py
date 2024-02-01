from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

units = {
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
    "d": "days",
    "w": "weeks",
    "M": "months",
    "y": "years",
}
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
EARLIEST_FLOOR = [1, 1, 1, 0, 0, 0, 0]


class RelativeDate:
    def __init__(self):
        self.timezone = ZoneInfo("UTC")
        self.result = datetime.now(self.timezone)
        self.yield_fmt = "%Y-%m-%d %H:%M:%S"
        self.positions = ["y", "M", "d", "h", "m", "s"]

    def __str__(self):
        return self.result.strftime(self.yield_fmt)

    def interpret(self, model):
        if model.now:
            if model.now.timezone:
                self.timezone = ZoneInfo(model.now.timezone)
            self.result = datetime.now(self.timezone)

        for c in model.statements:
            if c.__class__.__name__ in ["FixedDelta"]:
                self.result = self.result + timedelta(**dict([(units[c.unit], c.value)]))

            if c.__class__.__name__ in ["MonthFloor", "YearFloor", "Floor"]:
                value = (
                    c.delta.value
                    if hasattr(c, "delta") and hasattr(c.delta, "value")
                    else 0
                )
                day = (
                    c.day.value
                    if hasattr(c, "day") and hasattr(c.day, "value")
                    else False
                )
                unit = c.unit
                tt = [*self.result.timetuple()]

                resolution = self.positions.index(unit) + 1

                floored = [*tt[0:resolution], *EARLIEST_FLOOR[resolution:]]

                self.result = datetime(*floored, tzinfo=self.timezone)

                tt = [*self.result.timetuple()]

                if unit in ["M", "y"]:
                    m = value * 12 if unit == "y" else value
                    ye = tt[0] = tt[0] + ((tt[1] + m) // 12)
                    mo = (tt[1] + m) % 12
                    self.result = datetime(ye, mo, 1, 0, 0, 0, tzinfo=self.timezone)

                    if day:
                        wday_result = self.result.timetuple().tm_wday
                        wday_dest = WEEKDAYS.index(day)
                        wday_delta = wday_dest - wday_result
                        self.result = self.result + timedelta(days=wday_delta)

                elif hasattr(c, "unit") and hasattr(c, "value") and units.get(c.unit):
                    self.result = self.result + timedelta(
                        **dict([(units[c.unit], value)])
                    )

        return self.result
