from __future__ import annotations

import collections
import os
import pickle
from concurrent import futures
from typing import Any, Callable, Generic, Iterable, Iterator

import dill  # type: ignore

from . import collectible
from .common import T, U


class ParallelMap(collectible.Collectible[U]):
    def __init__(
        self, f: Callable[[T], U], items: Iterable[T], parallelism: int | None = None
    ):
        self.f: SerializableCallable = SerializableCallable(f)
        self.items = items
        self.parallelism = parallelism or os.cpu_count() or 2
        super().__init__(self._get_iterator())

    def _get_iterator(self) -> Iterator[U]:
        tasks: collections.deque = collections.deque()
        with futures.ProcessPoolExecutor(max_workers=self.parallelism) as pool:
            for item in self.items:
                tasks.append(pool.submit(self.f, item))
                if len(tasks) > self.parallelism:
                    yield tasks.popleft().result()

            while tasks:
                yield tasks.popleft().result()


#
# Serialization functions:
#
class SerializableCallable(Generic[T]):
    def __init__(self, f: Callable):
        self.f = self._dumps_if_needed(f)

    def __call__(self, *args: Any) -> T:
        return self._loads_if_needed(self.f)(*args)

    @staticmethod
    def _dumps_if_needed(obj: Callable) -> Callable | bytes:
        try:
            pickle.dumps(obj)
            return obj
        except (AttributeError, pickle.PicklingError):
            return dill.dumps(obj)

    @staticmethod
    def _loads_if_needed(obj: Callable | bytes) -> Callable:
        if isinstance(obj, bytes):
            return dill.loads(obj)
        return obj
