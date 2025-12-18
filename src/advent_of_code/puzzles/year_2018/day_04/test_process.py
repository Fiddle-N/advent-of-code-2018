from datetime import datetime
import textwrap
import unittest
import io

from advent_of_code.puzzles.year_2018.day_04 import process


class TestProcessFile(unittest.TestCase):

    def test_read_file_ordered(self):
        f = io.StringIO(textwrap.dedent("""\
            [1518-11-01 00:00] Guard #10 begins shift
            [1518-11-01 00:05] falls asleep
            [1518-11-01 00:25] wakes up
            [1518-11-01 00:30] falls asleep
            [1518-11-01 00:55] wakes up
            [1518-11-01 23:58] Guard #99 begins shift
            [1518-11-02 00:40] falls asleep
            [1518-11-02 00:50] wakes up
            [1518-11-03 00:05] Guard #10 begins shift
            [1518-11-03 00:24] falls asleep
            [1518-11-03 00:29] wakes up
            [1518-11-04 00:02] Guard #99 begins shift
            [1518-11-04 00:36] falls asleep
            [1518-11-04 00:46] wakes up
            [1518-11-05 00:03] Guard #99 begins shift
            [1518-11-05 00:45] falls asleep
            [1518-11-05 00:55] wakes up
        """))
        
        act = process.process_file(f)
        
        exp = {
            datetime(1518, 11, 1,  0,  0): 'Guard #10 begins shift',
            datetime(1518, 11, 1,  0,  5): 'falls asleep',
            datetime(1518, 11, 1,  0, 25): 'wakes up',
            datetime(1518, 11, 1,  0, 30): 'falls asleep',
            datetime(1518, 11, 1,  0, 55): 'wakes up',
            datetime(1518, 11, 1, 23, 58): 'Guard #99 begins shift',
            datetime(1518, 11, 2,  0, 40): 'falls asleep',
            datetime(1518, 11, 2,  0, 50): 'wakes up',
            datetime(1518, 11, 3,  0,  5): 'Guard #10 begins shift',
            datetime(1518, 11, 3,  0, 24): 'falls asleep',
            datetime(1518, 11, 3,  0, 29): 'wakes up',
            datetime(1518, 11, 4,  0,  2): 'Guard #99 begins shift',
            datetime(1518, 11, 4,  0, 36): 'falls asleep',
            datetime(1518, 11, 4,  0, 46): 'wakes up',
            datetime(1518, 11, 5,  0,  3): 'Guard #99 begins shift',
            datetime(1518, 11, 5,  0, 45): 'falls asleep',
            datetime(1518, 11, 5,  0, 55): 'wakes up',
        }

        self.assertEqual(act, exp)
        
        
    def test_read_file_unordered(self):
        f = io.StringIO(textwrap.dedent("""\
            [1518-11-05 00:55] wakes up
            [1518-11-04 00:02] Guard #99 begins shift
            [1518-11-05 00:45] falls asleep
            [1518-11-03 00:24] falls asleep
            [1518-11-01 23:58] Guard #99 begins shift
            [1518-11-03 00:29] wakes up
            [1518-11-03 00:05] Guard #10 begins shift
            [1518-11-02 00:50] wakes up
            [1518-11-02 00:40] falls asleep
            [1518-11-01 00:55] wakes up
            [1518-11-01 00:30] falls asleep
            [1518-11-01 00:00] Guard #10 begins shift
            [1518-11-01 00:25] wakes up
            [1518-11-01 00:05] falls asleep
            [1518-11-05 00:03] Guard #99 begins shift
            [1518-11-04 00:36] falls asleep
            [1518-11-04 00:46] wakes up
        """))
        
        act = process.process_file(f)
        
        exp = {
            datetime(1518, 11, 1,  0,  0): 'Guard #10 begins shift',
            datetime(1518, 11, 1,  0,  5): 'falls asleep',
            datetime(1518, 11, 1,  0, 25): 'wakes up',
            datetime(1518, 11, 1,  0, 30): 'falls asleep',
            datetime(1518, 11, 1,  0, 55): 'wakes up',
            datetime(1518, 11, 1, 23, 58): 'Guard #99 begins shift',
            datetime(1518, 11, 2,  0, 40): 'falls asleep',
            datetime(1518, 11, 2,  0, 50): 'wakes up',
            datetime(1518, 11, 3,  0,  5): 'Guard #10 begins shift',
            datetime(1518, 11, 3,  0, 24): 'falls asleep',
            datetime(1518, 11, 3,  0, 29): 'wakes up',
            datetime(1518, 11, 4,  0,  2): 'Guard #99 begins shift',
            datetime(1518, 11, 4,  0, 36): 'falls asleep',
            datetime(1518, 11, 4,  0, 46): 'wakes up',
            datetime(1518, 11, 5,  0,  3): 'Guard #99 begins shift',
            datetime(1518, 11, 5,  0, 45): 'falls asleep',
            datetime(1518, 11, 5,  0, 55): 'wakes up',
        }

        self.assertEqual(act, exp)
        self.assertListEqual(list(act.keys()), list(exp.keys()))            # tests order of keys
        
        
class TestProcessLog(unittest.TestCase):
    
    def test_process_log(self):
        log = {
            datetime(1518, 11, 1,  0,  0): 'Guard #10 begins shift',
            datetime(1518, 11, 1,  0,  5): 'falls asleep',
            datetime(1518, 11, 1,  0, 25): 'wakes up',
            datetime(1518, 11, 1,  0, 30): 'falls asleep',
            datetime(1518, 11, 1,  0, 55): 'wakes up',
            datetime(1518, 11, 1, 23, 58): 'Guard #99 begins shift',
            datetime(1518, 11, 2,  0, 40): 'falls asleep',
            datetime(1518, 11, 2,  0, 50): 'wakes up',
            datetime(1518, 11, 3,  0,  5): 'Guard #10 begins shift',
            datetime(1518, 11, 3,  0, 24): 'falls asleep',
            datetime(1518, 11, 3,  0, 29): 'wakes up',
            datetime(1518, 11, 4,  0,  2): 'Guard #99 begins shift',
            datetime(1518, 11, 4,  0, 36): 'falls asleep',
            datetime(1518, 11, 4,  0, 46): 'wakes up',
            datetime(1518, 11, 5,  0,  3): 'Guard #99 begins shift',
            datetime(1518, 11, 5,  0, 45): 'falls asleep',
            datetime(1518, 11, 5,  0, 55): 'wakes up',
        }
        
        exp = {
            10: [set(range(5, 25)), set(range(30, 55)), set(range(24, 29))],
            99: [set(range(40, 50)), set(range(36, 46)), set(range(45, 55))],
        }
        
        act = process.process_log(log)
        
        self.assertEqual(act, exp)
        
    def test_process_log_deals_with_midnight_times_correctly(self):
        log = {
            datetime(1518, 11, 5, 23, 59): 'Guard #99 begins shift',
            datetime(1518, 11, 6,  0,  0): 'falls asleep',
            datetime(1518, 11, 6,  0, 55): 'wakes up',
        }
        
        exp = {99: [set(range(0, 55))]}
        
        act = process.process_log(log)
        
        self.assertEqual(act, exp)


class TestOthers(unittest.TestCase):
    def test_retrieve_minutes_asleep(self):
        inpt = {
            10: [set(range(5, 25)), set(range(30, 55)), set(range(24, 29))],
            99: [set(range(40, 50)), set(range(36, 46)), set(range(45, 55))],
        }
        
        exp = {
            10: 50,
            99: 30,
        }
        
        act = process.retrieve_minutes_asleep(inpt)
        self.assertEqual(act, exp)
        
    def test_retrieve_minute_sleep_count(self):
        inpt = [set(range(5, 25)), set(range(30, 55)), set(range(24, 29))]
        
        exp_counts = {
            5: 1, 
            6: 1, 
            7: 1,
            8: 1,
            9: 1,
            10: 1,
            11: 1,
            12: 1,
            13: 1,
            14: 1,
            15: 1, 
            16: 1, 
            17: 1, 
            18: 1, 
            19: 1, 
            20: 1, 
            21: 1, 
            22: 1, 
            23: 1, 
            24: 2,
            25: 1,
            26: 1,
            27: 1,
            28: 1,
            30: 1,
            31: 1,
            32: 1,
            33: 1,
            34: 1,
            35: 1,
            36: 1,
            37: 1,
            38: 1,
            39: 1,
            40: 1,
            41: 1,
            42: 1,
            43: 1,
            44: 1,
            45: 1,
            46: 1,
            47: 1,
            48: 1,
            49: 1,
            50: 1,
            51: 1,
            52: 1,
            53: 1,
            54: 1,
        }
        
        act_counts = process.retrieve_minute_sleep_count(inpt)
        
        self.assertEqual(act_counts, exp_counts)
        
    def test_retreive_guards_and_sleepiest_minutes(self):
        inpt = {
            10: [set(range(5, 25)), set(range(30, 55)), set(range(24, 29))],
            99: [set(range(40, 50)), set(range(36, 46)), set(range(45, 55))],
        }
        
        exp = {
            10: process.SleepyCombo(minute=24, count=2),
            99: process.SleepyCombo(minute=45, count=3),
        }
        
        act = process.retrieve_guards_and_sleepiest_minutes(inpt)
        
        self.assertEqual(act, exp)
        
    def test_key_for_max_value(self):
        inpt = {
            10: 50,
            99: 30,
        }
        
        sleepiest_guard = process.key_for_max_value(inpt)
        
        self.assertEqual(10, sleepiest_guard)
        
    def test_key_and_max_value(self):
        inpt = {
            10: 50,
            99: 30,
        }
        
        sleepiest_guard = process.key_and_max_value(inpt)
        
        self.assertEqual((10, 50), sleepiest_guard)
        
    def test_key_for_max_value_at_end_of_nested_tuple(self):
        inpt = {
            10: process.SleepyCombo(minute=24, count=2),
            99: process.SleepyCombo(minute=45, count=3),
        }
        
        act = process.key_for_max_value_at_end_of_nested_tuple(inpt)
        
        self.assertEqual(
            (99, process.SleepyCombo(minute=45, count=3)), 
            act)


if __name__ == '__main__':
    unittest.main()
