import datetime
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ClientRequestBody:
    data: tuple[dict[str, Any], ...]
    timestamp: int = field(
        default_factory=lambda: int(datetime.datetime.now().timestamp()),  # noqa: DTZ005
    )

    to_dict = asdict
