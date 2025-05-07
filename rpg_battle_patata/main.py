from .game.engine import openning, game_loop
from .game.utils import clear_console, replace_variables, wait_key
from .game.display import display_msg
from .entities.rpg_exceptions import DeadCharacter
from rpg_battle_patata.game.language_manager import get_dict


def start_game():
    main_dict = get_dict("main_dict")
    clear_console()
    player = openning()
    loc_vars = {"player.name" : player.name, "player.__class__.__name__" : player.class_name }
    display_msg(replace_variables(main_dict["start_game.welcome"], loc_vars))
    wait_key()
    clear_console()
    try :
        game_loop(player)
    except DeadCharacter :
        pass

    display_msg(main_dict["start_game.end"])

