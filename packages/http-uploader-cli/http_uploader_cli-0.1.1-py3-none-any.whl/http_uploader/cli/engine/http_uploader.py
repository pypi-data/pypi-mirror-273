from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import final

from http_uploader.cli.engine.common import UploaderEngine
from http_uploader.cli.engine.dto.args import UploaderArgs


@final
@dataclass(frozen=True)
class HTTPUploaderEngine(UploaderEngine):
    _parser: ArgumentParser
    args: list[str]

    def configure(self) -> UploaderArgs:
        self._parser.add_argument("--url", type=str, help="Service to send POST")
        self._parser.add_argument(
            "--filter",
            type=str,
            help="Filter (default None)",
            default=None,
        )
        self._parser.add_argument(
            "--input-file",
            type=Path,
            help="Path to txt file",
            required=True,
        )
        self._parser.add_argument(
            "--n-lines",
            type=int,
            help="Number of lines to send (default all)",
        )
        self._parser.add_argument(
            "--cpus",
            type=int,
            help="Proccesses to use for reading file (default 4)",
            default=4,
        )
        self._parser.add_argument(
            "--coroutines",
            type=int,
            help="Requests amount to send (default 1)",
            default=1,
        )
        parsed_args = self._parser.parse_args(self.args)
        return UploaderArgs(
            url=parsed_args.url,
            filter=parsed_args.filter,
            input_file=parsed_args.input_file,
            number_lines=parsed_args.n_lines,
            cpus_count=parsed_args.cpus,
            coroutines_count=parsed_args.coroutines,
        )
