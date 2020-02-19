from . import move, player
import random

class AIPlayer(object):
    memory = None
    @classmethod
    def get_move(cls, maker: "player.Player"):

        global research
        if maker.name.startswith('Cheating'):
            r = 0
            for row in maker.opponents[0].board.contents:
                for c in range(0,len(row)):
                    if row[c].content not in ['X', 'O', '*'] and not row[c].has_been_fired_at:
                        coords = f'{r},{c}'
                        try:
                            firing_location = move.Move.from_str(maker, coords)
                        except ValueError as e:
                            print(e)
                        return firing_location
                r += 1

        if maker.name.startswith('Random'):
            r = random.randint(0, maker.opponents[0].board.num_rows - 1)
            c = random.randint(0, maker.opponents[0].board.num_cols - 1)
            coords = f'{r}, {c}'
            try:
                firing_location = move.Move.from_str(maker, coords)
            except ValueError as e:
                print(e)
            return firing_location

        if maker.name.startswith('Search Destroy'):
            while True:
                if not maker.opponents[0].hit_coords:
                    r = random.randint(0, maker.opponents[0].board.num_rows - 1)
                    c = random.randint(0, maker.opponents[0].board.num_cols - 1)

                else:
                    while True:
                        if maker.opponents[0].hit_coords[0][2] == 0:
                            r = maker.opponents[0].hit_coords[0][0]
                            c = maker.opponents[0].hit_coords[0][1] - 1

                        elif maker.opponents[0].hit_coords[0][2] == 1:
                            r = maker.opponents[0].hit_coords[0][0] + 1
                            c = maker.opponents[0].hit_coords[0][1]

                        elif maker.opponents[0].hit_coords[0][2] == 2:
                            r = maker.opponents[0].hit_coords[0][0]
                            c = maker.opponents[0].hit_coords[0][1] + 1

                        elif maker.opponents[0].hit_coords[0][2] == 3:
                            r = maker.opponents[0].hit_coords[0][0] - 1
                            c = maker.opponents[0].hit_coords[0][1]
                            del maker.opponents[0].hit_coords[0]

                        if r not in range(0, maker.opponents[0].board.num_rows) or c not in range(0, maker.opponents[0].board.num_cols - 1):
                            try:
                                maker.opponents[0].hit_coords[0][2] += 1
                                continue
                            except IndexError:
                                r = None
                                c = None
                                break
                        else:
                            break
                    try:
                        maker.opponents[0].hit_coords[0][2] += 1
                    except IndexError:
                        pass
                coords = f'{r}, {c}'
                try:
                    firing_location = move.Move.from_str(maker, coords)
                except ValueError as e:
                    print(e)

                return firing_location