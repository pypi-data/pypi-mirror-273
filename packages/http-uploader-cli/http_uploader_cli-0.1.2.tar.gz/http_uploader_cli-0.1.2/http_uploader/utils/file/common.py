from pathlib import Path
from typing import Protocol


class FileReader(Protocol):
    file_path: Path

    async def read(
        self,
        start_offset: int,
        end_offset: int,
    ) -> list[str]: ...

    async def file_length(self) -> int: ...

    async def bytes_count(self) -> int: ...
