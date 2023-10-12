import unittest

from values import Values as v

class ValueTestCases(unittest.TestCase):

    def setUp(self):
        self.data = v()
        
    def test_print(self):
        self.data.print_pst()
        self.assertEqual(3, 3)

    def test_matevalues(self):
        self.assertEqual(self.data.MATE_LOWER, 50710)
        self.assertEqual(self.data.MATE_UPPER, 69290)

if __name__ == '__main__':
    unittest.main()
