import unittest

from position import Position
from const import initial

class PositionTestCases(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_initpos(self):
        pos = [Position(initial, 0, (True,True), (True,True), 0, 0)]
        self.assertEqual(pos.fen(), "3")

if __name__ == '__main__':
    unittest.main()
