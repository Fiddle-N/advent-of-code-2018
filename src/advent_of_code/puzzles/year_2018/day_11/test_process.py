from advent_of_code.puzzles.year_2018.day_11 import process


def test_example_1():
    assert process.FuelCells.calculate_power_level(serial_no=8, x=3, y=5) == 4


def test_example_2():
    assert process.FuelCells.calculate_power_level(serial_no=57, x=122, y=79) == -5


def test_example_3():
    assert process.FuelCells.calculate_power_level(serial_no=39, x=217, y=196) == 0


def test_example_4():
    assert process.FuelCells.calculate_power_level(serial_no=71, x=101, y=153) == 4


def test_example_5():
    chronal_charge = process.ChronalCharge(serial_no=18)
    assert chronal_charge.largest_power_3_by_3() == (33, 45)


def test_example_5_2():
    chronal_charge = process.ChronalCharge(serial_no=18)
    result = chronal_charge.largest_power(3)
    assert (result.top_left_x, result.top_left_y) == (33, 45)


def test_example_6():
    chronal_charge = process.ChronalCharge(serial_no=42)
    assert chronal_charge.largest_power_3_by_3() == (21, 61)


def test_example_6_2():
    chronal_charge = process.ChronalCharge(serial_no=42)
    result = chronal_charge.largest_power(3)
    assert (result.top_left_x, result.top_left_y) == (21, 61)


def test_example_7():
    chronal_charge = process.ChronalCharge(serial_no=18)
    result = chronal_charge.largest_power_all_k()
    assert (result.top_left_x, result.top_left_y, result.size) == (90, 269, 16)


def test_example_8():
    chronal_charge = process.ChronalCharge(serial_no=42)
    result = chronal_charge.largest_power_all_k()
    assert (result.top_left_x, result.top_left_y, result.size) == (232, 251, 12)
