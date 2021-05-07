import collections
import copy
import dataclasses
import string
import timeit


@dataclasses.dataclass
class Worker:
    number: int
    _seconds_remaining: int = 0
    letter: str = None


    @property
    def seconds_remaining(self):
        return self._seconds_remaining

    @seconds_remaining.setter
    def seconds_remaining(self, value):
        if value < 0:
            value = 0
        self._seconds_remaining = value


class Instructions:

    def __init__(self, instructions):
        self.dependencies = collections.defaultdict(list)
        self.letters = set()
        for line in instructions.splitlines():
            words = line.split(' ')
            self.dependencies[words[7]].append(words[1])
            self.letters.add(words[1])
            self.letters.add(words[7])

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read())

    @staticmethod
    def _remove_letter_as_dependency(letter, dependencies):
        for letter_dependency in dependencies.values():
            if letter in letter_dependency:
                letter_dependency.remove(letter)

    def determine_order(self, worker_no, offset):
        dependencies = copy.deepcopy(self.dependencies)
        letters = sorted(list(self.letters))
        done = []

        workers = []
        for no in range(worker_no):
            workers.append(Worker(no))

        seconds = 0
        while True:
            for worker in workers:
                if not worker.seconds_remaining:
                    # worker is free
                    if worker.letter is not None:
                        self._remove_letter_as_dependency(worker.letter, dependencies)
                        done.append(worker.letter)
                        worker.letter = None
                    for letter in letters.copy():
                        if not dependencies[letter]:
                            # assign task to worker
                            time = offset + string.ascii_uppercase.index(letter) + 1
                            worker.seconds_remaining = time
                            worker.letter = letter

                            letters.remove(letter)
                            break
                worker.seconds_remaining -= 1
            if set(done) == self.letters:
                return ''.join(done), seconds
            seconds += 1


def main():
    i = Instructions.read_file()
    print(f'Instructions with 1 worker: {i.determine_order(worker_no=1, offset=0)}')
    print(f'Instructions with 5 workers and 60 sec duration: {i.determine_order(worker_no=5, offset=60)}')


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')

