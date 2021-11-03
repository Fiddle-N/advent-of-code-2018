import collections
import enum
import timeit


class Acre(enum.Enum):
    OPEN_GROUND = '.'
    TREES = '|'
    LUMBERYARD = '#'


Coords = collections.namedtuple('Coords', 'x y')


DIRECTIONS = {
    'up': Coords(0, 1),
    'right-up': Coords(1, 1),
    'right': Coords(1, 0),
    'right-down': Coords(1, -1),
    'down': Coords(0, -1),
    'left-down': Coords(-1, -1),
    'left': Coords(-1, 0),
    'left-up': Coords(-1, 1),
}


class LumberCollectionArea:

    def __init__(self, grid_str=None):
        grid_str = grid_str if grid_str is not None else self._read_file()
        grid = [list(line) for line in grid_str.splitlines()]
        self.row_no = len(grid[0])
        self.col_no = len(grid)
        self.area = {}
        for y, row in enumerate(grid):
            for x, acre in enumerate(row):
                acre_position = Coords(x, y)
                self.area[acre_position] = Acre(acre)

    @staticmethod
    def _read_file():
        with open('input.txt') as f:
            return f.read()

    def output_grid(self, area):
        grid = [[None for _ in range(self.row_no)] for _ in range(self.col_no)]
        for acre_coords, acre in area.items():
            grid[acre_coords.y][acre_coords.x] = acre
        return LumberCollectionArea._to_str(grid)

    @staticmethod
    def _to_str(input_list):
        return '\n'.join([
            ''.join([acre.value for acre in row])
            for row in input_list
        ])


class LumberCollectionAreaModel:

    def __init__(self, lumber_collection_area):
        self.area = lumber_collection_area.area
        self.adj_acres = {acre_coords: self.surrounding_acres(acre_coords) for acre_coords in self.area}

    def __iter__(self):
        return self

    def __next__(self):
        current_seats = self.area
        self.area = {}
        for acre_coords, acre in current_seats.items():
            adj_acre_coords = self.adj_acres[acre_coords]
            adj_acres = collections.Counter(current_seats[adj_seat] for adj_seat in adj_acre_coords)
            if acre == Acre.OPEN_GROUND and adj_acres.get(Acre.TREES, 0) >= 3:
                self.area[acre_coords] = Acre.TREES
            elif acre == Acre.TREES and adj_acres.get(Acre.LUMBERYARD, 0) >= 3:
                self.area[acre_coords] = Acre.LUMBERYARD
            elif acre == Acre.LUMBERYARD and not (adj_acres.get(Acre.LUMBERYARD, 0) >= 1 and adj_acres.get(Acre.TREES, 0) >= 1):
                self.area[acre_coords] = Acre.OPEN_GROUND
            else:
                self.area[acre_coords] = acre
        return self.area

    def surrounding_acres(self, acre_coords):
        next_coords = []
        for direction in DIRECTIONS.values():
            next_coord = Coords(acre_coords.x + direction.x, acre_coords.y + direction.y)
            if next_coord in self.area:
                next_coords.append(next_coord)
        return next_coords

    def resource_value(self):
        area_count = collections.Counter(self.area.values())
        return area_count[Acre.TREES] * area_count[Acre.LUMBERYARD]


def run_model_part_1():
    lumber_collection_area = LumberCollectionArea()
    primed_model = LumberCollectionAreaModel(lumber_collection_area)
    for _ in range(10):
        next(primed_model)
    return primed_model.resource_value()


def run_model_part_2():
    runs = 1_000_000_000
    lumber_collection_area = LumberCollectionArea()
    lumber_collection_area_model = LumberCollectionAreaModel(lumber_collection_area)
    areas = set()
    repeating_group = []
    for run_no in range(runs):
        grid = next(lumber_collection_area_model)
        grid_str = lumber_collection_area.output_grid(grid)
        if grid_str in areas:
            if not repeating_group:
                repeating_group.append(grid_str)
                first_repetition_start = run_no
            elif grid_str in repeating_group:
                break
            else:
                repeating_group.append(grid_str)
        else:
            areas.add(grid_str)
    periodicity = len(repeating_group)
    multiply_factor = (runs - first_repetition_start) // periodicity
    offset = runs - (first_repetition_start + (multiply_factor * periodicity))
    area_count = collections.Counter(repeating_group[offset-1])
    return area_count[Acre.TREES.value] * area_count[Acre.LUMBERYARD.value]


def main():
    print(f'Resource value for lumber collection area model after 10 runs: {run_model_part_1()}')
    print(f'Resource value for lumber collection area model after more runs: {run_model_part_2()}')


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
