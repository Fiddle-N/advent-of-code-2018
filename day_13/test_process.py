from day_13 import process


def test_one_pair_of_cart():
    track_list = [
        r'/->-\        ',
        r'|   |  /----' '\\',
        r'| /-+--+-\  |',
        r'| | |  | v  |',
        r'\-+-/  \-+--/',
        r'  \------/   ',
    ]
    track = '\n'.join(track_list)
    mine_cart_madness_iter = iter(process.MineCartMadness(track))
    crash = next(mine_cart_madness_iter)
    assert crash == process.Coords(x=7, y=3)


def test_multiple_pairs_of_carts():
    track_list = [
        r'/>-<\  ',
        r'|   |  ',
        r'| /<+-' '\\',
        r'| | | v',
        r'\>+</ |',
        r'  |   ^',
        r'  \<->/',
    ]
    track = '\n'.join(track_list)
    mine_cart_madness_iter = iter(process.MineCartMadness(track))
    while True:
        try:
            next(mine_cart_madness_iter)
        except StopIteration as e:
            last_cart = e.value
            break
    assert last_cart == process.Coords(x=6, y=4)
