from typing import Generic, Iterator

from .common import T


class Collectible(Generic[T]):
    def __init__(self, iterator: Iterator[T]):
        self._iterator = iterator

    def collect(self) -> list[T]:
        return list(self)

    def next(self) -> T:
        return next(self)

    def __iter__(self) -> Iterator[T]:
        return self._iterator

    def __next__(self) -> T:
        return next(self._iterator)
