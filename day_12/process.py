import collections
import dataclasses
import timeit
import typing


PLANT = '#'
NO_PLANT = '.'


@dataclasses.dataclass(frozen=True)
class Plant:
    position: typing.Optional[int]
    plant: str


class PlantGeneration:

    def __init__(self, first_gen, spread):
        self.spread = spread
        self.gen_queue = collections.deque()
        for position, plant in first_gen.items():
            self.gen_queue.append(Plant(position, plant))
        self._clean_ends()
        self.previous_gen_queue = None

    @property
    def gen(self):
        return {plant.position: plant.plant for plant in self.gen_queue}

    @property
    def total(self):
        total = 0
        for plant in self.gen_queue:
            if plant.plant == PLANT:
                total += plant.position
        return total

    @property
    def number(self):
        return sum(bool(plant) for plant in self.gen_queue if plant.plant == PLANT)

    def __iter__(self):
        return self

    def __next__(self):
        self.previous_gen_queue = self.gen_queue.copy()
        self._add_end_plants()
        self._calculate_next_gen()
        self._clean_ends()
        return self.gen

    def _clean_ends(self):
        while True:
            left = self.gen_queue.popleft()
            if left.plant == PLANT:
                self.gen_queue.appendleft(left)
                break
        while True:
            right = self.gen_queue.pop()
            if right.plant == PLANT:
                self.gen_queue.append(right)
                break

    def _add_end_plants(self):
        left = self.gen_queue.popleft()
        left_position = left.position
        self.gen_queue.appendleft(left)
        self.gen_queue.appendleft(Plant(left_position - 1, NO_PLANT))
        self.gen_queue.appendleft(Plant(left_position - 2, NO_PLANT))

        right = self.gen_queue.pop()
        right_position = right.position
        self.gen_queue.append(right)
        self.gen_queue.append(Plant(right_position + 1, NO_PLANT))
        self.gen_queue.append(Plant(right_position + 2, NO_PLANT))

    def _calculate_next_gen(self):
        next_gen = collections.deque()
        buffer = []
        for _ in range(2):
            buffer.append(Plant(None, NO_PLANT))
        for _ in range(2):
            buffer.append(self.gen_queue.popleft())
        for _ in range(2):
            self.gen_queue.append(Plant(None, NO_PLANT))
        while self.gen_queue:
            buffer.append(self.gen_queue.popleft())
            position = buffer[2].position
            surrounding_plants = ''.join(plant.plant for plant in buffer)
            next_plant = self.spread[surrounding_plants]
            next_gen.append(Plant(position, next_plant))
            buffer.pop(0)
        self.gen_queue = next_gen


class SubterraneanSustainability:

    def __init__(self, input_, is_full_input=True):
        self.initial_state = None
        self.plant_gen = None
        self.spread = None
        self._preprocess(input_, is_full_input)

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read().rstrip())

    def _preprocess(self, input_, is_full_input):
        self.initial_state = {}
        self.spread = {} if is_full_input else collections.defaultdict(lambda: NO_PLANT)
        for line_no, line in enumerate(input_.splitlines()):
            if line_no == 0:
                _, raw_initial_state = line.split(': ')
                for position, plant in enumerate(raw_initial_state):
                    self.initial_state[position] = plant
            elif line_no >= 2:
                input_, output = line.split(' => ')
                self.spread[input_] = output
        self.plant_gen = PlantGeneration(self.initial_state, self.spread)

    def restart(self):
        self.plant_gen = PlantGeneration(self.initial_state, self.spread)

    def __iter__(self):
        i = 0
        while True:
            i += 1
            next(self.plant_gen)
            current_gen_plants = ''.join(plant.plant for plant in self.plant_gen.gen_queue)
            last_gen_plants = ''.join(plant.plant for plant in self.plant_gen.previous_gen_queue)
            if current_gen_plants == last_gen_plants:
                return self.plant_gen, i
            yield self.plant_gen


def main():
    subterranean_sustainability = SubterraneanSustainability.read_file()
    plant_gen = iter(subterranean_sustainability)
    plants = None
    for _ in range(20):
        plants = next(plant_gen)
    print('Plant total after 20 gen:', plants.total)

    subterranean_sustainability.restart()

    plant_gen = iter(subterranean_sustainability)
    while True:
        try:
            next(plant_gen)
        except StopIteration as e:
            plants_first_repetition, plants_first_repetition_iteration = e.value
            break

    gens = 50_000_000_000
    initial_plant_total = plants_first_repetition.total
    plant_number = plants_first_repetition.number
    gens_to_go = gens - plants_first_repetition_iteration

    total = initial_plant_total + plant_number * gens_to_go
    print('Plant total after 50 bil gen:', total)


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
