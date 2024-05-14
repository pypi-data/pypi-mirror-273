from __future__ import annotations

from pysortlib.utils import swap


def bubble_sort(array: list[int]) -> None:
    """
    Sorts an array of integers using the bubble sort algorithm.

    Time complexity: O(n^2), where n is the length of the array.
    Extra space complexity: O(1)

    Stable: Yes (the relative order of equal elements is preserved).
    In-place: Yes (the input array is modified).

    :param array: array of integers
    :return: None
    """
    length = len(array)
    for i in range(length):
        for j in range(length - i - 1):
            if array[j] > array[j + 1]:
                swap(array, j, j + 1)


def cycle_sort(array: list[int]) -> None:
    """
    Sorts an array of integers using the cycle sort algorithm.

    Time complexity: O(n^2), where n is the length of the array.
    Extra space complexity: O(1)

    Stable: No (the relative order of equal elements is not preserved).
    In-place: Yes (the input array is modified).

    :param array: array of integers
    :return: None
    """
    length = len(array)
    for i in range(length - 1):
        item = array[i]
        position = i

        for j in range(i + 1, length):
            if array[j] < item:
                position += 1

        if position == i:
            continue

        while item == array[position]:
            position += 1

        array[position], item = item, array[position]

        while position != i:
            position = i
            for j in range(i + 1, length):
                if array[j] < item:
                    position += 1

            while item == array[position]:
                position += 1

            array[position], item = item, array[position]


def _left_child(index: int) -> int:
    return 2 * index + 1


def _right_child(index: int) -> int:
    return 2 * index + 2


def _heapify(array: list[int], size: int, index: int) -> None:
    largest = index
    left = _left_child(index)
    right = _right_child(index)

    if left < size and array[left] > array[largest]:
        largest = left
    if right < size and array[right] > array[largest]:
        largest = right
    if largest != index:
        array[index], array[largest] = array[largest], array[index]
        _heapify(array, size, largest)


def _build_heap(array: list[int]) -> None:
    for i in reversed(range(len(array) // 2)):
        _heapify(array, len(array), i)


def heap_sort(array: list[int]) -> None:
    """
    Sorts an array of integers using the heap sort algorithm.

    Time complexity: O(n*log(n)), where n is the length of the array.
    Extra space complexity: O(1).

    Stable: No (the relative order of equal elements is not preserved).
    In-place: Yes (the input array is modified).

    :param array: array of integers
    :return: None
    """
    _build_heap(array)

    for index in reversed(range(len(array))):
        array[index], array[0] = array[0], array[index]
        _heapify(array, index, 0)


def insert_sort(array: list[int]) -> None:
    """
    Sorts an array of integers using the insertion sort algorithm.

    Time complexity: O(n^2), where n is the length of the array.
    Extra space complexity: O(1)

    Stable: Yes (the relative order of equal elements is preserved).
    In-place: Yes (the input array is modified).

    :param array: array of integers
    :return: None
    """
    for i in range(1, len(array)):
        current = array[i]
        j = i

        while j > 0 and array[j - 1] > current:
            array[j] = array[j - 1]
            j -= 1

        array[j] = current


def _merge(array_1: list[int], array_2: list[int]) -> list[int]:
    result = []

    i = j = 0
    while i < len(array_1) and j < len(array_2):
        if array_1[i] < array_2[j]:
            result.append(array_1[i])
            i += 1
        else:
            result.append(array_2[j])
            j += 1

    result.extend(array_1[i:])
    result.extend(array_2[j:])
    return result


def merge_sort(array: list[int]) -> list[int]:
    """
    Sorts an array of integers using the merge sort algorithm.

    Time complexity: O(n*log(n)), where n is the length of the array.
    Extra space complexity: O(n), where n is the length of the array.

    Stable: Yes (the relative order of equal elements is preserved).
    In-place: No (the input array is not modified).

    :param array: array of integers
    :return: sorted array of integers
    """
    length = len(array)
    if length <= 1:
        return array

    mid = length // 2
    left_array = array[:mid]
    right_array = array[mid:]

    left_array_sorted = merge_sort(left_array)
    right_array_sorted = merge_sort(right_array)

    return _merge(left_array_sorted, right_array_sorted)


def _partition(array: list[int], start: int, end: int) -> int:
    pivot = array[end]
    pivot_index = start - 1

    for i in range(start, end):
        if array[i] <= pivot:
            pivot_index += 1
            swap(array, pivot_index, i)

    swap(array, pivot_index + 1, end)
    return pivot_index + 1


def quick_sort(array: list[int], left: int, right: int) -> None:
    """
    Sorts an array of integers using the quick sort algorithm.

    Time complexity: O(n*log(n)), where n is the length of the array.
    Extra space complexity: O(1)

    Stable: No (the relative order of equal elements is not preserved).
    In-place: Yes (the input array is modified).

    :param array: array of integers
    :param left: left index (inclusive)
    :param right: right index (inclusive)
    :return: None
    """
    if left < right:
        middle = _partition(array, left, right)
        quick_sort(array, left, middle - 1)
        quick_sort(array, middle + 1, right)


def selection_sort(array: list[int]) -> None:
    """
    Sorts an array of integers using the selection sort algorithm.

    Time complexity: O(n^2), where n is the length of the array.
    Extra space complexity: O(1)

    Stable: No (the relative order of equal elements is not preserved).
    In-place: Yes (the input array is modified).

    :param array: array of integers
    :return: None
    """
    length = len(array)
    for i in range(length - 1):
        minimum = i
        for j in range(i + 1, length):
            if array[j] < array[minimum]:
                minimum = j

        swap(array, i, minimum)


def shell_sort(array: list[int]) -> None:
    """
    Sorts an array of integers using the shell sort algorithm.

    Time complexity: O(n^2), where n is the length of the array.
    Extra space complexity: O(1).

    Stable: No (the relative order of equal elements is not preserved).
    In-place: Yes (the input array is modified).

    :param array: array of integers
    :return: None
    """
    length = len(array)
    gap = length // 2

    while gap > 0:
        for i in range(gap, length):
            current = array[i]
            j = i

            while j >= gap and array[j - gap] > current:
                array[j] = array[j - gap]
                j -= gap

            array[j] = current

        gap //= 2


def pancake_sort(array: list[int]) -> None:
    """
    Sorts an array of integers using the pancake sort algorithm.

    Time complexity: O(n^2), where n is the length of the array.
    Extra space complexity: O(1).

    Stable: No (the relative order of equal elements is not preserved).
    In-place: Yes (the input array is modified).

    :param array: array of integers
    :return: None
    """
    length = len(array)
    for i in reversed(range(length)):
        maximum_index = max(range(i + 1), key=lambda x: array[x])

        if maximum_index != i:
            for j in range((maximum_index + 1) // 2):
                swap(array, j, maximum_index - j)

            for j in range((i + 1) // 2):
                swap(array, j, i - j)
