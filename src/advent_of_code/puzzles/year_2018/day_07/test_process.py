from src.advent_of_code.puzzles.year_2018.day_07 import process


def test_example_1_worker():
    text_input = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""
    i = process.Instructions(text_input)
    step_order, _ = i.determine_order(worker_no=1, offset=0)
    assert step_order == 'CABDFE'


def test_example_2_workers():
    text_input = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""
    i = process.Instructions(text_input)
    assert i.determine_order(worker_no=2, offset=0) == ('CABFDE', 15)