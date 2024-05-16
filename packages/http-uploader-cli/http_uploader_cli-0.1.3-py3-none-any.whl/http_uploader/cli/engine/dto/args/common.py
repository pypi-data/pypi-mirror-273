from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class UploaderArgs:
    url: str
    filter: str
    input_file: Path
    number_lines: int
    cpus_count: int
    coroutines_count: int
