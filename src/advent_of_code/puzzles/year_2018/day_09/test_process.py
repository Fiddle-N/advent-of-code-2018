from advent_of_code.puzzles.year_2018.day_09 import process


def test_example_1():
    marble_game = process.MarbleGame(elves=9, last_marble=25)
    assert marble_game.play() == 32


def test_example_2():
    marble_game = process.MarbleGame.from_string('10 players; last marble is worth 1618 points')
    assert marble_game.play() == 8317


def test_example_3():
    marble_game = process.MarbleGame.from_string('13 players; last marble is worth 7999 points')
    assert marble_game.play() == 146373


def test_example_4():
    marble_game = process.MarbleGame.from_string('17 players; last marble is worth 1104 points')
    assert marble_game.play() == 2764


def test_example_5():
    marble_game = process.MarbleGame.from_string('21 players; last marble is worth 6111 points')
    assert marble_game.play() == 54718


def test_example_6():
    marble_game = process.MarbleGame.from_string('30 players; last marble is worth 5807 points')
    assert marble_game.play() == 37305
