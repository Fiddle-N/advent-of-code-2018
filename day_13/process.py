import collections
import dataclasses
import enum
import timeit
import typing


class Directions(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def turn_left(self):
        return Directions((self.value - 1) % len(Directions))

    def turn_right(self):
        return Directions((self.value + 1) % len(Directions))

    def opposite(self):
        return Directions((self.value + (len(Directions) // 2)) % len(Directions))


class RawGridPieces(enum.Enum):
    TRACK_UP_DOWN = "|"
    TRACK_LEFT_RIGHT = "-"
    TRACK_FORWARD_DIAGONAL = "/"
    TRACK_BACKWARD_DIAGONAL = "\\"
    TRACK_INTERSECTION = "+"

    CART_UP = "^"
    CART_RIGHT = ">"
    CART_DOWN = "v"
    CART_LEFT = "<"

    EMPTY = " "


@dataclasses.dataclass(frozen=True)
class GridPieceDetails:
    is_vertical: bool = False
    is_horizontal: bool = False
    is_cart: bool = False


GRID_PIECE_DETAILS = {
    RawGridPieces.TRACK_UP_DOWN: GridPieceDetails(is_vertical=True),
    RawGridPieces.TRACK_LEFT_RIGHT: GridPieceDetails(is_horizontal=True),
    RawGridPieces.TRACK_FORWARD_DIAGONAL: GridPieceDetails(
        is_vertical=True, is_horizontal=True
    ),
    RawGridPieces.TRACK_BACKWARD_DIAGONAL: GridPieceDetails(
        is_vertical=True, is_horizontal=True
    ),
    RawGridPieces.TRACK_INTERSECTION: GridPieceDetails(
        is_vertical=True, is_horizontal=True
    ),
    RawGridPieces.CART_UP: GridPieceDetails(is_vertical=True, is_cart=True),
    RawGridPieces.CART_RIGHT: GridPieceDetails(is_horizontal=True, is_cart=True),
    RawGridPieces.CART_DOWN: GridPieceDetails(is_vertical=True, is_cart=True),
    RawGridPieces.CART_LEFT: GridPieceDetails(is_horizontal=True, is_cart=True),
}


class CartIntersectionDirections(enum.Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

    def next(self):
        return CartIntersectionDirections(
            (self.value + 1) % len(CartIntersectionDirections)
        )


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coords(self.x - other.x, self.y - other.y)


class Cart:
    def __init__(self, cart_direction, previous_location):
        self.cart_direction = cart_direction
        self.previous_location = previous_location
        self.intersection_direction = CartIntersectionDirections.LEFT


CART_DIRECTIONS = {
    RawGridPieces.CART_UP: Directions.UP,
    RawGridPieces.CART_RIGHT: Directions.RIGHT,
    RawGridPieces.CART_DOWN: Directions.DOWN,
    RawGridPieces.CART_LEFT: Directions.LEFT,
}


DIRECTION_COORDS = {
    Directions.UP: Coords(0, -1),
    Directions.RIGHT: Coords(1, 0),
    Directions.DOWN: Coords(0, 1),
    Directions.LEFT: Coords(-1, 0),
}


@dataclasses.dataclass()
class TrackPiece:

    location: Coords
    adj_track: dict[Directions, Coords]
    cart: typing.Optional[Cart]

    @property
    def is_intersection(self):
        return len(self.adj_track) == 4

    def next_coords(self, prev_coords=None, direction=None):
        if self.is_intersection and direction is None:
            raise Exception("Direction must be specified for intersections")
        if not self.is_intersection and prev_coords is None:
            raise Exception(
                "Previous coordinates must be specified for non-intersections"
            )
        if not self.is_intersection:
            next_locations = {
                adj_track_direction: direction_coord
                for adj_track_direction, direction_coord in self.adj_track.items()
                if direction.opposite() != adj_track_direction
            }
            assert len(next_locations) == 1
            (next_location,) = next_locations.items()
            return next_location
        else:
            return direction, self.location + DIRECTION_COORDS[direction]


class MineCartMadness:
    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read().rstrip())

    def __init__(self, raw_track):
        raw_grid = raw_track.splitlines()
        self.nrows = len(raw_grid)
        self.ncols = len(raw_grid[0])

        self.grid = collections.defaultdict(lambda: RawGridPieces.EMPTY)
        for row_no, row in enumerate(raw_track.splitlines()):
            for col_no, track_piece in enumerate(row):
                self.grid[Coords(col_no, row_no)] = RawGridPieces(track_piece)

        self.track = self._create_track()

    def _create_track(self):
        track = {}

        left_right_track = {
            grid_piece
            for grid_piece, details in GRID_PIECE_DETAILS.items()
            if details.is_horizontal
        }

        up_down_track = {
            grid_piece
            for grid_piece, details in GRID_PIECE_DETAILS.items()
            if details.is_vertical
        }

        for row_no in range(self.nrows):
            for col_no in range(self.ncols):
                track_position = Coords(col_no, row_no)
                track_piece = self.grid[track_position]

                if track_piece == RawGridPieces.EMPTY:
                    continue
                adj_positions = self._surrounding_coords(track_position)
                populated_adj_positions = {
                    direction: direction_coords
                    for direction, direction_coords in adj_positions.items()
                    if self.grid[direction_coords] != RawGridPieces.EMPTY
                }

                adj_track = None
                cart = None

                grid_piece_detail = GRID_PIECE_DETAILS[track_piece]

                if (
                    grid_piece_detail.is_vertical
                    and not grid_piece_detail.is_horizontal
                ):
                    adj_track = {
                        Directions.UP: populated_adj_positions[Directions.UP],
                        Directions.DOWN: populated_adj_positions[Directions.DOWN],
                    }

                if (
                    grid_piece_detail.is_horizontal
                    and not grid_piece_detail.is_vertical
                ):
                    adj_track = {
                        Directions.LEFT: populated_adj_positions[Directions.LEFT],
                        Directions.RIGHT: populated_adj_positions[Directions.RIGHT],
                    }

                if grid_piece_detail.is_cart:
                    cart_direction = CART_DIRECTIONS[track_piece]
                    previous_cart_location = (
                        track_position + DIRECTION_COORDS[cart_direction.opposite()]
                    )
                    cart = Cart(cart_direction, previous_cart_location)

                if track_piece == RawGridPieces.TRACK_FORWARD_DIAGONAL:
                    is_left_up = (
                        Directions.LEFT in populated_adj_positions
                        and self.grid[populated_adj_positions[Directions.LEFT]]
                        in left_right_track
                        and Directions.UP in populated_adj_positions
                        and self.grid[populated_adj_positions[Directions.UP]]
                        in up_down_track
                    )
                    is_right_down = (
                        Directions.RIGHT in populated_adj_positions
                        and self.grid[populated_adj_positions[Directions.RIGHT]]
                        in left_right_track
                        and Directions.DOWN in populated_adj_positions
                        and self.grid[populated_adj_positions[Directions.DOWN]]
                        in up_down_track
                    )
                    assert is_left_up != is_right_down
                    if is_left_up:
                        adj_track = {
                            Directions.LEFT: populated_adj_positions[Directions.LEFT],
                            Directions.UP: populated_adj_positions[Directions.UP],
                        }
                    elif is_right_down:
                        adj_track = {
                            Directions.RIGHT: populated_adj_positions[Directions.RIGHT],
                            Directions.DOWN: populated_adj_positions[Directions.DOWN],
                        }
                    else:
                        raise Exception
                if track_piece == RawGridPieces.TRACK_BACKWARD_DIAGONAL:
                    is_left_down = (
                        Directions.LEFT in populated_adj_positions
                        and self.grid[populated_adj_positions[Directions.LEFT]]
                        in left_right_track
                        and Directions.DOWN in populated_adj_positions
                        and self.grid[populated_adj_positions[Directions.DOWN]]
                        in up_down_track
                    )
                    is_right_up = (
                        Directions.RIGHT in populated_adj_positions
                        and self.grid[populated_adj_positions[Directions.RIGHT]]
                        in left_right_track
                        and Directions.UP in populated_adj_positions
                        and self.grid[populated_adj_positions[Directions.UP]]
                        in up_down_track
                    )
                    assert is_left_down != is_right_up
                    if is_left_down:
                        adj_track = {
                            Directions.LEFT: populated_adj_positions[Directions.LEFT],
                            Directions.DOWN: populated_adj_positions[Directions.DOWN],
                        }
                    elif is_right_up:
                        adj_track = {
                            Directions.RIGHT: populated_adj_positions[Directions.RIGHT],
                            Directions.UP: populated_adj_positions[Directions.UP],
                        }
                    else:
                        raise Exception
                if track_piece == RawGridPieces.TRACK_INTERSECTION:
                    adj_track = populated_adj_positions.copy()
                track[track_position] = TrackPiece(track_position, adj_track, cart)
        return track

    def _surrounding_coords(self, coords: Coords):
        surrounding_coords = {}
        for direction, direction_coord in DIRECTION_COORDS.items():
            new_x = coords.x + direction_coord.x
            new_y = coords.y + direction_coord.y
            if 0 <= new_x < self.ncols and 0 <= new_y < self.nrows:
                surrounding_coords[direction] = Coords(new_x, new_y)
            else:
                # out of bounds
                continue
        return surrounding_coords

    def __iter__(self):
        while True:
            carts_on_track = {
                track_location: track_piece
                for track_location, track_piece in self.track.items()
                if track_piece.cart
            }
            if len(carts_on_track) == 1:
                for track_location, track_piece in carts_on_track.items():
                    if track_piece.cart is not None:
                        return track_location
            for track_location, track_piece in carts_on_track.items():
                cart: typing.Optional[Cart] = track_piece.cart
                if cart is None:
                    # there was a cart here previously on this tick but not anymore
                    continue
                track_piece = self.track[track_location]
                if track_piece.is_intersection:
                    if cart.intersection_direction == CartIntersectionDirections.LEFT:
                        cart_direction = cart.cart_direction.turn_left()
                    elif (
                        cart.intersection_direction == CartIntersectionDirections.RIGHT
                    ):
                        cart_direction = cart.cart_direction.turn_right()
                    elif (
                        cart.intersection_direction
                        == CartIntersectionDirections.STRAIGHT
                    ):
                        cart_direction = cart.cart_direction
                    else:
                        raise Exception("unexpected direction")
                    cart_direction, next_track_location = track_piece.next_coords(
                        direction=cart_direction,
                    )
                    cart.intersection_direction = cart.intersection_direction.next()
                else:
                    cart_direction, next_track_location = track_piece.next_coords(
                        prev_coords=cart.previous_location,
                        direction=cart.cart_direction,
                    )

                track_piece.cart = None

                cart.cart_direction = cart_direction
                cart.previous_location = track_location

                next_track_piece = self.track[next_track_location]

                if next_track_piece.cart is not None:
                    # crash
                    yield next_track_location
                    next_track_piece.cart = None
                else:
                    next_track_piece.cart = cart


def main():
    mine_cart_madness = MineCartMadness.read_file()
    mine_cart_madness_iter = iter(mine_cart_madness)
    crash = next(mine_cart_madness_iter)
    print(f"location of first crash: {crash.x},{crash.y}")
    while True:
        try:
            next(mine_cart_madness_iter)
        except StopIteration as e:
            last_cart = e.value
            break
    print(f"location of last cart: {last_cart.x},{last_cart.y}")


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
