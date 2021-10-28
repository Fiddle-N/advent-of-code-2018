import pytest

from day_15 import process


class TestGridParse:
    def test_grid_parse(self):
        input_ = """\
#######
#.G.E.#
#E.G.E#
#.G.E.#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits.grid == {
            process.Coords(1, 1): process.Map.CAVERN,
            process.Coords(2, 1): process.Unit(process.Map.GOBLIN),
            process.Coords(3, 1): process.Map.CAVERN,
            process.Coords(4, 1): process.Unit(process.Map.ELF),
            process.Coords(5, 1): process.Map.CAVERN,
            process.Coords(1, 2): process.Unit(process.Map.ELF),
            process.Coords(2, 2): process.Map.CAVERN,
            process.Coords(3, 2): process.Unit(process.Map.GOBLIN),
            process.Coords(4, 2): process.Map.CAVERN,
            process.Coords(5, 2): process.Unit(process.Map.ELF),
            process.Coords(1, 3): process.Map.CAVERN,
            process.Coords(2, 3): process.Unit(process.Map.GOBLIN),
            process.Coords(3, 3): process.Map.CAVERN,
            process.Coords(4, 3): process.Unit(process.Map.ELF),
            process.Coords(5, 3): process.Map.CAVERN,
        }


class TestAdjTargets:

    def test_adj_target_raises_exception_if_passed_a_wall_space(self):
        input_ = """\
#######
#.GE..#
#.E...#
#...G.#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        with pytest.raises(ValueError):
            beverage_bandits._adj_targets(process.Coords(0, 0))

    def test_adj_target_raises_exception_if_passed_a_cavern_space(self):
        input_ = """\
#######
#.GE..#
#.E...#
#...G.#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        with pytest.raises(ValueError):
            beverage_bandits._adj_targets(process.Coords(1, 1))

    def test_adj_target_with_no_units_in_range(self):
        input_ = """\
#######
#.GE..#
#.E...#
#...G.#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits._adj_targets(process.Coords(4, 3)) == []

    def test_adj_target_with_one_units_in_range(self):
        input_ = """\
#######
#.GE..#
#.E...#
#...G.#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits._adj_targets(process.Coords(3, 1)) == [process.Coords(2, 1)]

    def test_adj_target_with_multiple_units_in_range_returns_units_in_reading_order(self):
        input_ = """\
#######
#.E...#
#EGE..#
#.E...#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits._adj_targets(process.Coords(2, 2)) == [
            process.Coords(2, 1),
            process.Coords(1, 2),
            process.Coords(3, 2),
            process.Coords(2, 3),
        ]

    def test_adj_target_only_picks_up_enemy_targets(self):
        input_ = """\
#######
#.GE..#
#.G...#
#.....#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits._adj_targets(process.Coords(2, 1)) == [process.Coords(3, 1)]


class TestChooseStep:

    def test_target_picks_up_in_range_squares_for_one_target(self):
        input_ = """\
#######
#.....#
#.G.E.#
#.....#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits._choose_step(process.Coords(2, 2)) == process.Coords(3, 2)

    def test_target_picks_up_in_range_squares_for_multiple_targets(self):
        input_ = """\
#######
#.....#
#.G.E.#
#.....#
#...E.#
#.....#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits._choose_step(process.Coords(2, 2)) == process.Coords(3, 2)

    def test_target_does_not_consider_in_range_squares_for_friendly_units(self):
        input_ = """\
#######
#.....#
#.G.G.#
#.....#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits._choose_step(process.Coords(2, 2)) is None

    def test_target_does_not_consider_in_range_squares_for_targets_that_are_unreachable(self):
        input_ = """\
###########
#......G..#
#.G....#.E#
#......G..#
###########"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits._choose_step(process.Coords(2, 2)) is None

    def test_target_finds_shortest_path_by_reading_order(self):
        input_ = """\
#######
#.....#
#.GE..#
#.....#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits._choose_step(process.Coords(2, 2)) == process.Coords(2, 1)


class TestMove:

    def test_move_if_valid_move_exists(self):
        input_ = """\
#######
#.....#
#.GE..#
#.....#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits.grid[process.Coords(2, 1)] == process.Map.CAVERN
        assert beverage_bandits.grid[process.Coords(2, 2)] == process.Unit(process.Map.GOBLIN)

        new_position = beverage_bandits._move(process.Coords(2, 2))
        assert new_position == process.Coords(2, 1)
        assert beverage_bandits.grid[process.Coords(2, 1)] == process.Unit(process.Map.GOBLIN)
        assert beverage_bandits.grid[process.Coords(2, 2)] == process.Map.CAVERN

    def test_dont_move_if_valid_move_does_not_exist(self):
        input_ = """\
#######
#.....#
#.GG..#
#.....#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(input_)
        assert beverage_bandits.grid[process.Coords(2, 1)] == process.Map.CAVERN
        assert beverage_bandits.grid[process.Coords(2, 2)] == process.Unit(process.Map.GOBLIN)

        new_position = beverage_bandits._move(process.Coords(2, 2))
        assert new_position == process.Coords(2, 2)
        assert beverage_bandits.grid[process.Coords(2, 1)] == process.Map.CAVERN
        assert beverage_bandits.grid[process.Coords(2, 2)] == process.Unit(process.Map.GOBLIN)


class TestTurn:

    def test_larger_example_of_movement(self):
        initial_grid = """\
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########"""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)

        beverage_bandits.round()

        expected_grid_round_1 = """\
#########
#.G...G.#
#...G...#
#...E..G#
#.G.....#
#.......#
#G..G..G#
#.......#
#########"""
        actual_grid_round_1 = beverage_bandits._grid_unparse()
        assert actual_grid_round_1 == expected_grid_round_1

        beverage_bandits.round()

        expected_grid_round_2 = """\
#########
#..G.G..#
#...G...#
#.G.E.G.#
#.......#
#G..G..G#
#.......#
#.......#
#########"""
        actual_grid_round_2 = beverage_bandits._grid_unparse()
        assert actual_grid_round_2 == expected_grid_round_2

        beverage_bandits.round()

        expected_grid_round_3 = """\
#########
#.......#
#..GGG..#
#..GEG..#
#G..G...#
#......G#
#.......#
#.......#
#########"""
        actual_grid_round_3 = beverage_bandits._grid_unparse()
        assert actual_grid_round_3 == expected_grid_round_3



class TestSelectAndAttack:

    def test_select_and_attack_health_does_not_drop_below_0_and_unit_does_not_die(self):
        initial_grid = """\
G....
..G..
..EG.
..G..
...G."""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)

        beverage_bandits.grid[process.Coords(0, 0)].hit_points = 9
        beverage_bandits.grid[process.Coords(2, 1)].hit_points = 5
        beverage_bandits.grid[process.Coords(3, 2)].hit_points = 4
        beverage_bandits.grid[process.Coords(2, 3)].hit_points = 4
        beverage_bandits.grid[process.Coords(3, 4)].hit_points = 1

        beverage_bandits._select_and_attack([process.Coords(2, 1), process.Coords(3, 2), process.Coords(2, 3)])

        assert beverage_bandits.grid[process.Coords(0, 0)].hit_points == 9
        assert beverage_bandits.grid[process.Coords(2, 1)].hit_points == 5
        assert beverage_bandits.grid[process.Coords(2, 3)].hit_points == 4
        assert beverage_bandits.grid[process.Coords(3, 4)].hit_points == 1

        assert beverage_bandits.grid[process.Coords(3, 2)].hit_points == 1

    def test_select_and_attack_health_goes_to_exactly_0_and_unit_dies(self):
        initial_grid = """\
G....
..G..
..EG.
..G..
...G."""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)

        beverage_bandits.grid[process.Coords(0, 0)].hit_points = 9
        beverage_bandits.grid[process.Coords(2, 1)].hit_points = 4
        beverage_bandits.grid[process.Coords(3, 2)].hit_points = 3
        beverage_bandits.grid[process.Coords(2, 3)].hit_points = 3
        beverage_bandits.grid[process.Coords(3, 4)].hit_points = 1

        beverage_bandits._select_and_attack([process.Coords(2, 1), process.Coords(3, 2), process.Coords(2, 3)])

        assert beverage_bandits.grid[process.Coords(0, 0)].hit_points == 9
        assert beverage_bandits.grid[process.Coords(2, 1)].hit_points == 4
        assert beverage_bandits.grid[process.Coords(2, 3)].hit_points == 3
        assert beverage_bandits.grid[process.Coords(3, 4)].hit_points == 1

        assert beverage_bandits.grid[process.Coords(3, 2)] == process.Map.CAVERN

    def test_select_and_attack_health_drops_below_0_and_unit_dies(self):
        initial_grid = """\
G....
..G..
..EG.
..G..
...G."""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)

        beverage_bandits.grid[process.Coords(0, 0)].hit_points = 9
        beverage_bandits.grid[process.Coords(2, 1)].hit_points = 4
        beverage_bandits.grid[process.Coords(3, 2)].hit_points = 2
        beverage_bandits.grid[process.Coords(2, 3)].hit_points = 2
        beverage_bandits.grid[process.Coords(3, 4)].hit_points = 1

        beverage_bandits._select_and_attack([process.Coords(2, 1), process.Coords(3, 2), process.Coords(2, 3)])

        assert beverage_bandits.grid[process.Coords(0, 0)].hit_points == 9
        assert beverage_bandits.grid[process.Coords(2, 1)].hit_points == 4
        assert beverage_bandits.grid[process.Coords(2, 3)].hit_points == 2
        assert beverage_bandits.grid[process.Coords(3, 4)].hit_points == 1

        assert beverage_bandits.grid[process.Coords(3, 2)] == process.Map.CAVERN


class TestCombat:

    def test_combat_with_elf_death_before_end_of_turn_1_and_no_more_goblins_count_as_1_full_turn(self):
        initial_grid = """\
.....
..G..
..E..
.....
....."""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)

        beverage_bandits.grid[process.Coords(2, 2)].hit_points = 1      # dies after 1 hits

        # does not raise exception
        combat_gen = beverage_bandits.combat()

        try:
            while True:
                next(combat_gen)
        except StopIteration as e:
            summary = e.value

        assert summary.round_no == 1        # one full round occurs as combat goes to second round but second round ends prematurely

    def test_combat_with_elf_death_before_end_of_turn_1_and_at_least_one_goblin_left_does_not_count_as_1_full_turn(self):
        initial_grid = """\
.....
..G..
..E..
..G..
....."""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)

        beverage_bandits.grid[process.Coords(2, 2)].hit_points = 1  # dies after 1 hits

        # does not raise exception
        combat_gen = beverage_bandits.combat()

        try:
            while True:
                next(combat_gen)
        except StopIteration as e:
            summary = e.value

        assert summary.round_no == 0        # no full round occurs as the combat ends prematurely in first round - second goblin has no targets


class TestComplexCombat:

    def test_detailed_sample_combat(self):
        initial_grid = """\
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)
        combat_gen = beverage_bandits.combat()

        next(combat_gen)

        # round 1

        assert beverage_bandits._grid_unparse() == """\
#######
#..G..#
#...EG#
#.#G#G#
#...#E#
#.....#
#######"""

        assert beverage_bandits.grid[process.Coords(3, 1)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(3, 1)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(4, 2)].unit_type == process.Map.ELF
        assert beverage_bandits.grid[process.Coords(4, 2)].hit_points == 197

        assert beverage_bandits.grid[process.Coords(5, 2)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 2)].hit_points == 197

        assert beverage_bandits.grid[process.Coords(3, 3)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(3, 3)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(5, 3)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 3)].hit_points == 197

        assert beverage_bandits.grid[process.Coords(5, 4)].unit_type == process.Map.ELF
        assert beverage_bandits.grid[process.Coords(5, 4)].hit_points == 197

        next(combat_gen)

        # round 2

        assert beverage_bandits._grid_unparse() == """\
#######
#...G.#
#..GEG#
#.#.#G#
#...#E#
#.....#
#######"""

        assert beverage_bandits.grid[process.Coords(4, 1)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(4, 1)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(3, 2)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(3, 2)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(4, 2)].unit_type == process.Map.ELF
        assert beverage_bandits.grid[process.Coords(4, 2)].hit_points == 188

        assert beverage_bandits.grid[process.Coords(5, 2)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 2)].hit_points == 194

        assert beverage_bandits.grid[process.Coords(5, 3)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 3)].hit_points == 194

        assert beverage_bandits.grid[process.Coords(5, 4)].unit_type == process.Map.ELF
        assert beverage_bandits.grid[process.Coords(5, 4)].hit_points == 194

        for _ in range(21):
            next(combat_gen)

        # round 23

        assert beverage_bandits._grid_unparse() == """\
#######
#...G.#
#..G.G#
#.#.#G#
#...#E#
#.....#
#######"""

        assert beverage_bandits.grid[process.Coords(4, 1)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(4, 1)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(3, 2)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(3, 2)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(4, 2)] == process.Map.CAVERN

        assert beverage_bandits.grid[process.Coords(5, 2)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 2)].hit_points == 131

        assert beverage_bandits.grid[process.Coords(5, 3)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 3)].hit_points == 131

        assert beverage_bandits.grid[process.Coords(5, 4)].unit_type == process.Map.ELF
        assert beverage_bandits.grid[process.Coords(5, 4)].hit_points == 131

        next(combat_gen)

        # round 24

        assert beverage_bandits._grid_unparse() == """\
#######
#..G..#
#...G.#
#.#G#G#
#...#E#
#.....#
#######"""

        assert beverage_bandits.grid[process.Coords(3, 1)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(3, 1)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(4, 2)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(4, 2)].hit_points == 131

        assert beverage_bandits.grid[process.Coords(3, 3)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(3, 3)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(5, 3)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 3)].hit_points == 128

        assert beverage_bandits.grid[process.Coords(5, 4)].unit_type == process.Map.ELF
        assert beverage_bandits.grid[process.Coords(5, 4)].hit_points == 128

        next(combat_gen)

        # round 25

        assert beverage_bandits._grid_unparse() == """\
#######
#.G...#
#..G..#
#.#.#G#
#..G#E#
#.....#
#######"""

        assert beverage_bandits.grid[process.Coords(2, 1)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(2, 1)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(3, 2)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(3, 2)].hit_points == 131

        assert beverage_bandits.grid[process.Coords(5, 3)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 3)].hit_points == 125

        assert beverage_bandits.grid[process.Coords(3, 4)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(3, 4)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(5, 4)].unit_type == process.Map.ELF
        assert beverage_bandits.grid[process.Coords(5, 4)].hit_points == 125

        next(combat_gen)

        # round 26

        assert beverage_bandits._grid_unparse() == """\
#######
#G....#
#.G...#
#.#.#G#
#...#E#
#..G..#
#######"""

        assert beverage_bandits.grid[process.Coords(1, 1)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(1, 1)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(2, 2)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(2, 2)].hit_points == 131

        assert beverage_bandits.grid[process.Coords(5, 3)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 3)].hit_points == 122

        assert beverage_bandits.grid[process.Coords(5, 4)].unit_type == process.Map.ELF
        assert beverage_bandits.grid[process.Coords(5, 4)].hit_points == 122

        assert beverage_bandits.grid[process.Coords(3, 5)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(3, 5)].hit_points == 200

        next(combat_gen)

        # round 27

        assert beverage_bandits._grid_unparse() == """\
#######
#G....#
#.G...#
#.#.#G#
#...#E#
#...G.#
#######"""

        assert beverage_bandits.grid[process.Coords(1, 1)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(1, 1)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(2, 2)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(2, 2)].hit_points == 131

        assert beverage_bandits.grid[process.Coords(5, 3)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 3)].hit_points == 119

        assert beverage_bandits.grid[process.Coords(5, 4)].unit_type == process.Map.ELF
        assert beverage_bandits.grid[process.Coords(5, 4)].hit_points == 119

        assert beverage_bandits.grid[process.Coords(4, 5)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(4, 5)].hit_points == 200

        next(combat_gen)

        # round 28

        assert beverage_bandits._grid_unparse() == """\
#######
#G....#
#.G...#
#.#.#G#
#...#E#
#....G#
#######"""

        assert beverage_bandits.grid[process.Coords(1, 1)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(1, 1)].hit_points == 200

        assert beverage_bandits.grid[process.Coords(2, 2)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(2, 2)].hit_points == 131

        assert beverage_bandits.grid[process.Coords(5, 3)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 3)].hit_points == 116

        assert beverage_bandits.grid[process.Coords(5, 4)].unit_type == process.Map.ELF
        assert beverage_bandits.grid[process.Coords(5, 4)].hit_points == 113

        assert beverage_bandits.grid[process.Coords(5, 5)].unit_type == process.Map.GOBLIN
        assert beverage_bandits.grid[process.Coords(5, 5)].hit_points == 200

        try:
            while True:
                next(combat_gen)
        except StopIteration as e:
            summary = e.value

        assert summary.round_no == 47
        assert summary.hit_points == 590
        assert summary.outcome == 27730

        assert summary.map == """\
#######
#G....#
#.G...#
#.#.#G#
#...#.#
#....G#
#######"""

        assert summary.grid[process.Coords(1, 1)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(1, 1)].hit_points == 200

        assert summary.grid[process.Coords(2, 2)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(2, 2)].hit_points == 131

        assert summary.grid[process.Coords(5, 3)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(5, 3)].hit_points == 59

        assert summary.grid[process.Coords(5, 4)] == process.Map.CAVERN

        assert summary.grid[process.Coords(5, 5)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(5, 5)].hit_points == 200

    def test_summary_sample_combat_1(self):
        initial_grid = """\
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)
        combat_gen = beverage_bandits.combat()

        try:
            while True:
                next(combat_gen)
        except StopIteration as e:
            summary = e.value

        assert summary.round_no == 37
        assert summary.hit_points == 982
        assert summary.outcome == 36334

        assert summary.map == """\
#######
#...#E#
#E#...#
#.E##.#
#E..#E#
#.....#
#######"""

        assert summary.grid[process.Coords(5, 1)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(5, 1)].hit_points == 200

        assert summary.grid[process.Coords(1, 2)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(1, 2)].hit_points == 197

        assert summary.grid[process.Coords(2, 3)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(2, 3)].hit_points == 185

        assert summary.grid[process.Coords(1, 4)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(1, 4)].hit_points == 200

        assert summary.grid[process.Coords(5, 4)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(5, 4)].hit_points == 200

    def test_summary_sample_combat_2(self):
        initial_grid = """\
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)
        combat_gen = beverage_bandits.combat()

        try:
            while True:
                next(combat_gen)
        except StopIteration as e:
            summary = e.value

        assert summary.round_no == 46
        assert summary.hit_points == 859
        assert summary.outcome == 39514

        assert summary.map == """\
#######
#.E.E.#
#.#E..#
#E.##.#
#.E.#.#
#...#.#
#######"""

        assert summary.grid[process.Coords(2, 1)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(2, 1)].hit_points == 164

        assert summary.grid[process.Coords(4, 1)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(4, 1)].hit_points == 197

        assert summary.grid[process.Coords(3, 2)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(3, 2)].hit_points == 200

        assert summary.grid[process.Coords(1, 3)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(1, 3)].hit_points == 98

        assert summary.grid[process.Coords(2, 4)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(2, 4)].hit_points == 200

    def test_summary_sample_combat_3(self):
        initial_grid = """\
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)
        combat_gen = beverage_bandits.combat()

        try:
            while True:
                next(combat_gen)
        except StopIteration as e:
            summary = e.value

        assert summary.round_no == 35
        assert summary.hit_points == 793
        assert summary.outcome == 27755

        assert summary.map == """\
#######
#G.G#.#
#.#G..#
#..#..#
#...#G#
#...G.#
#######"""

        assert summary.grid[process.Coords(1, 1)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(1, 1)].hit_points == 200

        assert summary.grid[process.Coords(3, 1)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(3, 1)].hit_points == 98

        assert summary.grid[process.Coords(3, 2)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(3, 2)].hit_points == 200

        assert summary.grid[process.Coords(5, 4)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(5, 4)].hit_points == 95

        assert summary.grid[process.Coords(4, 5)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(4, 5)].hit_points == 200

    def test_summary_sample_combat_4(self):
        initial_grid = """\
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######"""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)
        combat_gen = beverage_bandits.combat()

        try:
            while True:
                next(combat_gen)
        except StopIteration as e:
            summary = e.value

        assert summary.round_no == 54
        assert summary.hit_points == 536
        assert summary.outcome == 28944

        assert summary.map == """\
#######
#.....#
#.#G..#
#.###.#
#.#.#.#
#G.G#G#
#######"""

        assert summary.grid[process.Coords(3, 2)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(3, 2)].hit_points == 200

        assert summary.grid[process.Coords(1, 5)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(1, 5)].hit_points == 98

        assert summary.grid[process.Coords(3, 5)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(3, 5)].hit_points == 38

        assert summary.grid[process.Coords(5, 5)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(5, 5)].hit_points == 200

    def test_summary_sample_combat_5(self):
        initial_grid = """\
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""
        beverage_bandits = process.ElfGoblinCombat.read_input(initial_grid)
        combat_gen = beverage_bandits.combat()

        try:
            while True:
                next(combat_gen)
        except StopIteration as e:
            summary = e.value

        assert summary.round_no == 20
        assert summary.hit_points == 937
        assert summary.outcome == 18740

        assert summary.map == """\
#########
#.G.....#
#G.G#...#
#.G##...#
#...##..#
#.G.#...#
#.......#
#.......#
#########"""

        assert summary.grid[process.Coords(2, 1)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(2, 1)].hit_points == 137

        assert summary.grid[process.Coords(1, 2)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(1, 2)].hit_points == 200

        assert summary.grid[process.Coords(3, 2)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(3, 2)].hit_points == 200

        assert summary.grid[process.Coords(2, 3)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(2, 3)].hit_points == 200

        assert summary.grid[process.Coords(2, 5)].unit_type == process.Map.GOBLIN
        assert summary.grid[process.Coords(2, 5)].hit_points == 200


class TestVariableElfAttackPower:

    def test_summary_sample_combat_1(self):
        initial_grid = """\
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""
        variable_elf_attack_power = process.VariableElfAttackPower(initial_grid)
        attack, summary = variable_elf_attack_power.search()

        assert attack == 15

        assert summary.round_no == 29
        assert summary.hit_points == 172
        assert summary.outcome == 4988

        assert summary.map == """\
#######
#..E..#
#...E.#
#.#.#.#
#...#.#
#.....#
#######"""

        assert summary.grid[process.Coords(3, 1)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(3, 1)].hit_points == 158

        assert summary.grid[process.Coords(4, 2)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(4, 2)].hit_points == 14

    def test_summary_sample_combat_2(self):
        initial_grid = """\
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######"""
        variable_elf_attack_power = process.VariableElfAttackPower(initial_grid)
        attack, summary = variable_elf_attack_power.search()

        assert attack == 4

        assert summary.round_no == 33
        assert summary.hit_points == 948
        assert summary.outcome == 31284

        assert summary.map == """\
#######
#.E.E.#
#.#E..#
#E.##E#
#.E.#.#
#...#.#
#######"""

        assert summary.grid[process.Coords(2, 1)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(2, 1)].hit_points == 200

        assert summary.grid[process.Coords(4, 1)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(4, 1)].hit_points == 23

        assert summary.grid[process.Coords(3, 2)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(3, 2)].hit_points == 200

        assert summary.grid[process.Coords(1, 3)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(1, 3)].hit_points == 125

        assert summary.grid[process.Coords(5, 3)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(5, 3)].hit_points == 200

        assert summary.grid[process.Coords(2, 4)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(2, 4)].hit_points == 200

    def test_summary_sample_combat_3(self):
        initial_grid = """\
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"""
        variable_elf_attack_power = process.VariableElfAttackPower(initial_grid)
        attack, summary = variable_elf_attack_power.search()

        assert attack == 15

        assert summary.round_no == 37
        assert summary.hit_points == 94
        assert summary.outcome == 3478

        assert summary.map == """\
#######
#.E.#.#
#.#E..#
#..#..#
#...#.#
#.....#
#######"""

        assert summary.grid[process.Coords(2, 1)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(2, 1)].hit_points == 8

        assert summary.grid[process.Coords(3, 2)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(3, 2)].hit_points == 86

    def test_summary_sample_combat_4(self):
        initial_grid = """\
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######"""
        variable_elf_attack_power = process.VariableElfAttackPower(initial_grid)
        attack, summary = variable_elf_attack_power.search()

        assert attack == 12

        assert summary.round_no == 39
        assert summary.hit_points == 166
        assert summary.outcome == 6474

        assert summary.map == """\
#######
#...E.#
#.#..E#
#.###.#
#.#.#.#
#...#.#
#######"""

        assert summary.grid[process.Coords(4, 1)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(4, 1)].hit_points == 14

        assert summary.grid[process.Coords(5, 2)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(5, 2)].hit_points == 152

    def test_summary_sample_combat_5(self):
        initial_grid = """\
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""
        variable_elf_attack_power = process.VariableElfAttackPower(initial_grid)
        attack, summary = variable_elf_attack_power.search()

        assert attack == 34

        assert summary.round_no == 30
        assert summary.hit_points == 38
        assert summary.outcome == 1140

        assert summary.map == """\
#########
#.......#
#.E.#...#
#..##...#
#...##..#
#...#...#
#.......#
#.......#
#########"""

        assert summary.grid[process.Coords(2, 2)].unit_type == process.Map.ELF
        assert summary.grid[process.Coords(2, 2)].hit_points == 38
