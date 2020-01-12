from . import game_config, player


class Game(object):

    def __init__(self, game_config_file: str, num_players: int = 2) -> None:
        super().__init__()
        self.game_config = game_config.GameConfig(game_config_file)
        self.players = []
        self.player_turn = 0

    def setup_players(self, num_players: int) -> None:
        for player_num in range(num_players):
            self.players.append(player.Player(self.game_config, self.players))

    def play(self) -> None:
        while not self.game_is_over():
            self.display_gamestate()
            cur_player = self.get_active_player()
            move = cur_player.get_move()
            move.make()

    @property
    def num_players(self) -> int:
        return len(self.players)

    def get_active_player(self) -> player.Player:
        return self.players[self.player_turn]

    def game_is_over(self) -> bool:
        return any(player_.all_ships_sunk() for player_ in self.players)

    def display_gamestate(self)->None:
        pass
