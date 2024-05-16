from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CLIResponse:
    data: dict[str, Any]
