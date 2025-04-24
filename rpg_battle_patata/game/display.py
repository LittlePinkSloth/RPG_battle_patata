from colorama import Fore, Style
from rpg_battle_patata.game.language_manager import display_dict

def pprint(color : str, end='\n') :
    """Closure that return a function to color the printed strings.

    :param color: can be RED GREEN BLUE YELLOW CYAN MAGENTA
    :param end: same as the print() end argument
    :return: a function that takes in arg the string you want to print in color
    """
    def inner(txt) :
        match color :
            case 'RED' :
                print(Fore.RED + Style.BRIGHT+ txt + Style.RESET_ALL, end = end)
            case 'BLUE' :
                print(Fore.BLUE + Style.BRIGHT + txt + Style.RESET_ALL, end = end)
            case 'GREEN' :
                print(Fore.GREEN + txt + Style.RESET_ALL, end = end)
            case 'YELLOW' :
                print(Fore.YELLOW + txt + Style.RESET_ALL, end = end)
            case 'CYAN' :
                print(Fore.CYAN + txt + Style.RESET_ALL, end = end)
            case 'MAGENTA' :
                print(Fore.MAGENTA + txt + Style.RESET_ALL, end = end)
            case _ :
                print(Fore.WHITE + txt + Style.RESET_ALL, end = end)

    return inner

rprint = pprint('RED')
bprint = pprint('BLUE')
nprint = pprint('GREEN')
uprint = pprint('YELLOW')
vprint = pprint('MAGENTA')
dprint = pprint('default')

def display_big_message(message, color=Fore.RED):
    border = "*" * (len(message) + 6)
    print(color + border)
    print(f"*  {message}  *")
    print(border + Style.RESET_ALL)

def display_stats(ply, adv) :
    nbchar = len(adv.__str__()) if len(adv.__str__()) > len(ply.__str__()) else len(ply.__str__())
    boss = 'Boss' in adv.name or 'Elite' in adv.name

    up = " ." + (4+nbchar)*"_" + "."
    sply = "|  " + ply.__str__() + (nbchar - len(ply.__str__()) + 2)*" " + "|"
    sadv = "|  " + adv.__str__() + (nbchar - len(adv.__str__()) + 2)*" " + "|"
    bot = "|" + (5+nbchar-1)*"_" + "|"

    print(up)
    bprint(sply)
    vprint(sadv) if boss else rprint(sadv)
    print(bot)

def display_msg(msg, is_player : int | bool = -1) :
    """
    is_player: -1 : regular, 0/False : red, 1/True : blue, 2 : yellow
    :param msg: string to print
    :param is_player: -1 : regular, 1 : yellow, True : blue, False : red
    :return: nothing
    """
    if is_player == -1:
        print(msg)
    elif is_player == 2 :
        uprint(msg)
    elif is_player == 3 :
        nprint(msg)
    elif not is_player :
        rprint(msg)
    else :
        bprint(msg)

def display_msgs(*msgs, is_player : int|bool =-1) :
    for msg in msgs :
        display_msg(msg, is_player)

def display_list(li, msg : None | str = None) :
    if msg : print(msg)
    for i, v in enumerate(li) :
        print(f"|   {i+1} - {v}")
    return li

def wait_for_input(li, zero = False) :
    #si zero alors on autorise la valeur 0 pour faire une action spécifique
    msg = display_dict["wait_for_input.zero"] if zero else '--> '
    choice = input(msg)
    match = [str(i) for i in range(len(li)+1)] if zero else [str(i+1) for i in range(len(li))]
    while choice not in match :
        choice = input('--> ')
    return int(choice) - 1

def display_player_turn(li) :
    print("." + 3 * "_" + display_dict["display_player_turn.turn"] + 3 * "_")
    return display_list(li)

def display_eny_turn(*msgs) :
    display_msg("\n" + "." + 3 * "_" + display_dict["display_eny_turn.turn"] + 3 * "_", False)
    for msg in msgs :
        display_msg(f"|   {msg}", False)
    from rpg_battle_patata.game.utils import wait_key
    wait_key()