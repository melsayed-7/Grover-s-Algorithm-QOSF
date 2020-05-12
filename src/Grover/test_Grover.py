import unittest
from search import *
from oracle import *


class TestSearch(unittest.TestCase):

    def test_search(self):
        result = search(1,1,oracle)
        self.assertEqual(max(result, key=int), '01011001')


if __name__ == '__main__':
    unittest.main()