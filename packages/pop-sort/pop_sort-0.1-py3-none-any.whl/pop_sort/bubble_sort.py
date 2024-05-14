def bubble_sort(arr):
    """
    Implementation of bubble sort algorithm
    :param arr: array to be sorted
    :return: sorted array
    """
    for i in range(len(arr)):
        for j in range(1, len(arr) - i):
            if arr[j - 1] > arr[j]:
                arr[j-1], arr[j] = arr[j], arr[j - 1]
    return arr
