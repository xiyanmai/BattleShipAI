import sys
from BattleShip.src import game

if __name__ == '__main__':
#    if len(sys.argv) < 2:
#        print('Not enough arguments given.')
#    else:
#        game_of_battle_ship = game.Game(sys.argv[1])
#        game_of_battle_ship.play()

    file = "BattleShip/configs/mini_game.txt"
    game_of_battle_ship = game.Game(file)
    game_of_battle_ship.play()