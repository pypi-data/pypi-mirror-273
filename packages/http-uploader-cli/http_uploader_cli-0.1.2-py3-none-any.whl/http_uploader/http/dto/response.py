from dataclasses import dataclass


@dataclass(frozen=True)
class HttpResponse:
    text: str
    status: int
