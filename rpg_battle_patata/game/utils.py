import json, os, random, sys
from ..data.ambiance import meeting

#python -m rpg_battle_patata

file_paths = {
    'enemies' : 'rpg_battle_patata/data/ENEMY_TABLE.json',
    'events' : 'rpg_battle_patata/data/EVENT_TABLE.json',
    'items' : 'rpg_battle_patata/data/ITEM_TABLE.json',
    'status' : 'rpg_battle_patata/data/STATUS_TABLE.json',
    'save' : 'rpg_battle_patata/save/',
}

def enemy_encounter(eny) :
    num = random.randint(0, len(meeting)-1)
    return f"{meeting[num]} \nIt's {eny.name}! \nIt can be defined by : {eny.definition} You have to fight for your life !"

def wait_key():
    if sys.platform == "win32":
        #print("--> ")
        import msvcrt
        msvcrt.getch()
    else:
        input("Appuyez sur Entrée pour continuer...")

def clear_console() :
    os.system('cls' if os.name == 'nt' else 'clear')

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

