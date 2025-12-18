import itertools
import collections
import timeit

class ChronalCoods:

    def __init__(self):
        self.coords = []
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.infinite_coords = set()
        self.areas = collections.defaultdict(int)

    def read_file(self):
        self.coords = []
        with open('input.txt') as f:
            for line in f:
                coord = line.split(', ')
                coord = [int(x) for x in coord]
                self.coords.append(coord)

    def get_min_max(self):
        x_coords = [x for x, _ in self.coords]
        y_coords = [y for _, y in self.coords]
        self.min_x = min(x_coords)
        self.max_x = max(x_coords)
        self.min_y = min(y_coords)
        self.max_y = max(y_coords)

    def calculate_nearest_coords(self):
        for x, y in itertools.product(range(self.min_x, self.max_x + 1), range(self.min_y, self.max_y + 1)):
            distances = [abs(coord_x - x) + abs(coord_y - y) for coord_x, coord_y in self.coords]
            sorted_distances = sorted(distances)
            if not sorted_distances[0] == sorted_distances[1]:    # not equally close to at least two coords
                nearest_coord = distances.index(sorted_distances[0])    # retrieve closest coord
                self.areas[nearest_coord] += 1
                if x in (self.min_x, self.max_x) or y in (self.min_y, self.max_y):    # at edge of grid
                    self.infinite_coords.add(nearest_coord)

    def retrieve_largest_finite_area(self):
        finite_areas = [area for coord, area in self.areas.items() if coord not in self.infinite_coords]
        return max(finite_areas)

    def calculate_region_size_close_to_all_coords(self, max_distance):
        region_size = 0
        for x, y in itertools.product(range(self.min_x, self.max_x + 1), range(self.min_y, self.max_y + 1)):
            total_distance = sum(abs(coord_x - x) + abs(coord_y - y) for coord_x, coord_y in self.coords)
            if total_distance < max_distance:
                region_size += 1
        return region_size


def main():
    chronal_coods = ChronalCoods()
    chronal_coods.read_file()
    chronal_coods.get_min_max()
    chronal_coods.calculate_nearest_coords()
    max_finite_area = chronal_coods.retrieve_largest_finite_area()
    print(f'max finite area: {max_finite_area}')
    largest_region_size = chronal_coods.calculate_region_size_close_to_all_coords(10000)
    print(f'largest region size {largest_region_size}')


if __name__ == '__main__':
    print(f'time taken: {timeit.timeit(main, number=1)}')
