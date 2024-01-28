from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

units = {
    "s": "seconds",
    "d": "days",
    "m": "minutes",
    "h": "hours",
    "w": "weeks",
    "M": "months",
    "y": "years",
}


class RelativeDate:
    def __init__(self):
        self.timezone = ZoneInfo("UTC")
        self.result = datetime.now(self.timezone)
        self.yield_fmt = "%Y-%m-%d %H:%M:%S"

    def __str__(self):
        return self.result.strftime(self.yield_fmt)

    def interpret(self, model):
        if model.now:
            if model.now.timezone:
                self.timezone = ZoneInfo(model.now.timezone)
            self.result = datetime.now(self.timezone)

        for c in model.statements:
            if c.__class__.__name__ == "DeltaStatement":

                self.result = self.result + timedelta(
                    **{units[c.unit]: c.value * -1 if c.sign == "-" else c.value}
                )

            if c.__class__.__name__ == "FloorStatement":
                specificy = ["years", "months", "days", "hours", "minutes", "seconds"]

                if units.get(c.unit) in specificy:
                    index_of_specificy = specificy.index(units[c.unit]) + 1
                    ensured_minimum_args = [
                        *self.result.timetuple()[0:index_of_specificy],
                        *[1, 1, 1][0:-index_of_specificy],
                    ]

                    self.result = datetime(*ensured_minimum_args, tzinfo=self.timezone)

                if units.get(c.unit) == "weeks":
                    self.result = self.result - timedelta(days=self.result.weekday())

                    # week specificy: start of day
                    self.result = datetime(
                        *self.result.timetuple()[0:3], tzinfo=self.timezone
                    )

        return self.result
