from numbers import Number
from typing import Optional, Protocol


class Finder(Protocol):
    def search(self, path: str) -> Optional[str | Number | bool]: ...
