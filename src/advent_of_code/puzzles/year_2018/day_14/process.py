import timeit


class ChocolateCharts:

    def __init__(self):
        self.initial_recipes = [3, 7]
        self.recipes = self.initial_recipes.copy()
        self.initial_elf_1_position = 0
        self.initial_elf_2_position = 1
        self.elf_1_position = self.initial_elf_1_position
        self.elf_2_position = self.initial_elf_2_position

    def score_part_1(self, score: int):
        self.recipes = self.initial_recipes.copy()
        self.elf_1_position = self.initial_elf_1_position
        self.elf_2_position = self.initial_elf_2_position
        iter_self = iter(self)
        while len(self.recipes) < (score + 10):
            next(iter_self)
        return ''.join(str(recipe) for recipe in self.recipes[score: score + 10])

    def score_part_2(self, score: str):
        self.recipes = self.initial_recipes.copy()
        self.elf_1_position = self.initial_elf_1_position
        self.elf_2_position = self.initial_elf_2_position
        processed_score = [int(digit) for digit in score]
        iter_self = iter(self)
        while self.recipes[-len(score):] != processed_score:
            next(iter_self)
        return len(self.recipes) - len(score)

    def __iter__(self):
        while True:
            elf_1_recipe = self.recipes[self.elf_1_position]
            elf_2_recipe = self.recipes[self.elf_2_position]
            total_int = elf_1_recipe + elf_2_recipe
            total = str(total_int)
            int_total = [int(x) for x in total]
            for recipe in int_total:
                self.recipes.append(recipe)
                yield
            self.elf_1_position = (self.elf_1_position + elf_1_recipe + 1) % len(self.recipes)
            self.elf_2_position = (self.elf_2_position + elf_2_recipe + 1) % len(self.recipes)


def main():
    with open("input.txt") as f:
        number_of_recipes = f.read().rstrip()
    chocolate_charts = ChocolateCharts()
    print('Score part 1:', chocolate_charts.score_part_1(int(number_of_recipes)))
    print('Score part 2:', chocolate_charts.score_part_2(number_of_recipes))


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")

