# inspired by / based on:
# src https://github.com/grafana/grafana/blob/main/packages/grafana-ui/src/components/DateTimePickers/RelativeTimeRangePicker/utils.ts
# https://github.com/grafana/grafana/blob/main/packages/grafana-data/src/datetime/rangeutil.ts

from textx import metamodel_from_file
from relative_date import RelativeDate

relative_date_meta_model = metamodel_from_file("dateexpressions/parse/to_relative_date.tx", use_regexp_group=True)


relative_date_model = relative_date_meta_model.model_from_str("now(UTC)-1d")

relative_date = RelativeDate()
relative_date.interpret(relative_date_model)