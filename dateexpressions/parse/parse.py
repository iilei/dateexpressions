# inspired by
# https://github.com/grafana/grafana/blob/main/packages/grafana-data/src/datetime/rangeutil.ts

from relative_date import RelativeDate
from textx import metamodel_from_file

relative_date_meta_model = metamodel_from_file(
    "dateexpressions/parse/to_relative_date.tx", use_regexp_group=True
)


relative_date_model = relative_date_meta_model.model_from_str("now-78d/M+2h")

relative_date = RelativeDate()

print(relative_date.interpret(relative_date_model))
