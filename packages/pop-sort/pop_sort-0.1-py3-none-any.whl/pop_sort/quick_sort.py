def quick_sort(arr):
    """
    Implementation of quick sort algorithm.
    :param arr: Array to be sorted.
    :return: Sorted array.
    """
    if len(arr) <= 1:
        return arr
    pivot, left, right = partition(arr)
    return quick_sort(left) + [pivot] + quick_sort(right)


def partition(arr):
    """
    Partitions array into two arrays according to pivot(last member of array).
    Left side smaller than pivot, right - larger.
    :param arr: Array to be partitioned
    :return: Pivot - number accroding to which array is partitioned, left - smaller numbers than pivot, right - larger numbers than pivot
    """
    pivot = arr[len(arr) - 1]
    pivot_index = 0
    for i in range(len(arr) - 1):
        if pivot >= arr[i]:
            arr[pivot_index], arr[i] = arr[i], arr[pivot_index]
            pivot_index += 1
    arr[pivot_index], arr[-1] = arr[-1], arr[pivot_index]
    return pivot, arr[:pivot_index], arr[pivot_index + 1:]
