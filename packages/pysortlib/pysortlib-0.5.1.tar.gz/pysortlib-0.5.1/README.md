# Python Sorting Library

[![PyPI](https://img.shields.io/pypi/v/pysortlib)](https://pypi.org/project/pysortlib)
[![Downloads](https://static.pepy.tech/badge/pysortlib)](https://pepy.tech/project/pysortlib)
[![Coverage](https://codecov.io/gh/slimreaper35/pysortlib/graph/badge.svg?token=S24DIT654W)](https://codecov.io/gh/slimreaper35/pysortlib)

Library of sorting algorithms with precise implementation and documentation.

## Algorithms

- Bubble sort
- Counting sort
- Cycle sort
- Heap sort
- Insert sort
- Merge sort
- Pancake sort
- Quick sort
- Radix sort
- Selection sort
- Shell sort
- Sleep sort

## Install

```bash
pip install pysortlib
```

## Usage

```python
from pysortlib import insert_sort

array = [3, 5, 2, 1, 7, 4, 6]
insert_sort(array)  # set a breakpoint and explore \o/
print(array)
```

## Development

### Virtual environment

```bash
pip install --user poetry
poetry config virtualenvs.in-project true
poety shell
poetry install
```

### Dependencies

```bash
poetry update
```

### Pre-commit

```bash
pre-commit clean
pre-commit install --hook-type pre-commit
```

### Coding standards

- ~~perfectionism~~
- [black](https://black.readthedocs.io/en/stable/) - code formatting
- [ruff](https://beta.ruff.rs/docs/) - static code analysis
- [mypy](https://mypy.readthedocs.io/en/stable/) - static type checking
- [pytest](https://docs.pytest.org/en/stable/) - unit tests
