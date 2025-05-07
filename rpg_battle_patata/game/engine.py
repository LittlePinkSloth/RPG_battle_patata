from .utils import *
from ..entities.characters import *
from .events import event_generator
from .display import display_msgs, display_msg, display_list, display_stats, display_eny_turn
from ..entities.rpg_exceptions import LoadingError, NoSavedGame
from .language_manager import get_dict


def openning() :
    engine_dict = get_dict("engine_dict")
    message = engine_dict["openning.message"]
    list_choices = engine_dict["openning.list_choices"]
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

        message = engine_dict["openning.savedgame"]
        choice = wait_for_input(display_list(list_choices, message), True)
        if choice == -1 :
            return openning()
        else :
            return load_game(os.path.join(path, list_choices[choice]))
    elif choice == 2 :
        path = input(engine_dict["openning.loadfile"]).replace('"','')
        return load_game(path)


def chose_player() :
    engine_dict = get_dict("engine_dict")
    name = input(engine_dict["chose_player.name"]).strip()
    while len(name) == 0 :
        name = input("--> ").strip()
    message = replace_variables(engine_dict["chose_player.player"], {"name" : name})
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
    engine_dict = get_dict("engine_dict")
    try:
        if not os.path.exists(path) : raise LoadingError
        data = load_datas(path)
        if isinstance(data, bool): raise LoadingError
        return Player.from_dict(data)
    except LoadingError:
        return chose_player()
    except Exception as e:
        print(replace_variables(engine_dict["load_game.exception"], {"e":e}))
        return chose_player()

def game_loop(player):
    while player.is_alive():
        enemy_ = event_generator(player)
        while enemy_:
            try:
                display_stats(player, enemy_)
                if random.randint(0,1) :
                    player.myturn(enemy_)
                    display_eny_turn(*enemy_.myturn(player))
                else :
                    player.is_alive()
                    display_eny_turn(*enemy_.myturn(player))
                    print()
                    player.myturn(enemy_)
                    msg = enemy_.is_alive()
                    if isinstance(msg, str) :
                        display_msg(msg, False)
                    wait_key()
                clear_console()
            except DeadCharacter as dead:
                if enemy_.name in dead.__str__() :
                    display_msgs(dead.__str__(), player.gain_xp(enemy_), is_player=True)
                    wait_key()
                    clear_console()
                else :
                    display_msg(dead.__str__(), False)
                break