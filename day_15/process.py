import collections
import dataclasses
import enum
import timeit
import typing


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)

@dataclasses.dataclass(frozen=True)
class Path:
    path: list
    coord: Coords


class Map(enum.Enum):
    CAVERN = '.'
    WALL = '#'
    ELF = 'E'
    GOBLIN = 'G'


@dataclasses.dataclass(eq=True)
class Unit:
    unit_type: Map
    hit_points: int = 200


@dataclasses.dataclass(frozen=True)
class Summary:
    round_no: int
    hit_points: int
    outcome: int
    map: str
    grid: dict


DIRECTIONS = {
    'UP': Coords(0, -1),
    'LEFT': Coords(-1, 0),
    'RIGHT': Coords(1, 0),
    'DOWN': Coords(0, 1),
}


DEFAULT_ATTACK_POWER = 3


class ElfGoblinCombat:

    def __init__(self, grid, elf_attack=DEFAULT_ATTACK_POWER):
        self.grid = {coord: space for coord, space in grid.items() if space != Map.WALL}
        self.grid_walls = {coord: space for coord, space in grid.items() if space == Map.WALL}
        self._elf_attack = elf_attack
        self._goblin_attack = DEFAULT_ATTACK_POWER
        self._first_elf_death = False

    @staticmethod
    def read_file():
        with open('input.txt') as f:
            return f.read().strip()

    @classmethod
    def read_input(cls, input_, elf_attack=DEFAULT_ATTACK_POWER):
        grid = {}
        for y, line in enumerate(input_.split('\n')):
            for x, space in enumerate(line):
                space_enum = Map(space)
                if space_enum in (Map.ELF, Map.GOBLIN):
                    grid_space = Unit(space_enum)
                else:
                    grid_space = space_enum
                grid[Coords(x, y)] = grid_space
        return cls(grid, elf_attack)

    def _grid_unparse(self):
        full_grid = self.grid | self.grid_walls

        max_x = max(full_grid, key=lambda coords: coords.x).x
        max_y = max(full_grid, key=lambda coords: coords.y).y
        max_width = max_x + 1
        max_height = max_y + 1

        raw_grid_repr: list[list[typing.Optional[str]]] = [([None] * max_width) for _ in range(max_height)]
        for grid_coords, grid_space in full_grid.items():
            if isinstance(grid_space, Unit):
                space_enum = grid_space.unit_type
            else:
                space_enum = grid_space
            raw_grid_repr[grid_coords.y][grid_coords.x] = space_enum.value

        raw_grid_repr: list[list[str]]

        grid_repr = '\n'.join([''.join(row) for row in raw_grid_repr])
        return grid_repr

    def combat(self, break_at_first_elf_death=False):
        round_no = 0
        while True:
            win = self.round()
            if break_at_first_elf_death and self._first_elf_death:
                return False
            elif win:
                hit_points = self._hit_points()
                return Summary(
                    round_no,
                    hit_points,
                    outcome=round_no * hit_points,
                    map=self._grid_unparse(),
                    grid=self.grid,
                )
            else:
                round_no += 1
                yield

    def round(self):
        """
        Return True if game is won before all turns are complete. Return False if full round occurs.
        """
        units = [unit_coord for unit_coord, space in self.grid.items() if isinstance(space, Unit)]
        for unit_coord in units:
            if isinstance(self.grid[unit_coord], Unit):     # check unit did not die earlier in the round
                if self._win_condition():  # one team won before a full round
                    return True
                self.turn(unit_coord)
        return False

    def turn(self, unit_coord):
        if not (adj_targets := self._adj_targets(unit_coord)):
            unit_coord = self._move(unit_coord)
            adj_targets = self._adj_targets(unit_coord)
        if adj_targets:
            self._select_and_attack(adj_targets)

    def _adj_targets(self, unit_coord):
        try:
            unit = self.grid[unit_coord]
        except KeyError as e:
            raise ValueError('Wall is not a type of unit') from e
        if not isinstance(unit, Unit):
            raise ValueError('Cavern is not a type of unit')
        adj_coords = self._adj_coords(unit_coord)
        adj_targets = []
        for adj_coord in adj_coords:
            adj_space = self.grid[adj_coord]
            if isinstance(adj_space, Unit) and unit.unit_type != adj_space.unit_type:
                # if adjacent space is an enemy
                adj_targets.append(adj_coord)
        return adj_targets

    def _choose_step(self, unit_coord):
        unit = self.grid[unit_coord]
        if not isinstance(unit, Unit):
            raise ValueError('Space is not a type of unit')
        visited = [unit_coord]
        queue = collections.deque([Path(path=[], coord=unit_coord)])
        while queue:
            path = queue.popleft()
            adj_coords = self._adj_coords(path.coord)
            for adj_coord in adj_coords:
                if adj_coord in visited:
                    continue
                visited.append(adj_coord)
                adj_space = self.grid[adj_coord]
                if adj_space != Map.CAVERN:
                    continue
                next_path = Path(path=path.path.copy() + [adj_coord], coord=adj_coord)
                queue.append(next_path)
                adj_adj_coords = self._adj_coords(adj_coord)
                for adj_adj_coord in adj_adj_coords:
                    adj_adj_space = self.grid[adj_adj_coord]
                    if isinstance(adj_adj_space, Unit) and unit.unit_type != adj_adj_space.unit_type:
                        # if adjacent space is an enemy
                        return next_path.path[0]
        return None

    def _move(self, unit_coord):
        unit_type = self.grid[unit_coord]
        chosen_step = self._choose_step(unit_coord)
        if chosen_step:
            self.grid[unit_coord] = Map.CAVERN
            self.grid[chosen_step] = unit_type
            return chosen_step
        else:
            return unit_coord

    def _select_and_attack(self, adj_targets):
        target = self._select_target(adj_targets)
        self._attack(target)

    def _select_target(self, adj_targets):
        # selects weakest target - chooses first in reading order if tie
        weakest_target = min(adj_targets, key=lambda unit_coord: self.grid[unit_coord].hit_points)
        return weakest_target

    def _attack(self, target_coord):
        target = self.grid[target_coord]
        if target.unit_type == Map.ELF:
            target.hit_points -= self._goblin_attack
        elif target.unit_type == Map.GOBLIN:
            target.hit_points -= self._elf_attack
        if target.hit_points <= 0:
            # target is dead
            self.grid[target_coord] = Map.CAVERN
            if target.unit_type == Map.ELF:
                self._first_elf_death = True

    def _adj_coords(self, unit_coord):
        """
        Retrieve adjacent coordinates to the given coord.

        Coordinates returned will be any valid coordinates on the map, including wall spaces.
        """
        in_range = []
        for direction in DIRECTIONS.values():
            adj_coord = unit_coord + direction
            try:
                self.grid[adj_coord]
            except KeyError:
                continue
            in_range.append(adj_coord)
        return in_range

    def _win_condition(self):
        units = [space for space in self.grid.values() if isinstance(space, Unit)]
        unit_types = [unit.unit_type for unit in units]
        if len(set(unit_types)) == 1:
            # all of one type died
            return True
        return False

    def _hit_points(self):
        units = [space for space in self.grid.values() if isinstance(space, Unit)]
        hit_points = sum(unit.hit_points for unit in units)
        return hit_points


class VariableElfAttackPower:

    def __init__(self, input_):
        self._input_ = input_

    def search(self, step_size=10):
        lower_bound_attack, upper_bound_attack = self._find_boundary(step_size)
        return self._search(lower_bound_attack, upper_bound_attack)

    def _find_boundary(self, step_size):
        lower_bound_attack = DEFAULT_ATTACK_POWER
        upper_bound_attack = DEFAULT_ATTACK_POWER + step_size
        while True:
            result = self._run(upper_bound_attack)
            if bool(result):
                return lower_bound_attack, upper_bound_attack
            else:
                lower_bound_attack = upper_bound_attack
                upper_bound_attack = upper_bound_attack + step_size

    def _search(self, lower_bound_attack, upper_bound_attack):
        middle_attack = (lower_bound_attack + upper_bound_attack) // 2
        result = self._run(middle_attack)
        result_plus_one = self._run(middle_attack + 1)
        if (result_pair := (bool(result), bool(result_plus_one))) == (False, True):
            # crossover point found where elf loss turns into elf win
            return (middle_attack + 1), result_plus_one
        elif result_pair == (False, False):
            # elves still losing - search for higher elf power
            return self._search(middle_attack, upper_bound_attack)
        elif result_pair == (True, True):
            # elves too powerful - search for lower elf power
            return self._search(lower_bound_attack, middle_attack)

    def _run(self, elf_attack):
        elf_goblin_combat = ElfGoblinCombat.read_input(self._input_, elf_attack)
        combat_gen = elf_goblin_combat.combat(break_at_first_elf_death=True)
        try:
            while True:
                next(combat_gen)
        except StopIteration as e:
            result = e.value
        return result


def main():
    input_ = ElfGoblinCombat.read_file()

    beverage_bandits = ElfGoblinCombat.read_input(input_)
    combat_gen = beverage_bandits.combat()

    try:
        while True:
            next(combat_gen)
    except StopIteration as e:
        part_1_summary = e.value

    print(f'Part 1: round no: {part_1_summary.round_no}')
    print(f'Part 1: hit points: {part_1_summary.hit_points}')
    print(f'Part 1: outcome: {part_1_summary.outcome}')

    print()

    variable_elf_attack_power = VariableElfAttackPower(input_)
    attack, part_2_summary = variable_elf_attack_power.search(step_size=10)

    print(f'Part 2: attack: {attack}')
    print(f'Part 2: round no: {part_2_summary.round_no}')
    print(f'Part 2: hit points: {part_2_summary.hit_points}')
    print(f'Part 2: outcome: {part_2_summary.outcome}')


if __name__ == '__main__':
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
