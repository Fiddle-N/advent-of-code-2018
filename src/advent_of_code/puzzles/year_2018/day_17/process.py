import dataclasses
import enum
import operator
import timeit


@dataclasses.dataclass(frozen=True, eq=True)
class Coords:
    x: int
    y: int


class Ground(enum.Enum):
    SAND = '.'
    CLAY = '#'
    WATER_FLOWING = '|'
    WATER_SETTLED = '~'


class WaterState(enum.Enum):
    WATER_FLOWING = enum.auto()
    WATER_SETTLED = enum.auto()
    WATER_ON_TOP_OF_CLAY_OR_WATER = enum.auto()
    WATER_FLOWING_FROM_OTHER_SOURCE = enum.auto()


class Side(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()


class ReservoirResearch:

    def __init__(self, input_):
        self.clay = self._clay_calc(input_)

        self.min_y_for_count = min(self.clay, key=lambda coords: coords.y).y
        self.max_y_for_count = max(self.clay, key=lambda coords: coords.y).y

        # add padding to minimum values to see in the graphical map
        self.min_x = min(self.clay, key=lambda coords: coords.x).x - 1
        self.max_x = max(self.clay, key=lambda coords: coords.x).x + 1
        self.min_y = self.min_y_for_count - 1
        self.max_y = self.max_y_for_count

        self.water = {}

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read().strip())

    def _clay_calc(self, input_):
        clay = set()
        for vein in input_.split('\n'):
            pos_1, pos_2 = vein.split(', ')
            pos_1_axis, raw_pos_1_val = pos_1.split('=')
            pos_1_val = int(raw_pos_1_val)
            pos_2_axis, raw_pos_2_range = pos_2.split('=')
            pos_2_start, pos_2_end = [int(pos_val) for pos_val in raw_pos_2_range.split('..')]
            pos_2_range = range(pos_2_start, pos_2_end + 1)
            for pos_2_val in pos_2_range:
                coord = Coords(**{pos_1_axis: pos_1_val, pos_2_axis: pos_2_val})
                clay.add(coord)
        return clay

    def map(self):
        min_x = self.min_x
        max_x = self.max_x
        min_y = self.min_y
        max_y = self.max_y

        map_list = []
        for y in range(min_y, max_y + 1):
            map_row = []
            for x in range(min_x, max_x + 1):
                if (coord := Coords(x, y)) in self.clay:
                    map_row.append(Ground.CLAY.value)
                elif coord in self.water:
                    water_type = self.water[coord]
                    map_row.append(water_type.value)
                else:
                    map_row.append(Ground.SAND.value)
            map_list.append(''.join(map_row))
        map = '\n'.join(map_list)
        return map

    def simulate_flow(self):
        y = self.min_y
        water = Coords(500, y)
        water_state = WaterState.WATER_FLOWING
        self._water_handler(water, water_state)

    def _water_handler(self, water, water_state):
        while True:      # while water.y <= self.max_y or while True?
            if water_state == WaterState.WATER_FLOWING:
                next_water_state = self._water_flowing(water, water_state)
            elif water_state == WaterState.WATER_ON_TOP_OF_CLAY_OR_WATER:
                next_water_state, next_water = self._water_on_top_of_clay(water)
            else:
                raise Exception

            if next_water_state == WaterState.WATER_FLOWING_FROM_OTHER_SOURCE:
                self.water[water] = Ground.WATER_FLOWING
                return

            elif water_state == WaterState.WATER_FLOWING and next_water_state == WaterState.WATER_FLOWING:
                next_water_y = water.y + 1
                water = Coords(water.x, next_water_y)
                if next_water_y == self.max_y:
                    self.water[water] = Ground.WATER_FLOWING
                    return

            elif water_state == WaterState.WATER_ON_TOP_OF_CLAY_OR_WATER and next_water_state == WaterState.WATER_SETTLED:
                next_water_y = water.y - 1
                water = Coords(water.x, next_water_y)
                next_water_state = WaterState.WATER_ON_TOP_OF_CLAY_OR_WATER

            elif water_state == WaterState.WATER_ON_TOP_OF_CLAY_OR_WATER and next_water_state == WaterState.WATER_FLOWING:
                for next_water_coords in next_water:
                    self._water_handler(next_water_coords, next_water_state)
                return

            water_state = next_water_state

    def _water_flowing(self, water, water_state):
        ground_below_water = Coords(water.x, water.y + 1)
        if ground_below_water in self.water and self.water[ground_below_water] == Ground.WATER_FLOWING:
            water_state = WaterState.WATER_FLOWING_FROM_OTHER_SOURCE
        elif ground_below_water in self.clay:
            water_state = WaterState.WATER_ON_TOP_OF_CLAY_OR_WATER
        else:
            self.water[water] = Ground.WATER_FLOWING
        return water_state

    def _water_on_top_of_clay(self, water):
        water_coords = [water]

        left_water_coords, left_water_state, left_last_water = self._water_on_top_of_clay_one_side(water, Side.LEFT)
        right_water_coords, right_water_state, right_last_water = self._water_on_top_of_clay_one_side(water, Side.RIGHT)

        water_coords.extend(left_water_coords)
        water_coords.extend(right_water_coords)

        if all(water_state == WaterState.WATER_SETTLED for water_state in (left_water_state, right_water_state)):
            # both sides must be settled on clay
            water_state = WaterState.WATER_SETTLED
            water_type = Ground.WATER_SETTLED
            next_water = water_coords       # we care about the water on the clay for the next operation
        else:
            water_state = WaterState.WATER_FLOWING
            water_type = Ground.WATER_FLOWING
            next_water = []

            # we care about where the water is dropping off for the next operation
            if left_water_state == WaterState.WATER_FLOWING:
                next_water.append(left_last_water)
            if right_water_state == WaterState.WATER_FLOWING:
                next_water.append(right_last_water)

        for water in water_coords:
            self.water[water] = water_type

        return water_state, next_water

    def _water_on_top_of_clay_one_side(self, water, side: Side):
        side_op = {Side.LEFT: operator.sub, Side.RIGHT: operator.add}[side]
        x_bound = {Side.LEFT: self.min_x, Side.RIGHT: self.max_x}[side]
        boundary_comp = {Side.LEFT: operator.ge, Side.RIGHT: operator.le}[side]

        water_coords = []

        x = side_op(water.x, 1)

        # if we are right at the edge of the map then water cannot be settled
        water_state = WaterState.WATER_FLOWING
        last_water = water

        while boundary_comp(x, x_bound):
            next_coords = Coords(x, water.y)
            if next_coords in self.clay:
                water_state = WaterState.WATER_SETTLED
                last_water = next_coords
                break
            water_coords.append(next_coords)    # this coordinate must be reachable by water (either settled or not)
            beneath_next_coords = Coords(x, water.y + 1)
            if beneath_next_coords in self.clay or (beneath_next_coords in self.water and self.water[beneath_next_coords] == Ground.WATER_SETTLED):
                x = side_op(x, 1)
            else:
                water_state = WaterState.WATER_FLOWING
                last_water = next_coords
                break

        return water_coords, water_state, last_water

    def count_water(self):
        return len([
            coord
            for coord in self.water
            if self.min_y_for_count <= coord.y <= self.max_y_for_count
        ])

    def count_settled_water(self):
        return len([
            coord
            for coord, water_type in self.water.items()
            if water_type == Ground.WATER_SETTLED
            and self.min_y_for_count <= coord.y <= self.max_y_for_count
        ])


def main():
    rr = ReservoirResearch.read_file()
    rr.simulate_flow()
    print(rr.map())
    print()
    print(f'Water in the map: {rr.count_water()}')
    print(f'Settled water in the map: {rr.count_settled_water()}')


if __name__ == '__main__':
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
