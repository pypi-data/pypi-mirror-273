from __future__ import annotations


def swap(array: list[int], index_1: int, index_2: int) -> None:
    """Swap two elements in the array."""
    array[index_1], array[index_2] = array[index_2], array[index_1]


def check_negative_integers(array: list[int]) -> None:
    """Check if the array contains only non-negative integers."""
    if any(num < 0 for num in array):
        msg = "The array should contain only non-negative integers"
        raise ValueError(msg)
