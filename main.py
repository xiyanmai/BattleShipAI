import sys
from BattleShip.src import game



if __name__ == '__main__':
    seed = None
    if len(sys.argv) < 2:
        print('Not enough arguments given.')

    else:
        if len(sys.argv) > 2:
           seed = int(sys.argv[2])
        game_of_battle_ship = game.Game(sys.argv[1], seed)
        game_of_battle_ship.play()

# Changed back to the above once done

 #   file = "BattleShip/configs/mini_game.txt"
 #   game_of_battle_ship = game.Game(file, '4')
 #   game_of_battle_ship.play()