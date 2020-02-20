from . import move, player
from . import CheatingAI, SearchDestroyAI, RandomAI


class AIPlayer(object):
    @classmethod
    def get_move(cls, maker: "player.Player"):

        if maker.type.startswith('Cheating'):
            return CheatingAI.CheatingAI.get_move(maker)

        if maker.type.startswith('Random'):
            return RandomAI.RandomAI.get_move(maker)

        if maker.type.startswith('Search Destroy'):
            return SearchDestroyAI.SearchDestroyAI.get_move(maker)
