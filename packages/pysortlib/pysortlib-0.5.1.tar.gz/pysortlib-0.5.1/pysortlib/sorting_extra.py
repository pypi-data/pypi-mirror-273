from __future__ import annotations

import concurrent.futures
import time
from itertools import chain, repeat

from .utils import check_negative_integers


def counting_sort(array: list[int], *, max_value: int) -> list[int]:
    """
    Sorts an array of integers using the counting sort algorithm.

    Time complexity: O(n+k), where:
     - n is the length of the array
     - k is the maximum value in the array

    Extra space complexity: O(n+k), where:
     - n is the length of the array
     - k is the maximum value in the array

    Stable: Yes (the relative order of equal elements is preserved).
    In-place: No (the input array is not modified).

    :param array: array of integers
    :param max_value: maximum value in the array
    :raises: ValueError: if the array contains negative integers
    :return: sorted array of integers
    """
    check_negative_integers(array)

    count_of_each_integer = list(repeat(0, max_value + 1))
    for num in array:
        count_of_each_integer[num] += 1

    for i in range(1, max_value + 1):
        count_of_each_integer[i] += count_of_each_integer[i - 1]

    result = list(repeat(0, len(array)))
    for num in reversed(array):
        count_of_each_integer[num] -= 1
        result[count_of_each_integer[num]] = num

    return result


def radix_sort(array: list[int], *, max_digits: int, base: int = 10) -> list[int]:
    """
    Sorts an array of integers using the radix sort algorithm.

    Time complexity: O(d*(n+k)), where:
     - d is the number of digits in the largest number
     - n is the length of the array
     - k is the number of possible digits (the base)

    Extra space complexity: O(n+k), where:
     - n is the length of the array
     - k is the number of possible digits (the base)

    Stable: Yes (the relative order of equal elements is preserved).
    In-place: Yes (the input array is modified).

    :param array: array of integers
    :param max_digits: number of digits in the largest number
    :param base: base of the numbers, default is 10
    :raises: ValueError: if the array contains negative integers
    :return: sorted array of integers
    """
    check_negative_integers(array)

    for i in range(max_digits):
        bins: list[list[int]] = [[] for _ in range(base)]
        for num in array:
            digit = (num // base**i) % base
            bins[digit].append(num)

        array = list(chain.from_iterable(bins))

    return array


def _shut_up_for(secs: int) -> int:
    time.sleep(secs)
    return secs


def sleep_sort(array: list[int]) -> list[int]:
    """
    Sorts an array of integers using the sleep sort algorithm.

    Time complexity: O(n), where n is the length of the array.
    Extra space complexity: O(n), where n is the length of the array.

    :param array: array of integers
    :return: sorted array of integers
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(_shut_up_for, num) for num in array]
        iterator = concurrent.futures.as_completed(futures)

        return [future.result() for future in iterator]
