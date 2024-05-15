from typing import Iterable

import pytest

import proq


def test_proq_create_collect():
    assert proq.create([0, 1, 2, 3]).collect() == [0, 1, 2, 3]


def test_proq_collect_exhausts_input():
    p = proq.create([0, 1, 2, 3])
    assert p.collect() == [0, 1, 2, 3]
    assert p.collect() == []


def test_proq_append_adds_to_back():
    assert proq.create([0, 1]).append([2, 3]).collect() == [0, 1, 2, 3]


def test_proq_prepend_adds_to_front():
    assert proq.create([2, 3]).prepend([0, 1]).collect() == [0, 1, 2, 3]


def test_proq_flatten_flattens_output():
    assert proq.create([[0, 1], [2, 3]]).flatten().collect() == [0, 1, 2, 3]


def test_proq_map_modifies_output():
    assert proq.create([0, 1, 2, 3]).map(lambda x: x + 1).collect() == [1, 2, 3, 4]


def test_proq_flatmap_modifies_output():
    assert proq.create([0, 1]).flat_map(lambda x: (x, x)).collect() == [0, 0, 1, 1]


def test_proq_foreach_does_not_modify_output():
    array = []
    assert proq.create([0, 1, 2, 3]).foreach(array.append).collect() == [0, 1, 2, 3]
    assert array == [0, 1, 2, 3]


def test_proq_filter_keeps_items_evaluated_to_true():
    assert proq.create([0, 1, 2, 3]).filter(lambda x: x % 2 == 0).collect() == [0, 2]


def test_proq_reduce_returns_aggregated_result():
    assert proq.create([0, 1, 2, 3]).reduce(lambda x, y: x + y).collect() == [6]
    assert proq.create([0, 1, 2, 3]).reduce(lambda x, y: x + y).next() == 6


def test_proq_reduce_returns_only_object():
    assert proq.create([0]).reduce(lambda x, y: x + y).next() == 0
    assert proq.create([]).reduce(lambda x, y: x + y, 0).next() == 0


def test_proq_reduce_without_object_raises():
    with pytest.raises(TypeError, match="reduce"):
        assert proq.create([]).reduce(lambda x, y: x + y).next() == 0


def test_proq_tee_duplicates_items():
    a, b = proq.create([0, 1, 2, 3]).tee()
    assert a.collect() == b.collect() == [0, 1, 2, 3]


def test_proq_par_map_modifies_output():
    assert proq.create([0, 1, 2, 3]).par_map(lambda x: x + 1).collect() == [1, 2, 3, 4]


#
# Lazy Evaluation
#
def test_proq_map_is_lazy():
    p = proq.create([1, 2]).map(_raise_runtime_foo)
    with pytest.raises(RuntimeError, match="foo"):
        p.next()


def test_proq_foreach_is_lazy():
    p = proq.create([1, 2]).foreach(_raise_runtime_foo)
    with pytest.raises(RuntimeError, match="foo"):
        p.next()


def test_proq_filter_is_lazy():
    p = proq.create([1, 2]).filter(_raise_runtime_foo)
    with pytest.raises(RuntimeError, match="foo"):
        p.next()


def test_proq_reduce_is_lazy():
    p = proq.create([1, 2]).reduce(_raise_runtime_foo)
    with pytest.raises(RuntimeError, match="foo"):
        p.next()


def test_proq_par_map_is_lazy():
    p = proq.create([1, 2]).par_map(_raise_runtime_foo)
    with pytest.raises(RuntimeError, match="foo"):
        p.next()


def _raise_runtime_foo(*_):
    raise RuntimeError("foo")


#
# Allowed inputs
#
@pytest.mark.parametrize(
    "iterable",
    [
        [0, 1],
        (0, 1),
        range(2),
        iter(range(2)),
        (i for i in range(2)),
        {0, 1},
        {0: "a", 1: "b"},
    ],
)
def test_proq_accepts_iterable(iterable: Iterable[int]):
    assert sorted(proq.create(iterable)) == [0, 1]
