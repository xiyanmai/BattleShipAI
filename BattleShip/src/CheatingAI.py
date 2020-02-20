from . import move, player
import random

class CheatingAI(object):
    @classmethod
    def get_move(cls, maker):
        r = 0
        for row in maker.opponents[0].board.contents:
            for c in range(0, len(row)):
                if row[c].content not in ['X', 'O', '*'] and not row[c].has_been_fired_at:
                    coords = f'{r},{c}'
                    try:
                        firing_location = move.Move.from_str(maker, coords)
                    except ValueError:
                        pass
                    return firing_location
            r += 1