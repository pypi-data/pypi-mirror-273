from typing import Any, Protocol

from http_uploader.http.dto.response import HttpResponse


class HTTPClient(Protocol):
    async def send_request(self, data: dict[str, Any]) -> HttpResponse: ...
