import operator
from dataclasses import dataclass, field
from typing import Any, Callable, Literal, final

from http_uploader.utils.filter.common import Filter
from http_uploader.utils.filter.compare import CompareFilter


@final
@dataclass(frozen=True)
class ExtentedCompareFilter(CompareFilter):
    operator: Literal["==", "!=", ">", ">=", "<", "<="]  # type: ignore[assignment]

    _ext_operators: dict[str, Callable[[Any, Any], bool]] = field(
        init=False,
        default_factory=lambda: {
            ">": operator.gt,
            ">=": operator.ge,
            "<": operator.lt,
            "<=": operator.le,
        },
    )

    def check(self, obj: str | float | bool) -> bool:
        if self._operators.get(self.operator):
            return super().check(obj)
        return self._ext_operators[self.operator](self.comparable_value, obj)


def create_extented_compare_filter(
    operator: Literal["==", "!=", ">", ">=", "<", "<="],
    comparable_value: int,
) -> Filter:
    return ExtentedCompareFilter(operator, comparable_value)
