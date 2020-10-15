import unittest
from os import path, remove
from main import KVStorage, open_storage


class Test_setup(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        KVStorage('test', 'init')

    @classmethod
    def tearDownClass(self):
        remove('test.json')

    def test_add(self):
        KVStorage('test', 'add', '123', 'abc')
        self.assertEqual(open_storage('test'), {'123': 'abc'})

    def test_delete(self):
        KVStorage('test', 'delete', '123', 'abc')
        self.assertEqual(open_storage('test'), {})
