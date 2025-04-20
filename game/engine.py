from .utils import *
from ..entities.characters import *
from .events import event_generator

def openning() :
    print("Welcome to the wonderful game RPG battle patata. You will explore an infinite dungeon full of dangers.\nDo you want to load a game, or start a new one ?")
    nprint("1 : Load a game\n2 : Start a new one")
    rep = input("--> ")
    while rep not in ['1', '2'] :
        rep = input("--> ")

    if rep == '2' :
        return chose_player()
    else :
        #print("To load a game, the game file need to be a '.json'. You need to write exactly were this file is (the full path to it, including the file name and the .json extension), otherwise, it will bug and you'll juste start a new game.")
        print("Here are the saved games available. Please chose one to load.")
        choice = ''
        abspath = os.path.abspath(file_paths['save'])
        try :
            if not os.path.exists(abspath) : raise LoadingError
        except LoadingError :
            print("No 'save' dir in your game directory. Please create one or start a new game.")
            exit()
        list_file = os.listdir(abspath)
        if len(list_file) == 0 :
            print("No game saved. You'll start a new one.")
            return chose_player()

        for i, fl in enumerate(list_file) :
            print(f"{i+1} : {fl}")
            choice = input("--> ")
            while choice not in [str(x+1) for x in range(len(list_file))] :
                choice = input("--> ")
        try :
            pathfile = os.path.join(abspath, list_file[int(choice) - 1])
            data = load_datas(pathfile)
            if isinstance(data, bool) : raise LoadingError
            ply = Player.from_dict(data)
            print("Character successfully loaded. Have fun :).")
            return ply
        except LoadingError :
            print("We were unable to load your file.")
            return chose_player()
        except Exception as e :
            print(
                f"Sorry something went wrong. For now, no specific error management has been done, because I don't know what to expect.\nThis error is : {e}.")
            return chose_player()

def chose_player() :
    nprint("What is your name ?")
    name = input("--> ").strip()
    while len(name) == 0 :
        name = input("--> ").strip()
    print(f"\nHello {name}. What kind of player are you ?\n")
    nprint(f"  1 : {Baker.definition}\n  2 : {NarcissicPerverse.definition}\n  3 : {Gambler.definition}\n")
    choice = input("--> ")
    while choice not in ['1', '2', '3'] :
        choice = input("--> ")

    match choice :
        case '1' :
            return Baker(name)
        case '2' :
            return NarcissicPerverse(name)
        case '3' :
            return Gambler(name)

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