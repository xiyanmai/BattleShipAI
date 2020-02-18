from . import move, player

class HumanPlayer(object):

    @classmethod
    def get_move(cls, maker: "player.Player"):
        while True:
            coords = input(f'{maker.name}, enter the location you want to fire at in the form row, column: ')
            try:
                firing_location = move.Move.from_str(maker, coords)
            except ValueError as e:
                print(e)
                continue
            return firing_location
