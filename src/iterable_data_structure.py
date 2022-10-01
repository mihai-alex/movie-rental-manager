# TODO: ask how to make the iterator work on nested for loops
class MyIterator:
    def __init__(self, data=None):
        self._index = 0
        if data is None:
            self._data = []
        else:
            self._data = [data]

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __delitem__(self, index):
        del self._data[index]

    def __next__(self):
        if self._index >= len(self._data):
            self._index = 0
            raise StopIteration

        current = self._data[self._index]
        self._index = self._index + 1
        return current

    def __iter__(self):
        self._index = 0
        return self

    def __str__(self):
        return '[' + ', '.join(str(item) for item in self._data) + ']'

    def remove(self, item):
        self._data.remove(item)

    def append(self, item):
        self._data.append(item)

    def pop(self):
        return self._data.pop()

    def clear(self):
        self._data.clear()


def my_sort(collection, comparison):
    """
    Gnome Sort implementation.
    The comparison function must work with "<=" or ">=". If it does not include the '=' sign: infinite loop.
    """
    index = 0
    while index < len(collection):
        if index == 0 or comparison(collection[index - 1], collection[index]):
            index = index + 1
        else:
            collection[index - 1], collection[index] = collection[index], collection[index - 1]
            index = index - 1


def my_filter(collection, acceptance):
    return [item for item in collection if acceptance(item)]

# TODO: fix nested loop iterator
# li = MyIterator()
# for i in range(4):
#     li.append(i)
#
# for i in li:
#     for j in li:
#         print(f'{i} and {j}\n')
