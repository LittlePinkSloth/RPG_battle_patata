from .game.events import *

def game_loop(player):
    while player.is_alive():
        enemy_ = event_generator(player)
        while enemy_:
            try:
                display_stats(player, enemy_)
                if random.randint(0,1) :
                    player.myturn(enemy_)
                    enemy_.myturn(player)
                else :
                    enemy_.myturn(player)
                    print()
                    player.myturn(enemy_)
                    enemy_.is_alive()
                wait_key()
                clear_console()
            except DeadCharacter as dead:
                print(dead)
                if enemy_.name in str(dead):
                    player.gain_xp(int(enemy_.maxhp/1.5))
                    wait_key()
                    clear_console()
                break

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

