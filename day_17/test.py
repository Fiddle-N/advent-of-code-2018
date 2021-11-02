import pytest

from day_17 import process


class TestMapGeneration:

    def test_map_gen(self):
        input_ = """\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""
        rr = process.ReservoirResearch(input_)
        exp_map = """\
..............
............#.
.#..#.......#.
.#..#..#......
.#..#..#......
.#.....#......
.#.....#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######..."""
        act_map = rr.map()
        assert act_map == exp_map


class TestSimulateFlow:

    def test_simulate_flow_one_column_well_of_clay(self):
        input_ = """\
y=7, x=499..501
x=499, y=3..7
x=501, y=2..7"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
..|..
|||#.
|#~#.
|#~#.
|#~#.
|#~#.
|###."""
        act_map = rr.map()
        assert act_map == exp_map

    def test_simulate_flow_one_column_well_of_clay_with_no_corner_clay(self):
        input_ = """\
y=7, x=500..500
x=499, y=3..6
x=501, y=2..6"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
..|..
|||#.
|#~#.
|#~#.
|#~#.
|#~#.
|.#.."""
        act_map = rr.map()
        assert act_map == exp_map

    def test_simulate_flow_one_row_well_of_clay_contains_settled_water(self):
        input_ = """\
y=7, x=498..502
x=498, y=6..7
x=502, y=6..7"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
|||||||
|#~~~#|
|#####|"""
        act_map = rr.map()
        assert act_map == exp_map

    def test_simulate_flow_one_row_well_of_clay_with_missing_bottom_left_clay_contains_non_settled_water(self):
        input_ = """\
y=7, x=500..502
x=498, y=6..7
x=502, y=6..7"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
...|...
.#|||#.
.#|###."""
        act_map = rr.map()
        assert act_map == exp_map

    def test_simulate_flow_one_row_well_of_clay_with_missing_bottom_right_clay_contains_non_settled_water(self):
        input_ = """\
y=7, x=498..500
x=498, y=6..7
x=502, y=6..7"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
...|...
.#|||#.
.###|#."""
        act_map = rr.map()
        assert act_map == exp_map

    def test_simulate_flow_one_row_well_of_clay_with_missing_bottom_left_and_right_clay_contains_non_settled_water(self):
        input_ = """\
y=7, x=500..500
x=498, y=6..7
x=502, y=6..7"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
...|...
.#|||#.
.#|#|#."""
        act_map = rr.map()
        assert act_map == exp_map

    def test_simulate_flow_one_row_well_of_clay_with_missing_left_clay_contains_non_settled_water(self):
        input_ = """\
y=7, x=498..502
x=502, y=6..7"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
...|...
|||||#.
|#####."""
        act_map = rr.map()
        assert act_map == exp_map

    def test_simulate_flow_one_row_well_of_clay_with_missing_right_clay_contains_non_settled_water(self):
        input_ = """\
y=7, x=498..502
x=498, y=6..7"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
...|...
.#|||||
.#####|"""
        act_map = rr.map()
        assert act_map == exp_map

    def test_simulate_flow_one_row_well_of_clay_with_missing_both_side_clay_contains_non_settled_water(self):
        input_ = """\
y=7, x=498..502"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
|||||||
|#####|"""
        act_map = rr.map()
        assert act_map == exp_map


    def test_simulate_flow_two_row_well_of_clay_contains_settled_water(self):
        input_ = """\
y=7, x=498..502
x=498, y=5..7
x=502, y=5..7"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
|||||||
|#~~~#|
|#~~~#|
|#####|"""
        act_map = rr.map()
        assert act_map == exp_map

    def test_simulate_flow_one_well_overflowing_on_both_ends_into_another_well(self):
        input_ = """\
y=7, x=498..502
x=498, y=5..7
x=502, y=5..7
y=10, x=494..506
x=494, y=9..10
x=506, y=9..10"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
....|||||||....
....|#~~~#|....
....|#~~~#|....
....|#####|....
|||||||||||||||
|#~~~~~~~~~~~#|
|#############|"""
        act_map = rr.map()
        assert act_map == exp_map

    def test_simulate_flow_full(self):
        input_ = """\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
......|.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
...|||||||||..
...|#~~~~~#|..
...|#~~~~~#|..
...|#~~~~~#|..
...|#######|.."""
        act_map = rr.map()
        assert act_map == exp_map
        assert rr.count_water() == 57
        assert rr.count_settled_water() == 29

    def test_simulate_flow_full_counting_water_beyond_clay_at_x_boundaries(self):
        input_ = """\
y=7, x=498..501
x=501, y=3..7
x=498, y=2..7
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""
        rr = process.ReservoirResearch(input_)
        rr.simulate_flow()
        exp_map = """\
...|.......
...|.....#.
.#||||...#.
.#~~#|.....
.#~~#|.....
.#~~#|.....
.#~~#|.....
.####|.....
.....|.....
|||||||||..
|#~~~~~#|..
|#~~~~~#|..
|#~~~~~#|..
|#######|.."""
        act_map = rr.map()
        assert act_map == exp_map
        assert rr.count_water() == 51