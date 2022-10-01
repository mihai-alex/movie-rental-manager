import unittest

from iterable_data_structure import MyIterator, my_sort, my_filter


class TestIterableDataStructure(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_iterator(self):
        my_list = MyIterator()
        self.assertEqual(len(my_list), 0)
        my_list.append(1)
        my_list.append(2)
        my_list.append(3)
        my_list.append(1)
        my_list.append(1)
        my_list.remove(1)

        for item in my_list:
            self.assertIsInstance(my_list[item], int)

        self.assertEqual(len(my_list), 4)
        my_list.clear()
        self.assertEqual(len(my_list), 0)

        my_list2 = MyIterator(15)
        self.assertEqual(my_list2[0], 15)
        self.assertEqual(len(my_list2), 1)
        my_list2.append(22)
        self.assertEqual(my_list2[1], 22)
        self.assertEqual(len(my_list2), 2)
        my_list2[0] = 99
        self.assertEqual(my_list2[0], 99)

        del my_list2[0]
        self.assertEqual(len(my_list2), 1)

        self.assertIsInstance(str(my_list2), str)
        item = my_list2.pop()
        self.assertEqual(item, 22)

    def test_my_sort(self):
        my_list = MyIterator()
        my_list.append(1)
        my_list.append(3)
        my_list.append(2)
        my_list.append(1)
        my_list.append(1)
        my_list.append(4)

        my_sort(my_list, lambda x, y: x <= y)
        self.assertEqual(str(my_list), '[1, 1, 1, 2, 3, 4]')

        my_sort(my_list, lambda x, y: x >= y)
        self.assertEqual(str(my_list), '[4, 3, 2, 1, 1, 1]')

    def test_my_filter(self):
        my_list = MyIterator()
        my_list.append(1)
        my_list.append(3)
        my_list.append(2)
        my_list.append(1)
        my_list.append(1)
        my_list.append(4)

        new_list = my_filter(my_list, lambda x: x > 2)
        self.assertEqual(len(new_list), 2)
        for item in new_list:
            self.assertGreater(item, 2)
