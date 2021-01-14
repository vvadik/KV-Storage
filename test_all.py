import unittest
import random
import string
from unittest.mock import patch
from os import remove, path
from localstorage import LocalStrorage


class HashMock:
    def __init__(self, key):
        self.value = len(key) % 10

    def hexdigest(self):
        return str(self.value)


class Test_setup(unittest.TestCase):
    def setUp(self):
        self.storage = LocalStrorage('.Test_storage.dat')

    def tearDown(self):
        self.storage.close()
        remove('.Test_storage.dat')

    def test_basic_things(self):
        # add
        self.storage.add_key(('a', 'a'))
        self.storage.add_key(('asd', 'asd'))
        self.storage.add_key(('b', 'b'))
        self.storage.add_key(('a', 'b'))
        self.assertEqual(self.storage._get_key('a'), 'b')
        self.assertEqual(self.storage._get_key('b'), 'b')
        self.assertEqual(self.storage._get_key('asd'), 'asd')
        self.assertEqual(self.storage._get_key('d'), 'no such key')

        # delete
        self.storage._remove_key('a')
        self.storage._remove_key('asd')
        self.assertEqual(self.storage._is_exists('a'), False)
        self.assertEqual(self.storage._get_key('a'), 'no such key')
        self.assertEqual(self.storage._is_exists('asd'), False)
        self.assertEqual(self.storage._get_key('asd'), 'no such key')
        self.assertEqual(self.storage._is_exists('b'), True)
        self.assertEqual(self.storage._get_key('b'), 'b')

        # open\close
        self.storage.close()
        self.storage = LocalStrorage('.Test_storage.dat')
        self.assertEqual(len(self.storage.storage), 1)
        self.assertEqual(len(self.storage.deleted_sectors), 3)

    def test_random_add(self):
        self.check = {}
        amount_pairs = random.randint(5000, 10000)
        repeat_check = random.randint(100, 200)
        for pair in range(amount_pairs):
            key = ''.join(random.choice(string.ascii_letters)
                          for _ in range(random.randint(10, 100)))
            value = ''.join(random.choice(string.ascii_letters)
                            for _ in range(random.randint(10, 100)))
            if pair % repeat_check == 0:
                self.check[key] = value
            self.storage.add_key((key, value))
        for key, value in self.check.items():
            self.assertEqual(self.storage._get_key(key), value)

    def test_random_delete(self):
        self.check = {}
        self.check2 = {}
        amount_pairs = random.randint(2000, 5000)
        repeat_check = random.randint(100, 200)
        for pair in range(amount_pairs):
            key = ''.join(random.choice(string.ascii_letters)
                          for _ in range(random.randint(10, 100)))
            value = ''.join(random.choice(string.ascii_letters)
                            for _ in range(random.randint(10, 100)))
            if pair % repeat_check == 0:
                self.check[key] = value
            else:
                self.check2[key] = value
            self.storage.add_key((key, value))
        for key, value in self.check.items():
            self.storage._remove_key(key)

        for key, value in self.check.items():
            self.assertEqual(self.storage._get_key(key), 'no such key')
        for key, value in self.check2.items():
            self.assertEqual(self.storage._get_key(key), value)

    @patch('localstorage.md5', new=HashMock)
    def test_collisions_random_add(self):
        self.check = {}
        amount_pairs = random.randint(2000, 5000)
        repeat_check = random.randint(100, 200)
        for pair in range(amount_pairs):
            key = ''.join(random.choice(string.ascii_letters)
                          for _ in range(random.randint(10, 20)))
            value = ''.join(random.choice(string.ascii_letters)
                            for _ in range(random.randint(10, 20)))
            if pair % repeat_check == 0:
                self.check[key] = value
            self.storage.add_key((key, value))
        for key, value in self.check.items():
            self.assertEqual(self.storage._get_key(key), value)

    @patch('localstorage.md5', new=HashMock)
    def test_collisions_random_delete(self):
        self.check = {}
        self.check2 = {}
        amount_pairs = random.randint(2000, 5000)
        repeat_check = random.randint(100, 200)
        for pair in range(amount_pairs):
            key = ''.join(random.choice(string.ascii_letters)
                          for _ in range(random.randint(10, 20)))
            value = ''.join(random.choice(string.ascii_letters)
                            for _ in range(random.randint(10, 20)))
            if pair % repeat_check == 0:
                self.check[key] = value
            else:
                self.check2[key] = value
            self.storage.add_key((key, value))
        for key, value in self.check.items():
            self.storage._remove_key(key)

        for key, value in self.check.items():
            self.assertEqual(self.storage._get_key(key), 'no such key')
        for key, value in self.check2.items():
            self.assertEqual(self.storage._get_key(key), value)

    def test_defragmentation(self):
        # Пишем 78Мб, удаляем и ожидаем увидеть не более 3Мб
        self.check = {}
        amount_pairs = 200  # 1024
        length = 2000  # 100
        for i in range(100):  # i = (length * amount_pairs / 2^20)Mb
            all_keys = []
            for pair in range(amount_pairs):
                key = ''.join(random.choice(string.ascii_letters)
                              for _ in range(length))
                value = ''.join(random.choice(string.ascii_letters)
                                for _ in range(length))
                self.storage.add_key((key, value))
                all_keys.append(key)
            for key in all_keys:
                self.storage._remove_key(key)

        for pair in range(amount_pairs):
            key = ''.join(random.choice(string.ascii_letters)
                          for _ in range(length))
            value = ''.join(random.choice(string.ascii_letters)
                            for _ in range(length))
            self.storage.add_key((key, value))
            self.check[key] = value

        self.storage.defragmentation()

        for key, value in self.check.items():
            self.assertEqual(self.storage._get_key(key), value)
        self.assertEqual(path.getsize(self.storage.file_name) < 1024*1024*3,
                         True)
