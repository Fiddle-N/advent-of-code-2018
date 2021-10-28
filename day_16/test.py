from day_16 import process


def test_example():
    chronal_classification = process.ChronalClassification(
        [process.Sample([3, 2, 1, 1], process.Instructions(*[9, 2, 1, 2]),[3, 2, 2, 1])],
    )

    assert chronal_classification.calculate_opcodes(skip_opcode_resolution=True) == 1
