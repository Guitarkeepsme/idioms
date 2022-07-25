# этот файл не имеет никакого отношения к боту. Он нужен как практика изучения алгоритмов

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


def my_sum(li):
    if li == []:
        return 0
    return li[0] + my_sum(li[1:])


def count(li):
    if li == []:
        return 0
    return 1 + count(li[1:])


def max_index(li):
    if len(li) == 2:
        return li[0] if li[0] > li[1] else li[1]
    return


print(my_sum([2, 4, 5, 4, 1]))
print(count([1, 2, 3]))


