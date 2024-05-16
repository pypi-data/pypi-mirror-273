import asyncio
import sys
from argparse import ArgumentParser

from prettytable import PrettyTable

from http_uploader.cli.engine.http_uploader import HTTPUploaderEngine
from http_uploader.facade.http_uploader import HTTPUploaderApplication
from http_uploader.facade.proxy import CLIApplicationProxy


async def main() -> None:
    response = await CLIApplicationProxy(
        HTTPUploaderApplication(
            HTTPUploaderEngine(
                ArgumentParser(),
                sys.argv[1:],
            ),
        ),
    ).run()
    table = PrettyTable(
        field_names=(
            " ".join(header.split("_")).capitalize() for header in response.data
        ),
    )
    table.add_row(response.data.values())
    print(table)  # noqa: T201


if __name__ == "__main__":
    asyncio.run(main())
