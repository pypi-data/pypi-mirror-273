from typing import Any, Iterator


def split_to_n_chunks(sequence: tuple, n: int) -> Iterator[tuple[Any, ...]]:
    parts_count = min(len(sequence), n)
    for i in range(parts_count):
        k, m = divmod(len(sequence), parts_count)
        yield sequence[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)]
