import operator as op
from dataclasses import dataclass, field
from typing import Any, Callable, Literal

from http_uploader.utils.filter.common import Filter


@dataclass(frozen=True)
class CompareFilter(Filter):
    operator: Literal["==", "!="]
    comparable_value: str | float | bool

    _operators: dict[str, Callable[[Any, Any], bool]] = field(
        init=False,
        default_factory=lambda: {
            "==": op.eq,
            "!=": op.ne,
        },
    )

    def check(self, obj: str | float | bool) -> bool:
        return self._operators[self.operator](self.comparable_value, obj)
