from typing import Protocol


class Filter(Protocol):
    operator: str
    comparable_value: str | float | bool

    def check(self, obj: str | float | bool) -> bool: ...
