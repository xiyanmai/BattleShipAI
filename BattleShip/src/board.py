from typing import Set, List
from . import ship_placement, orientation, game_config, cell
from .cell import Cell


class Board(object):
    empty_marker: str
    hit_marker: str
    miss_marker: str
    contents: List[List[Cell]]

    def __init__(self, config: game_config.GameConfig, empty_marker: str = '*') -> None:
        super().__init__()
        self.empty_marker = empty_marker
        self.hit_marker = 'X'
        self.miss_marker = 'O'
        self.contents = [
            [cell.Cell(self.empty_marker, self.empty_marker, self.hit_marker, self.miss_marker) for col in
             range(config.num_cols)]
            for row in range(config.num_rows)
        ]

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
                self.contents[row][col].content = placement.ship.name

    def get_overlapping_ships(self, placement: ship_placement.ShipPlacement) -> Set[str]:
        overlapping_ships: Set[str] = set()
        for row in range(placement.row_start, placement.row_end + 1):
            for col in range(placement.col_start, placement.col_end + 1):
                if self.contains_ship(row, col):
                    overlapping_ships.add(self.contents[row][col].content)
        return overlapping_ships

    def contains_ship(self, row: int, col: int) -> bool:
        return self.contents[row][col].contains_ship()

    def get_display(self, hidden: bool = False) -> str:
        # the amount of whitespace between each element should be
        # the number of characters that is in the largest dimension
        sep = ' ' * max((len(str(self.num_rows - 1)), len(str(self.num_cols - 1))))
        rep = sep * 2 + sep.join((str(headder) for headder in range(self.num_cols))) + '\n'
        for row_num, row in enumerate(self.contents):
            rep += str(row_num) + sep + sep.join(cell_.representation(hidden) for cell_ in row) + '\n'
        return rep
