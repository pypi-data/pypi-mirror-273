def insertion_sort(arr):
    """
    Implementation of insertion sort algorithm
    :param arr: Array to be sorted
    :return: Sorted array
    """
    for i in range(1, len(arr)):
        for j in range(i, 0, -1):
            if arr[j] > arr[j-1]:
                break
            else:
                arr[j-1], arr[j] = arr[j], arr[j-1]
    return arr
