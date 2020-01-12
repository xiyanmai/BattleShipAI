from typing import Set
from . import ship_placement, orientation, game_config


class Board(object):

    def __init__(self, config:game_config.GameConfig, blank_char: str = '*') -> None:
        super().__init__()
        self.contents = [[blank_char] * config.num_cols for _ in range(config.num_rows)]
        self.blank_space = blank_char
        self.hit_marker = 'X'
        self.miss_marker = 'O'

    @property
    def num_rows(self) -> int:
        return len(self.contents)

    @property
    def num_cols(self) -> int:
        return len(self.contents[0])

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols

    def place_ship(self, placement: ship_placement.ShipPlacement) -> None:
        direction = 'horizontally' if placement.orientation == orientation.Orientation.HORIZONTAL else 'vertically'
        if not self.in_bounds(placement.row_start, placement.col_start):
            raise ValueError(f'Cannot {placement.ship.name} {direction} at {placement.row_start}, {placement.col_start}'
                             f' because it would be out of bounds.')
        elif not self.in_bounds(placement.row_end, placement.col_end):
            raise ValueError(f'Cannot {placement.ship.name} {direction} at {placement.row_start}, {placement.col_start}'
                             f' because it would end up out of bounds.')

        overlapping_ships = sorted(self.get_overlapping_ships(placement))
        if overlapping_ships:
            raise ValueError(f'Cannot {placement.ship.name} {direction} at {placement.row_start}, {placement.col_start}'
                             f' because it would overlap with {overlapping_ships}')

        # actually add the ship
        for row in range(placement.row_start, placement.row_end + 1):
            for col in range(placement.col_start, placement.col_end + 1):
                self.contents[row][col] = placement.ship.name

    def get_overlapping_ships(self, placement: ship_placement.ShipPlacement) -> Set[str]:
        overlapping_ships: Set[str] = set()
        for row in range(placement.row_start, placement.row_end + 1):
            for col in range(placement.col_start, placement.col_end + 1):
                if self.contains_ship(row, col):
                    overlapping_ships.add(self.contents[row][col])
        return overlapping_ships

    def contains_ship(self, row: int, col: int) -> bool:
        return self.contents[row][col] not in (self.blank_space, self.hit_marker, self.miss_marker)
