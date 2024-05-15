# Process Queue

Simplify data processing using pipelines.

- Inline

```python
# Create the numbers 1-10, square them, then sum the results
result = proq.create(range(11)).map(lambda x: x ** 2).reduce(lambda x, y: x + y).next()
```

- Procedurally

```python
# Create a square numbers proq and split into two
data1, data2 = proq.create(range(11)).map(lambda x: x ** 2).tee()

# negate one of the streams
data1_neg = data1.map(lambda x: -x)

# add 1 to the other
data2_plus_1 = data2.map(lambda x: x + 1)

# Iterate over the results
for d1, d2 in zip(data1_neg, data2_plus_1):
    print(d1, d2, d1 + d2)
    assert d1 + d2 == 1
```

- In parallel

```python
# Get prime numbers under 1,000,000 - calculation happens concurrently
primes = (
    proq.create(range(1000001))
        .par_map(lambda x: x, is_prime(x))
        .filter(lambda x, is_prime: is_prime)
        .map(lambda x, is_prime: x)
        .collect()
)
```

# Installation

```bash
pip install proq
```

# Development

- Download source
- Install development dependencies: `flit install -s --deps develop`
- Format code: `black .`
- Run tests: `pytest`
- Bump version in `src/proq/__init__.py`
- Build package: `flit build`
- Deploy: `flit publish`
