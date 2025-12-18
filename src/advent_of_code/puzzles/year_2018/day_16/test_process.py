from src.advent_of_code.puzzles.year_2018.day_16 import process


def test_example():
    dvm = process.DeviceVM(
        [process.Sample([3, 2, 1, 1], process.Instructions(*[9, 2, 1, 2]), [3, 2, 2, 1])],
    )

    assert dvm.calculate_opcodes(skip_opcode_resolution=True) == 1
