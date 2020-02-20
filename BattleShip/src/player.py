from typing import Dict, List
import copy
from . import game, game_config, board, ship, orientation, ship_placement, move, HumanPlayer, AIPlayer
from .firing_location_error import FiringLocationError
import random


class Player(object):
    opponents: List["Player"]
    ships: Dict[str, ship.Ship]

    def __init__(self, player_num: int, config: game_config.GameConfig, other_players: List["Player"]) -> None:
        super().__init__()
        self.name = 'No Name'
        self.type = 'No Type'
        self.types = ['Human', 'CheatingAi', 'SearchDestroyAi', 'RandomAi']
        self.types_for_display = ['Human', 'Cheating Ai', 'Search Destroy AI', 'Random Ai']
        self.init_name(player_num, other_players)
        self.board = board.Board(config)
        self.opponents = other_players[:]  # a copy of other players
        self.ships = copy.deepcopy(config.available_ships)
        self.place_ships()
        self.destroy = []
        self.possible_locations = [(row, col) for row in range(self.board.num_rows) for col in range(self.board.num_cols)]

        # make this player the opponent of all the other players
        for opponent in other_players:
            opponent.add_opponent(self)

    def init_name(self, player_num: int, other_players: List["Player"]) -> None:
        #while True:
         #   self.name = input(f'Player {player_num} please enter your name: ').strip()
         #   if self in other_players:
         #       print(f'Someone is already using {self.name} for their name.\n'
         #             f'Please choose another name.')
         #   else:
         #       break
         # Can delete

        while True:
            self.name = input(f"Enter one of {self.types} for Player {player_num}'s type: ").strip()
            for type in self.types_for_display:
                if type.replace(" ", "").lower().startswith(self.name.lower()):
                    self.name = f'{type} {player_num}'
                    self.type = f'{type}'
                    if self.name.startswith('Human'):
                        self.type = 'Human'
                        self.name = input(f'Player {player_num} please enter your name: ').strip()
                    return None
            else:
                print('not valid')
                continue



    def add_opponent(self, opponent: "Player") -> None:
        self.opponents.append(opponent)

    def place_ships(self) -> None:

        if self.type.startswith('Human'):
            for ship_ in self.ships.values():
                self.display_placement_board()
                self.place_ship(ship_)
        else:
            for ship_ in self.ships.values():
                self.display_placement_board()
                self.ai_place_ship(ship_)

        self.display_placement_board()

    def place_ship(self, ship_: ship.Ship) -> None:
        while True:
            placement = self.get_ship_placement(ship_)
            try:
                self.board.place_ship(placement)
            except ValueError as e:
                print(e)
            else:
                return

    def ai_place_ship(self, ship_: ship.Ship) -> None:
        while True:
            placement = self.get_ai_ship_placement(ship_)
            try:
                self.board.ai_place_ship(placement)
            except ValueError:
                pass
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

    def get_ai_ship_placement(self, ship_: ship.Ship):
        while True:
            try:
                orientation_ = self.get_ai_orientation(ship_)
                start_row, start_col = self.get_ai_start_coords(orientation_, ship_)
            except ValueError:
                pass
            else:
                return ship_placement.ShipPlacement(ship_, orientation_, start_row, start_col)

    def get_orientation(self, ship_: ship.Ship) -> orientation.Orientation:
        orientation_ = input(
            f'{self.name} enter horizontal or vertical for the orientation of {ship_.name} '
            f'which is {ship_.length} long: ')
        return orientation.Orientation.from_string(orientation_)

    def get_ai_orientation(self, ship_: ship.Ship) -> orientation.Orientation:
        return orientation.Orientation.random_orientation()

    def get_start_coords(self, ship_: ship.Ship):

        coords = input(f'{self.name}, enter the starting position for your {ship_.name} ship '
                       f',which is {ship_.length} long, in the form row, column: ')
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
            col = int(col)
        except ValueError:
            raise ValueError(f'{col} is not a valid value for column.\n'
                             f'It should be an integer between 0 and {self.board.num_cols - 1}')

        return row, col

    def get_ai_start_coords(self, orientation, ship_: ship.Ship):
        if orientation.value == 'horizontal':
            row = random.randint(0, self.board.num_rows - 1)
            col = random.randint(0, self.board.num_cols - ship_.length)
            return row, col
        elif orientation.value == 'vertical':
            row = random.randint(0, self.board.num_rows - ship_.length)
            col = random.randint(0, self.board.num_cols - 1)
            return row, col

    def all_ships_sunk(self) -> bool:
        return all(ship_.health == 0 for ship_ in self.ships.values())

    def get_move(self) -> move.Move:
        if self.type.startswith('Human'):
            firing_location = HumanPlayer.HumanPlayer.get_move(self)
        else:
            firing_location = AIPlayer.AIPlayer.get_move(self)
        return firing_location


    def fire_at(self, row: int, col: int) -> None:
        opponent = self.opponents[0]
        if not opponent.board.coords_in_bounds(row, col):
            raise FiringLocationError(f'{row}, {col} '
                                      f'is not in bounds of our '
                                      f'{opponent.board.num_rows} X {opponent.board.num_cols} board.')
        elif opponent.board.has_been_fired_at(row, col):
            if self.type.startswith('Human'):
                raise FiringLocationError(f'You have already fired at {row}, {col}.')
            else:
                raise FiringLocationError()
        else:
            opponent.receive_fire_at(row, col)
            self.display_scanning_boards()
            self.display_firing_board()

    def receive_fire_at(self, row: int, col: int) -> None:
        location_fired_at = self.board.shoot(row, col)
        if location_fired_at.contains_ship():
            ship_hit = self.ships[location_fired_at.content]
            ship_hit.damage()
            print(f"You hit {self.name}'s {ship_hit}!")
            if self.opponents[0].type.startswith('Search Destroy'):
                self.destroy.extend(((row, col-1), (row-1, col), (row, col+1), (row+1, col)))
            if ship_hit.destroyed():
                print(f"You destroyed {self.name}'s {ship_hit}")
        else:
            print('Miss')


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False
        else:
            return self.name == other.name

    def __ne__(self, other: object) -> bool:
        return self != other

    def display_placement_board(self) -> None:
        print(f"{self.name}'s Placement Board")
        print(self.get_visible_representation_of_board(), end='')

    def display_scanning_boards(self) -> None:
        print(f"{self.name}'s Scanning Board")
        for opponent in self.opponents:
            print(opponent.get_hidden_representation_of_board(), end='')

    def display_firing_board(self) -> None:
        print(f"\n{self.name}'s Board")
        print(self.get_visible_representation_of_board())

    def get_hidden_representation_of_board(self) -> str:
        return self.board.get_display(hidden=True)

    def get_visible_representation_of_board(self) -> str:
        return self.board.get_display(hidden=False)

    def __str__(self) -> str:
        return self.name

