import dataclasses
import itertools
import timeit
import typing

import more_itertools


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int


@dataclasses.dataclass(frozen=True)
class Matrix:
    top_left_x: int
    top_left_y: int
    size: int
    val: int


class FuelCells:

    def __init__(self, serial_no):
        self._serial_no = serial_no
        self.size = 300
        self.map = {}
        for x, y in itertools.product(range(1, self.size + 1), range(1, self.size + 1)):
            power_level = self.calculate_power_level(serial_no, x, y)
            self.map[Coords(x, y)] = power_level
        self.grid = []
        for row_no in range(1, self.size+1):
            row = []
            for col_no in range(1, self.size+1):
                row.append(self.map[Coords(col_no, row_no)])
            self.grid.append(row)
        self.nrows = len(self.grid)
        self.ncols = len(self.grid[0])



    @staticmethod
    def calculate_power_level(serial_no, x, y):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += serial_no
        power_level *= rack_id
        hundreds_digit = str(power_level).zfill(3)[-3]
        power_level = int(hundreds_digit) - 5
        return power_level


class ChronalCharge:

    def __init__(self, serial_no):
        self.fuel_cells = FuelCells(serial_no)

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(int(f.read().rstrip()))

    def largest_power_3_by_3(self):
        powers = {}
        for square_split_coords in itertools.product(more_itertools.windowed(range(1, 300), 3), more_itertools.windowed(range(1, 300), 3)):
            square_coords = itertools.product(*square_split_coords)
            (top_left,), square_coords = more_itertools.spy(square_coords)
            power = sum(self.fuel_cells.map[Coords(x, y)] for x, y in square_coords)
            powers[Coords(*top_left)] = power
        largest_power = max(powers, key=lambda coords: powers[coords])
        return largest_power.x, largest_power.y

    def _largest_power(self, k, summed_grid):
        largest_power = None
        for bottom_right_row_no in range(k - 1, self.fuel_cells.nrows):
            for bottom_right_col_no in range(k - 1, self.fuel_cells.ncols):

                # br_row_no br_col_no represent the bottom-right corner

                summed_val = summed_grid[bottom_right_row_no][bottom_right_col_no]
                matrix_val = summed_val

                if bottom_right_row_no >= k:
                    bottom_left = summed_grid[bottom_right_row_no - k][bottom_right_col_no]
                    matrix_val -= bottom_left

                if bottom_right_col_no >= k:
                    top_right = summed_grid[bottom_right_row_no][bottom_right_col_no - k]
                    matrix_val -= top_right

                if bottom_right_row_no >= k and bottom_right_col_no >= k:
                    top_left = summed_grid[bottom_right_row_no - k][bottom_right_col_no - k]
                    matrix_val += top_left

                if largest_power is None or matrix_val > largest_power.val:
                    top_left_col_no = bottom_right_col_no - k + 1
                    top_left_row_no = bottom_right_row_no - k + 1
                    top_left_x = top_left_col_no + 1
                    top_left_y = top_left_row_no + 1

                    largest_power = Matrix(
                        top_left_x=top_left_x,
                        top_left_y=top_left_y,
                        size=k,
                        val=matrix_val
                    )
        return largest_power

    def largest_power(self, start_k, end_k=None):

        summed_grid: list[list[typing.Optional[int]]] = [[None for _ in range(self.fuel_cells.nrows)] for _ in range(self.fuel_cells.ncols)]

        # first value
        summed_grid[0][0] = self.fuel_cells.grid[0][0]

        # first col
        for row_no in range(1, self.fuel_cells.nrows):
            summed_grid[row_no][0] = self.fuel_cells.grid[row_no][0] + summed_grid[row_no-1][0]

        # first row
        for col_no in range(1, self.fuel_cells.ncols):
            summed_grid[0][col_no] = self.fuel_cells.grid[0][col_no] + summed_grid[0][col_no-1]


        # the rest of the grid
        for row_no in range(1, self.fuel_cells.nrows):
            for col_no in range(1, self.fuel_cells.ncols):
                summed_grid[row_no][col_no] = (
                        self.fuel_cells.grid[row_no][col_no]
                        + summed_grid[row_no-1][col_no]
                        + summed_grid[row_no][col_no-1]
                        - summed_grid[row_no-1][col_no-1]
                )

        largest_power = None

        if end_k is None:
            largest_power = self._largest_power(start_k, summed_grid)
        else:
            for k in range(start_k, end_k+1):
                power = self._largest_power(k, summed_grid)
                if largest_power is None or power.val > largest_power.val:
                    largest_power = power

        return largest_power

    def largest_power_all_k(self):
        return self.largest_power(start_k=1, end_k=self.fuel_cells.ncols)


def main():
    chronal_charge = ChronalCharge.read_file()
    print('Largest power for 3x3 square:', chronal_charge.largest_power_3_by_3())
    largest_power_for_any_square = chronal_charge.largest_power_all_k()
    print(
        'Largest power for any square:',
        ','.join(str(val) for val in [
            largest_power_for_any_square.top_left_x,
            largest_power_for_any_square.top_left_y,
            largest_power_for_any_square.size
        ])
    )


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
