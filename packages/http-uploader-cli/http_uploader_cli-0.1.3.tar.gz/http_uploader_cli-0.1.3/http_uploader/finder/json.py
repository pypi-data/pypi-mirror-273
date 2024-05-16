import re
from dataclasses import dataclass
from numbers import Number
from typing import Any, Optional, final

from http_uploader.finder.common import Finder


@final
@dataclass(frozen=True)
class JsonFinder(Finder):
    json: dict[str | Number, Any] | list

    @classmethod
    def from_json(cls, json: dict[str | Number, Any] | list) -> Finder:
        return cls(json)

    def search(self, path: str) -> Optional[str | Number | bool]:
        keys = path.split(".")
        current_json = self.json.copy()
        for key in keys:
            index_match = re.match(r"\[(\d+)\]", key)
            if isinstance(current_json, list) and index_match:
                index = int(index_match.groups()[0])
                if index < len(current_json):
                    current_json = current_json[index]
            if isinstance(current_json, dict) and not index_match and key in current_json:
                current_json = current_json[key]
            if isinstance(current_json, str | Number | bool):
                return current_json
        return None


def create_json_finder(json: dict[str | Number, Any] | list) -> Finder:
    return JsonFinder(json)
