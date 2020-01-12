from typing import Dict, Tuple, Container

from . import game, game_config, board, ship, orientation, ship_placement, move
import BattleShip.src.ship


class Player(object):
    ships: Dict[str, ship.Ship]

    def __init__(self, config: game_config.GameConfig, other_players: Container["Player"]) -> None:
        super().__init__()
        self.name = 'No Name'
        self.init_name(other_players)
        self.board = board.Board(config)
        self.ships = dict(config.available_ships)
        self.place_ships()

    def init_name(self, other_players: Container["Player"]) -> None:
        while True:
            self.name = input('Please enter your name: ').strip()
            if self in other_players:
                print(f'Someone is already using {self.name} for their name.\n'
                      f'Please choose another name.')
            else:
                break

    def place_ships(self) -> None:
        for ship_ in self.ships.values():
            self.place_ship(ship_)

    def place_ship(self, ship_: ship.Ship) -> None:
        while True:
            placement = self.get_ship_placement(ship_)
            try:
                self.board.place_ship(placement)
            except ValueError as e:
                print(e)
            else:
                return

    def get_ship_placement(self, ship_: ship.Ship):
        while True:
            try:
                orientation_ = self.get_orientation(ship_)
                start_row, start_col = self.get_start_coords(ship_)
            except ValueError as e:
                print(e)
            else:
                return ship_placement.ShipPlacement(ship_, orientation_, start_row, start_col)

    def get_orientation(self, ship_: ship.Ship) -> orientation.Orientation:
        orientation_ = input(f'{self.name} enter horizontal or vertical for the orientation of {ship_.name}.')
        return orientation.Orientation.from_string(orientation_)

    def get_start_coords(self, ship_: ship.Ship):

        coords = input(f'{self.name}, enter the starting position for your {ship_.name} ship '
                       f'in the for row, column: ')
        try:
            row, col = coords.split(',')
        except ValueError:
            raise ValueError(f'{coords} is not in the form x,y')

        try:
            row = int(row)
        except ValueError:
            raise ValueError(f'{row} is not a valid value for row.\n'
                             f'It should be an integer between 0 and {self.board.num_rows - 1}')

        try:
            row = int(row)
        except ValueError:
            raise ValueError(f'{col} is not a valid value for column.\n'
                             f'It should be an integer between 0 and {self.board.num_cols - 1}')

        return row, col

    def all_ships_sunk(self) -> bool:
        return all(ship_.health == 0 for ship_ in self.ships.values())

    def get_move(self):
        coords = input('Enter the location you want to fire at in the form row,col: ')

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False
        else:
            return self.name == other.name

    def __ne__(self, other: object) -> bool:
        return self != other


