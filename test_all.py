import unittest
import random
import string
from os import remove
from kvstorage import Local_Strorage


class Test_setup(unittest.TestCase):
    # @classmethod
    # def setUpClass(self):
    #     pass

    @classmethod
    def tearDownClass(self):
        remove('Test_storage.dat')

    def setUp(self):
        self.storage = Local_Strorage('Test_storage.dat')

    def tearDown(self):
        self.storage.close()

    def test_basic1_add(self):
        self.storage.add_key(('a', 'a'))
        self.storage.add_key(('asd', 'asd'))
        self.storage.add_key(('b', 'b'))
        self.storage.add_key(('a', 'b'))
        self.assertEqual(self.storage._get_key('a'), 'b')
        self.assertEqual(self.storage._get_key('b'), 'b')
        self.assertEqual(self.storage._get_key('asd'), 'asd')
        self.assertEqual(self.storage._get_key('d'), 'no such key')

    def test_basic2_delete(self):
        self.storage.remove_key('a')
        self.storage.remove_key('asd')
        self.assertEqual(self.storage._is_exists('a'), False)
        self.assertEqual(self.storage._get_key('a'), 'no such key')
        self.assertEqual(self.storage._is_exists('asd'), False)
        self.assertEqual(self.storage._get_key('asd'), 'no such key')
        self.assertEqual(self.storage._is_exists('b'), True)
        self.assertEqual(self.storage._get_key('b'), 'b')

    def test_basic3_close_open(self):
        self.assertEqual(len(self.storage.storage), 1)
        self.assertEqual(len(self.storage.deleted_sectors), 3)

    def test_random_add(self):
        self.storage.close()
        remove('Test_storage.dat')
        self.storage = Local_Strorage('Test_storage.dat')

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
