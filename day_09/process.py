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
        self.circle: list[typing.Optional[Marble]] = [None] * (last_marble + 1)
        self.elves = [Elf(elf_no) for elf_no in range(elves)]
        self.marbles = collections.deque(range(last_marble + 1))

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
        current_marble = self.marbles.popleft()
        self.circle[current_marble] = Marble(previous=current_marble, next=current_marble)
        for elf in itertools.cycle(self.elves):
            next_marble = self.marbles.popleft()
            if next_marble % 23 == 0:
                elf.score += next_marble

                for _ in range(7):
                    counter_clockwise = self.circle[current_marble].previous
                    current_marble = counter_clockwise

                one_counter_clockwise = self.circle[current_marble].previous
                one_clockwise = self.circle[current_marble].next

                self.circle[one_counter_clockwise].next = one_clockwise
                self.circle[current_marble] = None
                self.circle[one_clockwise].previous = one_counter_clockwise

                elf.score += current_marble

                current_marble = one_clockwise
            else:
                one_clockwise = self.circle[current_marble].next
                two_clockwise = self.circle[one_clockwise].next

                self.circle[one_clockwise].next = next_marble
                self.circle[next_marble] = Marble(previous=one_clockwise, next=two_clockwise)
                self.circle[two_clockwise].previous = next_marble

                current_marble = next_marble
            if not self.marbles:
                return max(self.elves, key=lambda elf_: elf_.score).score


def main():
    marble_game = MarbleGame.read_file()
    print(f"Winning elf's score: {marble_game.play()}")

    marble_game_2 = MarbleGame.read_file(marble_multiplier=100)
    print(f"Winning elf's score with last marble 100 times larger: {marble_game_2.play()}")


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
