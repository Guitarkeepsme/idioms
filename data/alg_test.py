sample = [-4, 3, 2, 10, -17]


def find_smallest(arr):
    smallest = arr[0]
    smallest_index = 0
    for i in range(1, len(arr)):
        if arr[i] < smallest:
            smallest_index = i
            smallest = arr[i]
    return smallest_index


print(find_smallest(sample))


def selection_sort(arr):
    new_arr = []
    for i in range(len(arr)):
        smallest = find_smallest(arr)
        new_arr.append(arr.pop(smallest))
    return new_arr


print(selection_sort(sample))


def fact(x):
    if x == 1:
        return 1
    else:
        return x * fact(x-1)


def summ(arr):
    count = 0
    for i in arr:
        count += i
    return count


def rec_sum(arr):
    if arr == []:
        return 0
    else:
        return 1 + rec_sum(arr[1:])


print(rec_sum([2, 4, 5, 4, 1]))
