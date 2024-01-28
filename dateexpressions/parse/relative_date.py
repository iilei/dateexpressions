from datetime import datetime
from zoneinfo import ZoneInfo

# const units: Record<string, number> = {
#   w: 604800,
#   d: 86400,
#   h: 3600,
#   m: 60,
#   s: 1,
# };

class Delta:
    def __init__(self) -> None:
        ...
    

        
class RelativeDate:
    def __init__(self):
        self.timezone = ZoneInfo("UTC")
        self.now = datetime.now(self.timezone)
        self.result = datetime.now(self.timezone)
        self.yield_fmt = "%Y-%m-%d %H:%M:%S"

    def __str__(self):
        return self.result.strftime(self.yield_fmt)    



    def interpret(self, model):
        # model is an instance of Program
        for c in model.statements:

            if c.__class__.__name__ == "NowStatement":
                if c.timezone:
                    self.timezone = ZoneInfo(c.timezone)

                self.now = datetime.now(tz=self.timezone)
                
            if c.__class__.__name__ == "DeltaStatement":
                # TBD
                c.value
                c.operation
                c.unit


            if c.__class__.__name__ == "Add":
                # TBD
                c.delta

            if c.__class__.__name__ == "Sub":
                # TBD
                c.delta

            if c.__class__.__name__ == "Operation":
                # TBD
                c.operation

            if c.__class__.__name__ == "Unit":
                # TBD
                c.delta

            if c.__class__.__name__ == "FloorStatement":
                # TBD
                ...