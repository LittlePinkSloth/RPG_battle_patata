from colorama import Fore, Style
import json, os, random, sys
from ..data.ambiance import meeting

file_paths = {
    'enemies' : 'rpg_battle_patata/data/ENEMY_TABLE.json',
'events' : 'rpg_battle_patata/data/EVENT_TABLE.json',
'items' : 'rpg_battle_patata/data/ITEM_TABLE.json',
'status' : 'rpg_battle_patata/data/STATUS_TABLE.json',
'save' : 'rpg_battle_patata/save/',
}

class GameObject :
    def __init__(self, name):
        self.name = name

class LoadingError(Exception) :
    pass

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

def enemy_encounter(eny) :
    num = random.randint(0, len(meeting)-1)
    rprint(f"{meeting[num]} \nIt's {eny.name}! \nIt can be defined by : {eny.definition} You have to fight for your life !")
    wait_key()
    clear_console()

def wait_key():
    if sys.platform == "win32":
        print("--> ")
        import msvcrt
        msvcrt.getch()
    else:
        input("Appuyez sur Entrée pour continuer...")


def clear_console() :
    os.system('cls' if os.name == 'nt' else 'clear')

def display_big_message(message, color=Fore.RED):
    border = "*" * (len(message) + 6)
    print(color + border)
    print(f"*  {message}  *")
    print(border + Style.RESET_ALL)


def save_game(dict_ply, filename) -> bool:
    try:
        with open(filename, "w") as f:
            json.dump(dict_ply, f, indent=4)
            return True
    except OSError as e:  # Spécifie une exception liée au système

        print("The file could not be opened:", os.strerror(e.errno))
        return False
    except Exception as e:
        print(f"Erreur ({type(e).__name__}) :", str(e))
        return False

def load_datas(pathfile) : #fusion avec load_game
    try:
        with open(pathfile, "r",  encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        print("Sorry, we were unable to find your file.")
        return False

    except OSError as e:  # Spécifie une exception liée au système
        print("The file could not be opened:", os.strerror(e.errno))
        return False

    except Exception as e:
        print(f"Erreur ({type(e).__name__}) :", str(e))
        return False
