import unittest
import random
import string
from unittest.mock import patch
from os import remove
from kvstorage import Local_Strorage


class HashMock:
    def __init__(self, key):
        self.value = len(key) % 10

    def hexdigest(self):
        return str(self.value)


class BadHashMock:
    def __init__(self, key):
        pass

    def hexdigest(self):
        return str(1)


class Test_setup(unittest.TestCase):
    def setUp(self):
        self.storage = Local_Strorage('Test_storage.dat')

    def tearDown(self):
        self.storage.close()
        remove('Test_storage.dat')

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
        self.storage.remove_key('a')
        self.storage.remove_key('asd')
        self.assertEqual(self.storage._is_exists('a'), False)
        self.assertEqual(self.storage._get_key('a'), 'no such key')
        self.assertEqual(self.storage._is_exists('asd'), False)
        self.assertEqual(self.storage._get_key('asd'), 'no such key')
        self.assertEqual(self.storage._is_exists('b'), True)
        self.assertEqual(self.storage._get_key('b'), 'b')

        # open\close
        self.storage.close()
        self.storage = Local_Strorage('Test_storage.dat')
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
            self.storage.remove_key(key)

        for key, value in self.check.items():
            self.assertEqual(self.storage._get_key(key), 'no such key')
        for key, value in self.check2.items():
            self.assertEqual(self.storage._get_key(key), value)

    @patch('kvstorage.md5', new=HashMock)
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

    @patch('kvstorage.md5', new=HashMock)
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
            self.storage.remove_key(key)

        for key, value in self.check.items():
            self.assertEqual(self.storage._get_key(key), 'no such key')
        for key, value in self.check2.items():
            self.assertEqual(self.storage._get_key(key), value)

    @patch('kvstorage.md5', new=BadHashMock)
    def test_collisions_with_bad_hash_add_delete(self):
        self.check = {}
        self.check2 = {}
        amount_pairs = random.randint(200, 500)
        repeat_check = random.randint(2, 2)
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
            self.storage.remove_key(key)

        for key, value in self.check.items():
            self.assertEqual(self.storage._get_key(key), 'no such key')
        for key, value in self.check2.items():
            self.assertEqual(self.storage._get_key(key), value)

    def test_defragmentation(self):
        pass
        # add- all delete
        # add- all delete
        # check length
