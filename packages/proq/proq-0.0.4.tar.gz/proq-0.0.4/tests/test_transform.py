import operator

import pytest

from proq import transform, transform_parallel


@pytest.mark.parametrize(
    "pipeline_builder,expected",
    [
        (lambda: transform.Map(str, [0, 1]), ["0", "1"]),
        (lambda: transform.Filter(bool, [0, 1]), [1]),
        (lambda: transform.Reduce(operator.add, [1, 2]), [3]),
        (lambda: transform.ReduceInitial(lambda s, n: f"{s}{n}", [1, 2], ""), ["12"]),
        (lambda: transform.Flatten([[1, 2], [3, 4]]), [1, 2, 3, 4]),
        (lambda: transform_parallel.ParallelMap(str, [0, 1]), ["0", "1"]),
    ],
)
class TestTransform:
    def test_collect_returns_expected_value(self, pipeline_builder, expected):
        assert pipeline_builder().collect() == expected

    def test_collect_exhausts_input(self, pipeline_builder, expected):
        pipeline = pipeline_builder()
        pipeline.collect()
        assert pipeline.collect() == []

    def test_next_exhausts_input(self, pipeline_builder, expected):
        pipeline = pipeline_builder()
        for ex in expected:
            assert pipeline.next() == ex
        with pytest.raises(StopIteration):
            pipeline.next()
