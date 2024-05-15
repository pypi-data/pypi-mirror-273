from __future__ import annotations

import functools
import itertools
from typing import Callable, Iterable

from . import collectible, transform, transform_parallel
from .common import T, U


def create(objects: Iterable[T]) -> Proq[T]:
    return Proq(objects)


class Proq(collectible.Collectible[T]):
    def __init__(self, items: Iterable[T]):
        self.items = items
        super().__init__(iter(items))

    def append(self, items: Iterable[T]) -> Proq[T]:
        return Proq(itertools.chain(self, items))

    def prepend(self, items: Iterable[T]) -> Proq[T]:
        return Proq(itertools.chain(items, self))

    def flatten(self: Proq[Iterable[T]]) -> Proq[T]:
        return Proq(transform.Flatten(self))

    def map(self, f: Callable[[T], U]) -> Proq[U]:
        return Proq(transform.Map(f, self))

    def flat_map(self, f: Callable[[T], Iterable[U]]) -> Proq[Iterable[U]]:
        return self.map(f).flatten()

    def foreach(self, f: Callable[[T], U]) -> Proq[T]:
        def _foreach(item: T) -> T:
            f(item)
            return item

        return self.map(_foreach)

    def filter(self, f: Callable[[T], bool]) -> Proq[T]:
        return Proq(transform.Filter(f, self))

    def reduce(self, f: Callable[[T, T], T], initial: T | None = None) -> Proq[T]:
        if initial is None:
            return Proq(transform.Reduce(f, self))
        return Proq(transform.ReduceInitial(f, self, initial))

    def tee(self, n: int = 2) -> tuple[Proq[T], ...]:
        return tuple(Proq(iterator) for iterator in itertools.tee(self, n))

    def par_map(self, f: Callable[[T], U], max_tasks: int | None = None) -> Proq[U]:
        return Proq(transform_parallel.ParallelMap(f, self, max_tasks))
