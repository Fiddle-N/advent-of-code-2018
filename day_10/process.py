import dataclasses
import re
import timeit


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)


@dataclasses.dataclass
class Point:
    position: Coords
    velocity: Coords


class Points(list):

    POINT = '#'
    SPACE = '.'

    @property
    def min_position_x(self):
        return min(self, key=lambda point: point.position.x).position.x

    @property
    def max_position_x(self):
        return max(self, key=lambda point: point.position.x).position.x

    @property
    def min_position_y(self):
        return min(self, key=lambda point: point.position.y).position.y

    @property
    def max_position_y(self):
        return max(self, key=lambda point: point.position.y).position.y

    @property
    def area(self):
        return (self.max_position_x - self.min_position_x) * (self.max_position_y - self.min_position_y)

    def image(self):
        positions = {point.position for point in self}
        raw_image = []
        for y in range(self.min_position_y, self.max_position_y + 1):
            row = []
            for x in range(self.min_position_x, self.max_position_x + 1):
                row.append(self.POINT if Coords(x, y) in positions else self.SPACE)
            raw_image.append(''.join(row))
        return '\n'.join(raw_image)


class Stars:

    def __init__(self, points):
        self.points = points

    @classmethod
    def from_string(cls, text):
        points = Points()
        for line in text.splitlines():
            if match := re.fullmatch(
                    r'position=<(?P<position_x>.*), (?P<position_y>.*)> velocity=<(?P<velocity_x>.*), (?P<velocity_y>.*)>',
                    line,
            ):
                position = Coords(int(match.group('position_x')), int(match.group('position_y')))
                velocity = Coords(int(match.group('velocity_x')), int(match.group('velocity_y')))
                points.append(Point(position, velocity))
            else:
                raise Exception
        return cls(points)

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls.from_string(f.read())

    def align(self, yield_image=False):
        iteration = 0
        points = self.points
        while True:
            next_points = Points()
            for point in points:
                next_position = point.position + point.velocity
                next_points.append(Point(position=next_position, velocity=point.velocity))
            if next_points.area > points.area:
                if not yield_image:
                    yield points.image()
                return iteration
            if yield_image:
                yield next_points.image()
            else:
                yield
            points = next_points
            iteration += 1


def main():
    stars = Stars.read_file()
    iter_align = stars.align()
    message = None
    try:
        while True:
            message = next(iter_align)
    except StopIteration as e:
        number_of_seconds = e.value
    print('Message:')
    print(message)
    print(f'Number of seconds:', number_of_seconds)


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
