from . import move, player
import random


class AIPlayer(object):
    @classmethod
    def get_move(cls, maker: "player.Player"):

        if maker.type.startswith('Cheating'):
            r = 0
            for row in maker.opponents[0].board.contents:
                for c in range(0,len(row)):
                    if row[c].content not in ['X', 'O', '*'] and not row[c].has_been_fired_at:
                        coords = f'{r},{c}'
                        try:
                            firing_location = move.Move.from_str(maker, coords)
                        except ValueError:
                            pass
                        return firing_location
                r += 1

        if maker.type.startswith('Random'):
            r, c =(random.choice(maker.possible_locations))
            coords = f'{r}, {c}'
            try:
                firing_location = move.Move.from_str(maker, coords)
                maker.possible_locations.remove((r, c))
            except ValueError:
                pass
            return firing_location

        if maker.type.startswith('Search Destroy'):
            try:
                r, c = maker.opponents[0].destroy[0]
                del maker.opponents[0].destroy[0]
                if (r, c) in maker.possible_locations:
                    maker.possible_locations.remove((r, c))

            except IndexError:
                r, c = (random.choice(maker.possible_locations))
                maker.possible_locations.remove((r, c))


            coords = f'{r}, {c}'
            try:
                firing_location = move.Move.from_str(maker, coords)
            except ValueError:
                pass
            return firing_location
