import unittest
import os.path as path
from main import KVStorage


class Test_setup(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.storage = KVStorage('init', 'test')
        self.storage.run()

    def test_create(self):
        self.storage.add([0, 'first', 'second'])
        self.storage.save([])
        self.assertEqual(self.storage.data, {'first': 'second'})
        self.assertEqual(path.isfile('test.json'), True)

    def test_error(self):
        self.storage.delete([0, 'first'])
        result = self.storage.delete([0, 'second'])
        result2 = self.storage.load([0, 'first'])
        self.assertEqual(self.storage.data, {})
        self.assertEqual(result2, 'No such key')
        self.assertEqual(result, 'No such key')
