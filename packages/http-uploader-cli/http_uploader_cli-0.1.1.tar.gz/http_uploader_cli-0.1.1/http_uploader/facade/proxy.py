from dataclasses import dataclass
from typing import final

from http_uploader.cli.engine.dto.response import CLIResponse
from http_uploader.facade.common import CLIApplication


@final
@dataclass(frozen=True)
class CLIApplicationProxy(CLIApplication):
    _app: CLIApplication

    async def run(self) -> CLIResponse:
        return await self._app.run()
