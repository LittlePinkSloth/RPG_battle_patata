from .game.engine import *

def start_game():
    clear_console()
    player = openning()
    print(f"Welcome to our dungeon, {player.name}, proud {player.__class__.__name__}!")
    wait_key()
    clear_console()

    try:
        game_loop(player)
    except DeadCharacter:
        pass

    print("This is the end of the game. We hope you had fun.")

