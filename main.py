from game.events import *

def game_loop(player):
    while player.is_alive():
        enemy_ = event_generator(player)
        while enemy_:
            try:
                display_stats(player, enemy_)
                player.myturn(enemy_)
                enemy_.myturn(player)
                wait_key()
                clear_console()
            except DeadCharacter as dead:
                print(dead)
                if enemy_.name in str(dead):
                    player.gain_xp(enemy_.maxhp)
                    wait_key()
                    clear_console()
                break

def main():
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

if __name__ == "__main__":
    main()
