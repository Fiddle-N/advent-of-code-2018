from day_08 import process


def test_example():
    raw_text = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    tree_parser = process.TreeParser(raw_text)
    tree = tree_parser.parse()
    assert tree.metadata_sum == 138
    assert tree.value == 66
