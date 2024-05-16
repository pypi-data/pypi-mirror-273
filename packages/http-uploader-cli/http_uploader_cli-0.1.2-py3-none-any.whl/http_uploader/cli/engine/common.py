from typing import Protocol

from http_uploader.cli.engine.dto.args import UploaderArgs


class UploaderEngine(Protocol):
    def configure(self) -> UploaderArgs: ...
