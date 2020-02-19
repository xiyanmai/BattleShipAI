import sys
from BattleShip.src import game
import random

if __name__ == '__main__':
 #   if len(sys.argv) < 3:
 #       print('Not enough arguments given.')
 #   else:
 #       random.seed(int(sys.argv[2])
 #       game_of_battle_ship = game.Game(sys.argv[1])
 #       game_of_battle_ship.play()

# Changed back to the above once done

    file = "BattleShip/configs/mini_game.txt"
    game_of_battle_ship = game.Game(file)
    game_of_battle_ship.play()