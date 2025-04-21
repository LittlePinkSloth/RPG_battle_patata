from .utils import *
from ..entities.characters import *
from .events import event_generator
from .display import display_msgs, display_msg, display_list, display_stats
from ..entities.rpg_exceptions import LoadingError, NoSavedGame

def openning() :
    message = "Welcome to the wonderful game RPG battle patata. You will explore an infinite dungeon full of dangers.\nDo you want to load a game, or start a new one ?"
    list_choices = ["Start a new game", "Load a game from save directory","Load a game from a custom path (please provide full path with the .json exention)"]
    choice = wait_for_input(display_list(list_choices, message))

    if choice == 0 :
        return chose_player()
    elif choice == 1 :
        path = file_paths['save']
        try :
            if not os.path.exists(path) :
                os.makedirs(path)
            list_choices = os.listdir(path)
            if len(list_choices) == 0 :
                raise NoSavedGame
        except NoSavedGame :
            return chose_player()

        message = "Here are the saved games available. Please chose one to load."
        choice = wait_for_input(display_list(list_choices, message), True)
        if choice == -1 :
            return openning()
        else :
            return load_game(os.path.join(path, list_choices[choice]))
    elif choice == 2 :
        path = input("Enter you save absolute path (including C:// and .json extension) : \n-->  ").replace('"','')
        return load_game(path)


def chose_player() :
    name = input("What is your name ?\n-->  ").strip()
    while len(name) == 0 :
        name = input("--> ").strip()
    message = f"\nHello {name}. What kind of player are you ?\n"
    list_choices = [f"{Baker.definition}",f"{NarcissicPerverse.definition}",f"{Gambler.definition}"]
    choice = wait_for_input(display_list(list_choices, message))

    match choice :
        case 0 :
            return Baker(name)
        case 1 :
            return NarcissicPerverse(name)
        case 2 :
            return Gambler(name)

def load_game(path) :
    try:
        if not os.path.exists(path) : raise LoadingError
        data = load_datas(path)
        if isinstance(data, bool): raise LoadingError
        return Player.from_dict(data)
    except LoadingError:
        return chose_player()
    except Exception as e:
        print(
            f"Sorry something went wrong. For now, no specific error management has been done, because I don't know what to expect.\nThis error is : {e} : {e.__str__()}.")
        return chose_player()

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
                if enemy_.name in dead.__str__() :
                    display_msgs(dead.__str__(), player.gain_xp(int(enemy_.maxhp/1.5)), is_player=True)
                    wait_key()
                    clear_console()
                else :
                    display_msg(dead.__str__(), False)
                break