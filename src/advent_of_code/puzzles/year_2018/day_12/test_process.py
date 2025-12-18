from src.advent_of_code.puzzles.year_2018.day_12 import process


def test():
    input_ = """\
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""
    subterranean_sustainability = process.SubterraneanSustainability(input_, is_full_input=False)
    plant_gen = iter(subterranean_sustainability)
    plants = None
    for _ in range(20):
        plants = next(plant_gen)
    exp_plants = {
        -2: '#',
        -1: '.',
        0: '.',
        1: '.',
        2: '.',
        3: '#',
        4: '#',
        5: '.',
        6: '.',
        7: '.',
        8: '.',
        9: '#',
        10: '#',
        11: '#',
        12: '#',
        13: '#',
        14: '.',
        15: '.',
        16: '.',
        17: '#',
        18: '#',
        19: '#',
        20: '#',
        21: '#',
        22: '#',
        23: '#',
        24: '.',
        25: '.',
        26: '.',
        27: '.',
        28: '#',
        29: '.',
        30: '#',
        31: '.',
        32: '.',
        33: '#',
        34: '#',
    }
    assert plants.gen == exp_plants
    assert plants.total == 325

