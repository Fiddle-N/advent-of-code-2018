import collections
import operator
from datetime import datetime
import re

SleepyCombo = collections.namedtuple('SleepyCombo', 'minute count')


def process_file(f):
    log = {}
    for line in f:
        line = line.rstrip()
        _, raw_dt, raw_action = re.split('\[|] ', line)     # splits on [, or on ] with a space followed
        dt = datetime.strptime(raw_dt, '%Y-%m-%d %H:%M')
        if dt in log:
            raise Exception('this timestamp has already been seen')
        log[dt] = raw_action
    return {k: v for k,v in sorted(log.items(), key=operator.itemgetter(0))}
    
    
def process_log(log):
    guard_log = collections.defaultdict(list)
    
    current_id = None
    start_min = None
    end_min = None
    for idx, (dt, raw_log) in enumerate(log.items()):
        if raw_log.startswith('Guard'):
            # new day new guard
            m = re.search('Guard #(\d+) begins shift', raw_log)
            id = m.group(1)
            current_id = int(id)
        elif raw_log == 'falls asleep':
            start_min = dt.minute
        elif raw_log == 'wakes up':
            end_min = dt.minute
        else:
            raise Exception('should not get here')
        if start_min is not None and end_min is not None:
            guard_log[current_id].append(set(range(start_min, end_min)))
            start_min = None
            end_min = None
    
    return dict(guard_log)


def retrieve_minutes_asleep(guard_log):
    minutes_asleep = {}
    for id, asleep_ranges in guard_log.items():
        minutes_asleep_for_guard = sum(
            len(asleep_range) 
            for asleep_range in asleep_ranges
        )
        minutes_asleep[id] = minutes_asleep_for_guard
    return minutes_asleep
    

def retrieve_minute_sleep_count(ranges):
    minute_sleep_count = collections.defaultdict(int)
    for range in ranges:
        for minute in range:
            minute_sleep_count[minute] += 1
    return minute_sleep_count


def key_for_max_value(d):
    return max(d.items(), key=operator.itemgetter(1))[0]
    
    
def key_and_max_value(d):
    max_combo = max(d.items(), key=operator.itemgetter(1))
    return max_combo[0], max_combo[1]
    
    
def key_for_max_value_at_end_of_nested_tuple(d):
    tpl = max(d.items(), key=lambda x: x[1][1])
    return tpl[0], tpl[1]
    
    
def retrieve_guards_and_sleepiest_minutes(log):
    guards_and_sleepiest_minutes = {}
    for id, ranges in log.items():
        minute_sleep_count = retrieve_minute_sleep_count(ranges)
        sleepiest_min_count = key_and_max_value(minute_sleep_count)
        sleepiest_min_count = SleepyCombo(*sleepiest_min_count)
        guards_and_sleepiest_minutes[id] = sleepiest_min_count
    return guards_and_sleepiest_minutes

def main():
    with open('input.txt', 'r') as f:
        raw_log = process_file(f)
        
    log = process_log(raw_log)

    minutes_asleep = retrieve_minutes_asleep(log)
    sleepiest_guard = key_for_max_value(minutes_asleep)
    print(f'sleepiest_guard {sleepiest_guard}')
    
    sleepiest_ranges = log[sleepiest_guard]
    minute_sleep_count = retrieve_minute_sleep_count(sleepiest_ranges)
    sleepiest_minute = key_for_max_value(minute_sleep_count)
    print(f'sleepiest_minute {sleepiest_minute}')
    
    print(f'answer_1 {sleepiest_guard * sleepiest_minute}')
    
    sleepiest_minute_log = retrieve_guards_and_sleepiest_minutes(log)
    sleepiest_minute_guard, combo = key_for_max_value_at_end_of_nested_tuple(sleepiest_minute_log)
    print(f'sleepiest_minute_guard {sleepiest_minute_guard}')
    print(f'sleepiest_minute_guard_minute {combo.minute}')
    print(f'answer_2 {sleepiest_minute_guard * combo.minute}')


if __name__ == '__main__':
    main()
