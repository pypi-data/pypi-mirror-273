import asyncio
import json
from dataclasses import dataclass
from itertools import chain
from typing import Any, final

from aiomultiprocess import Pool

from http_uploader.cli.engine import UploaderEngine
from http_uploader.cli.engine.dto.args import UploaderArgs
from http_uploader.cli.engine.dto.response import CLIResponse
from http_uploader.facade.common import CLIApplication
from http_uploader.finder import JsonFinder
from http_uploader.http.dto.client_request import ClientRequestBody
from http_uploader.http.post import PostHTTPClient
from http_uploader.utils.file import FileReader, TxtReader
from http_uploader.utils.filter import create_extented_compare_filter
from http_uploader.utils.parts import split_to_n_chunks


@final
@dataclass(frozen=True)
class HTTPUploaderApplication(CLIApplication):
    engine: UploaderEngine

    async def run(self) -> CLIResponse:
        args = self.engine.configure()
        file_reader = TxtReader.from_file_path(args.input_file)
        return await self._handle_file_and_send_request(file_reader, args)

    async def _handle_file_and_send_request(
        self,
        file_reader: FileReader,
        cli_args: UploaderArgs,
    ) -> CLIResponse:
        return await self._work_with_parts(file_reader, cli_args)

    async def _work_with_parts(
        self,
        file_reader: FileReader,
        cli_args: UploaderArgs,
    ) -> CLIResponse:
        lines_length = await file_reader.file_length()
        lines_num = tuple(range(lines_length))
        tasks = []
        async with Pool() as pool:
            for chunk in split_to_n_chunks(lines_num, cli_args.cpus_count):
                start_line = chunk[0] + 1
                end_line = start_line if len(chunk) == 1 else chunk[-1] + 1
                tasks.append(
                    pool.apply(
                        _handle_file_part,
                        (file_reader, (start_line, end_line), cli_args),
                    ),
                )
            return await self._send_to_endpoint(
                cli_args,
                await asyncio.gather(*tasks),
                file_reader,
            )

    async def _send_to_endpoint(
        self,
        cli_args: UploaderArgs,
        filtered_data: list[dict[str, Any]],
        file_reader: FileReader,
    ) -> CLIResponse:
        chained_data = tuple(chain.from_iterable(filtered_data))
        if cli_args.number_lines:
            chained_data = chained_data[: cli_args.number_lines]
        for data_chunk in split_to_n_chunks(chained_data, cli_args.coroutines_count):
            json_body = ClientRequestBody(data=data_chunk).to_dict()
            await PostHTTPClient.from_url(cli_args.url).send_request(
                json_body,
            )
        send_bytes = len(json.dumps(chained_data))
        skipped_bytes = await file_reader.bytes_count() - send_bytes
        return CLIResponse(
            {
                "send_lines": len(chained_data),
                "send_bytes": len(json.dumps(chained_data)),
                "skipped_lines": await file_reader.file_length() - len(chained_data),
                "skipped_bytes": (abs(skipped_bytes) + skipped_bytes) // 2,
            },
        )


async def _handle_file_part(
    file_reader: FileReader,
    positions_range: tuple[int, int],
    cli_args: UploaderArgs,
) -> list[dict[str, str | float | bool]]:
    readed_strings = await file_reader.read(*positions_range)
    if cli_args.filter:
        result = []
        for json_string in readed_strings:
            filter_operands = cli_args.filter.split()
            json_object = json.loads(json_string)
            found_value = JsonFinder.from_json(json_object).search(filter_operands[0])
            filtering_value = filter_operands[-1].strip("'\"")
            if not found_value:
                continue
            if create_extented_compare_filter(filter_operands[1], found_value).check(  # type: ignore[arg-type]
                filtering_value,
            ):
                result.append(json_object)
    else:
        result = readed_strings
    return result
