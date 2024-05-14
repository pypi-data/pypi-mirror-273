def selection_sort(arr):
    """
    Implementation of selection sort algorithm
    :param arr: array to be sorted
    :return: sorted array
    """
    for i in range(len(arr)):
        min_idx = i
        for j in range(i, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
