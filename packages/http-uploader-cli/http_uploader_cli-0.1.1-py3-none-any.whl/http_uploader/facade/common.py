from typing import Protocol

from http_uploader.cli.engine.dto.response import CLIResponse


class CLIApplication(Protocol):
    async def run(self) -> CLIResponse: ...
