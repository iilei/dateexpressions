from pathlib import Path

from relative_date import RelativeDate
from textx import metamodel_from_file

relative_date_meta_model = metamodel_from_file(
    Path.joinpath(Path(__file__).parent, "to_relative_date.tx"), use_regexp_group=True
)


def parse(expression: str = "now"):
    relative_date_model = relative_date_meta_model.model_from_str(expression)

    relative_date = RelativeDate()

    return relative_date.interpret(relative_date_model)


print(parse("now/y"))
