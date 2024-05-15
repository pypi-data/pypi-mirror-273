from __future__ import annotations

import functools
from typing import Callable, Iterable, Iterator

from . import collectible
from .common import T, U


class Map(collectible.Collectible[U]):
    def __init__(self, f: Callable[[T], U], items: Iterable[T]):
        self.f = f
        self.items = items
        super().__init__(self._get_iterator())

    def _get_iterator(self) -> Iterator[U]:
        return map(self.f, self.items)


class Filter(collectible.Collectible[T]):
    def __init__(self, f: Callable[[T], bool], items: Iterable[T]):
        self.f = f
        self.items = items
        super().__init__(self._get_iterator())

    def _get_iterator(self) -> Iterator[T]:
        return filter(self.f, self.items)


class Flatten(collectible.Collectible[T]):
    def __init__(self, items: Iterable[Iterable[T]]):
        self.items = items
        super().__init__(self._get_iterator())

    def _get_iterator(self) -> Iterator[T]:
        for item in self.items:
            yield from item


class Reduce(collectible.Collectible[T]):
    def __init__(self, f: Callable[[T, T], T], items: Iterable[T]):
        self.f = f
        self.items = items
        super().__init__(self._get_iterator())

    def _get_iterator(self) -> Iterator[T]:
        yield functools.reduce(self.f, self.items)


class ReduceInitial(collectible.Collectible[T]):
    def __init__(self, f: Callable[[T, U], T], items: Iterable[U], initial: T):
        self.f = f
        self.items = items
        self.initial = initial
        super().__init__(self._get_iterator())

    def _get_iterator(self) -> Iterator[T]:
        print(self, self.f, self.items, self.initial)
        yield functools.reduce(self.f, self.items, self.initial)
