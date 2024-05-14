def merge_sort(arr):
    """
    Implementation of merge sort algorithm
    :param arr: Array to be sorted
    :return: Sorted array
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    """
    Merges two arrays(that are sorted) together in ascending order
    :param left: Left sorted array to be merged
    :param right: Right sorted array to be merged
    :return:
    """
    left_index = 0
    right_index = 0
    result = []
    while len(left) > left_index and len(right) > right_index:
        if left[left_index] < right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1
    while len(left) > left_index:
        result.append(left[left_index])
        left_index += 1
    while len(right) > right_index:
        result.append(right[right_index])
        right_index += 1
    return result
