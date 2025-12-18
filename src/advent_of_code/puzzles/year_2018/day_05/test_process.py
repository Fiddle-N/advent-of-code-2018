import unittest

from advent_of_code.puzzles.year_2018.day_05 import process

class TestProcessPolymer(unittest.TestCase):

    def test_process_polymer(self):
        inpt = 'dabAcCaCBAcCcaDA'
        exp = 'dabCBAcaDA'
        act = process.process_polymer(inpt)
        self.assertEqual(act, exp)
    
if __name__ == '__main__':
    unittest.main()