from dataclasses import dataclass
from pathlib import Path
from typing import final

import aiofiles

from http_uploader.utils.file.common import FileReader


@final
@dataclass
class TxtReader(FileReader):
    file_path: Path

    @classmethod
    def from_file_path(cls, file_path: Path) -> FileReader:
        return cls(file_path)

    async def read(
        self,
        start_offset: int,
        end_offset: int,
    ) -> list[str]:
        lines = []
        async with aiofiles.open(self.file_path) as file:
            current_line_idx = 0
            async for line in file:
                if current_line_idx >= start_offset - 1 and current_line_idx < end_offset:
                    lines.append(line.strip("\n"))
                current_line_idx += 1
        return lines

    async def file_length(self) -> int:
        length = 0
        async with aiofiles.open(self.file_path) as file:
            async for _ in file:
                length += 1
        return length

    async def bytes_count(self) -> int:
        bytes_count = 0
        async with aiofiles.open(self.file_path) as file:
            async for line in file:
                bytes_count += len(line)
        return bytes_count
