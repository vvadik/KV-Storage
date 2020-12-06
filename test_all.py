import unittest
from os import remove
from kvstorage import Local_Strorage


class Test_setup(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.storage = Local_Strorage('Test_storage.dat')

    @classmethod
    def tearDownClass(self):
        self.storage.close()
        remove('Test_storage.dat')

    def test_basic_add(self):
        self.storage.add_key(('a', 'a'))
        self.storage.add_key(('asd', 'asd'))
        self.storage.add_key(('b', 'b'))
        self.storage.add_key(('a', 'b'))
        self.assertEqual(self.storage._get_key('a'), 'b')
        self.assertEqual(self.storage._get_key('b'), 'b')
        self.assertEqual(self.storage._get_key('asd'), 'asd')
        self.assertEqual(self.storage._get_key('d'), 'no such key')

    def test_basic_delete(self):
        self.storage.remove_key('a')
        self.storage.remove_key('asd')
        self.assertEqual(self.storage._is_exists('a'), False)
        self.assertEqual(self.storage._get_key('a'), 'no such key')
        self.assertEqual(self.storage._is_exists('asd'), False)
        self.assertEqual(self.storage._get_key('asd'), 'no such key')
        self.assertEqual(self.storage._is_exists('b'), True)
        self.assertEqual(self.storage._get_key('b'), 'b')
