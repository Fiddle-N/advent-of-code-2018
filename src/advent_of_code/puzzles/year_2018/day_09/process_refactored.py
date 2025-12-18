import collections
import dataclasses
import itertools
import re
import timeit
import typing


@dataclasses.dataclass
class Marble:
    previous: int
    next: int


@dataclasses.dataclass
class Elf:
    number: int
    score: int = 0


class MarbleGame:

    def __init__(self, elves, last_marble):
        self.circle = collections.deque()
        self.elves = [Elf(elf_no) for elf_no in range(elves)]
        self.last_marble = last_marble

    @classmethod
    def from_string(cls, string, marble_multiplier=1):
        if match := re.fullmatch(r'(\d+) players; last marble is worth (\d+) points', string):
            return cls(int(match.group(1)), int(match.group(2)) * marble_multiplier)
        else:
            raise Exception

    @classmethod
    def read_file(cls, marble_multiplier=1):
        with open('input.txt') as f:
            return cls.from_string(f.read().rstrip(), marble_multiplier)

    def play(self):
        for marble, elf in enumerate(itertools.cycle(self.elves)):
            if marble and (marble % 23 == 0):
                self.circle.rotate(7)
                elf.score += (self.circle.pop() + marble)
                self.circle.rotate(-1)
            else:
                self.circle.rotate(-1)
                self.circle.append(marble)
            if marble == self.last_marble:
                return max(self.elves, key=lambda elf_: elf_.score).score


def main():
    marble_game = MarbleGame.read_file()
    print(f"Winning elf's score: {marble_game.play()}")

    marble_game_2 = MarbleGame.read_file(marble_multiplier=100)
    print(f"Winning elf's score with last marble 100 times larger: {marble_game_2.play()}")


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
