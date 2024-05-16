from dataclasses import dataclass
from typing import Any, final

from aiohttp import ClientSession

from http_uploader.http.common import HTTPClient
from http_uploader.http.dto.response import HttpResponse


@final
@dataclass(frozen=True)
class PostHTTPClient(HTTPClient):
    url: str
    client: ClientSession

    @classmethod
    def from_url(cls, url: str) -> HTTPClient:
        return cls(url, ClientSession())

    async def send_request(self, data: dict[str, Any]) -> HttpResponse:
        async with self.client as session:  # noqa: SIM117
            async with session.post(self.url, json=data) as response:
                return HttpResponse(await response.text("utf-8"), response.status)
