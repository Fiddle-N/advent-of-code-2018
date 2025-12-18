from advent_of_code.puzzles.year_2018.day_14 import process


class TestPart1:
    def test_example_1(self):
        chocolate_charts = process.ChocolateCharts()
        assert chocolate_charts.score_part_1(9) == '5158916779'

    def test_example_2(self):
        chocolate_charts = process.ChocolateCharts()
        assert chocolate_charts.score_part_1(5) == '0124515891'

    def test_example_3(self):
        chocolate_charts = process.ChocolateCharts()
        assert chocolate_charts.score_part_1(18) == '9251071085'

    def test_example_4(self):
        chocolate_charts = process.ChocolateCharts()
        assert chocolate_charts.score_part_1(2018) == '5941429882'


class TestPart2:
    def test_example_1(self):
        chocolate_charts = process.ChocolateCharts()
        assert chocolate_charts.score_part_2('51589') == 9

    def test_example_2(self):
        chocolate_charts = process.ChocolateCharts()
        assert chocolate_charts.score_part_2('01245') == 5

    def test_example_3(self):
        chocolate_charts = process.ChocolateCharts()
        assert chocolate_charts.score_part_2('92510') == 18

    def test_example_4(self):
        chocolate_charts = process.ChocolateCharts()
        assert chocolate_charts.score_part_2('59414') == 2018

    def test_check_after_scoreboard_extends_by_2(self):
        chocolate_charts = process.ChocolateCharts()
        assert chocolate_charts.score_part_2('15891') == 10
