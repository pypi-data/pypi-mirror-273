from pop_sort.insertion_sort import insertion_sort


def bucket_sort(input_list, num_of_buckets=None):
    max_value = max(input_list)
    size = max_value // num_of_buckets + 1 if num_of_buckets else max_value / len(input_list) + 1
    num_of_buckets = num_of_buckets if num_of_buckets else len(input_list)
    buckets_list = [[] for _ in range(num_of_buckets)]
    for i in range(len(input_list)):
        j = int(input_list[i] // size)
        if j != num_of_buckets:
            buckets_list[j].append(input_list[i])
        else:
            buckets_list[num_of_buckets - 1].append(input_list[i])
    for z in range(len(buckets_list)):
        insertion_sort(buckets_list[z])
    final_output = [num for bucket in buckets_list for num in bucket]
    return final_output
