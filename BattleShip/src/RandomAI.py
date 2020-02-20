from . import move, player
import random

class RandomAI(object):
    @classmethod
    def get_move(cls, maker):
        r, c = (random.choice(maker.possible_locations))
        coords = f'{r}, {c}'
        try:
            firing_location = move.Move.from_str(maker, coords)
            maker.possible_locations.remove((r, c))
        except ValueError:
            pass
        return firing_location