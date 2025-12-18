import pytest
from advent_of_code.puzzles.year_2018.day_06 import process


def test_example():
    c = src.advent_of_code.puzzles.year_2018.day_06.process.ChronalCoods()
    c.coords = [
        [1, 1],
        [1, 6],
        [8, 3],
        [3, 4],
        [5, 5],
        [8, 9],
    ]
    c.get_min_max()
    c.calculate_nearest_coords()
    assert c.retrieve_largest_finite_area() == 17
    assert c.calculate_region_size_close_to_all_coords(32) == 16

pytest.main()