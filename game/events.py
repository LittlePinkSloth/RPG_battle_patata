import msvcrt, os, json
from .characters import *
from .items import *
from genericpath import exists
from .data import *

ENEMY_STRH_TABLE = [
    {"strengh": 'normal', "weight": 75, "min_level": 1, "message": None},
    {"strengh": 'elite', "weight": 15, "min_level": 2,
     "message": "An elite warrior stands in your way!"},
    {"strengh": 'boss', "weight": 10, "min_level": 3,
     "message": "⚠️ A terrifying boss emerges from the shadows..."}
]

ENEMY_TABLE = [
    {'class': EnyOldMan, "weight": 10},
    {'class': EnyRageDog, "weight": 10}
]

def save_game(player : Player, filename="save/savegame.json") -> bool :
    try :
        with open(filename, "w") as f:
            json.dump(player.to_dict(), f, indent=4)
            return True
    except OSError as e:  # Spécifie une exception liée au système

        print("The file could not be opened:", os.strerror(e.errno))
        return False
    except Exception as e:
        print(f"Erreur ({type(e).__name__}) :", str(e))
        return False

def load_game(filename="savegame.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return Player.from_dict(data)
    except FileNotFoundError:
        print(
            "Sorry, we were unable to find your file. Do you want to try again ?\n1 : try again\n2 : start a new game")
        rep = input("--> ")
        while rep not in ['1', '2']:
            rep = input("--> ")

        if rep == '1':
            return openning()
        else:
            return chose_player()


    except OSError as e:  # Spécifie une exception liée au système

        print("The file could not be opened:", os.strerror(e.errno))
    except Exception as e:
        print(f"Erreur ({type(e).__name__}) :", str(e))



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

def enemy_generator(ply) :
    hp = int(random.randint(0, 5) + ply.lvl * 7)
    att = int(random.randint(0, 1) + ply.lvl * 1.5)
    df = int(random.randint(0, 1) + ply.lvl * 1.5)

    available_strh = [entry for entry in ENEMY_STRH_TABLE if ply.lvl >= entry["min_level"]]
    chosen_strh = random.choices(available_strh, weights=[e["weight"] for e in available_strh])[0]

    chosen_class = random.choices(ENEMY_TABLE, weights=[e["weight"] for e in ENEMY_TABLE])[0]

    if chosen_strh["message"]:
        display_big_message(chosen_strh["message"], Fore.MAGENTA)
        wait_key()

    return chosen_class["class"](hp, att, df, chosen_strh["strengh"])


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
        list_file = os.listdir('save')
        if len(list_file) == 0 :
            print("No game saved. You'll start a new one.")
            return chose_player()

        for i, fl in enumerate(list_file) :
            print(f"{i+1} : {fl}")
            choice = input("--> ")
            while choice not in [str(x+1) for x in range(len(list_file))] :
                choice = input("--> ")
        try :

            file = 'save/' + list_file[int(choice) - 1]
            #file = file.replace('"','')
            ply = load_game(file)
            print("Character successfully loaded. Have fun :).")
            return ply

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

def wait_key() :
    print("--> ")
    msvcrt.getch()  # Attend n'importe quelle touche, sans besoin d'appuyer sur Entrée

def clear_console() :
    os.system('cls' if os.name == 'nt' else 'clear')

def enemy_encounter(eny) :
    num = random.randint(0, len(meeting)-1)
    rprint(f"{meeting[num]} \nIt's {eny.name}! \nIt can be defined by : {eny.definition} You have to fight for your life !")
    wait_key()
    clear_console()

def item_generator(ply) :
    item_type = ply.dice()
    hp = random.randint(0, (4 + int(ply.lvl * 1.2)))
    mana = random.randint(0, (2 + int(ply.lvl * 1.2)))
    att = random.randint(0, (int(ply.lvl * 1.1)))
    df = random.randint(0, (int(ply.lvl * 1.1)))

    EATABLE_ITEM_TABLE = [
        {'item': Eatable('Health potion', hp=hp), 'weight': 1},
        {'item': Eatable('Adaptive Health potion', attribut='adaptive'), 'weight': 1},
        {'item': Eatable('Mana potion', mana=mana), 'weight': 1},
        {'item': Eatable('Adaptive Mana potion', attribut='adaptive'), 'weight': 1},
        {'item': Eatable('Bread and cheese', hp=hp, mana=mana), 'weight': 1}
    ]

    STATUS_ITEM_TABLE = [
        {'name': it['item'].capitalize(), 'weight': it['weight']} for it in STATUS_TABLE
    ]

    if item_type == 1 :
        chosen = random.choices(STATUS_ITEM_TABLE, weights=[e["weight"] for e in STATUS_ITEM_TABLE])[0]
        return AntiStatus(chosen['name'])
    elif item_type < 6 :
        chosen = random.choices(EATABLE_ITEM_TABLE, weights=[e["weight"] for e in EATABLE_ITEM_TABLE])[0]
        return chosen['item']
    else :
        nba = random.randint(0, len(item_adjectives) - 1)
        nbo = random.randint(0, len(equipable_items) - 1)
        name = item_adjectives[nba] + ' ' + equipable_items[nbo]
        return Wearable(name, hp, mana, att, df)

def item_generator_old(ply) :
    item_type = ply.dice()
    hp = random.randint(0,(4 + int(ply.lvl*1.2)))
    mana = random.randint(0,(2 + int(ply.lvl*1.2)))
    att = random.randint(0,(int(ply.lvl*1.1)))
    df = random.randint(0,(int(ply.lvl*1.1)))

    if item_type < 6 :
        match item_type :
            case 1 :
                return Eatable('Health potion', hp = hp)
            case 2 :
                return Eatable('Adaptive Health potion', attribut ='adaptive')
            case 3 :
                return Eatable('Mana potion', mana=mana)
            case 4 :
                return Eatable('Adaptive Mana potion', attribut='adaptive')
            case 5 :
                return Eatable('Bread and cheese', hp = hp, mana = mana)
    else :
        nba = random.randint(0, len(item_adjectives)-1)
        nbo = random.randint(0, len(equipable_items)-1)
        name = item_adjectives[nba] + ' ' + equipable_items[nbo]
        return Wearable(name, hp, mana, att, df)

def chest(ply) :
    ns = random.randint(0, len(chest_discovery)-1)
    print(chest_discovery[ns])
    nprint("You can let it alone (1), or open it (2).")
    op = input("--> ")
    while op not in ['1', '2'] :
        op = input("--> ")
    if op == '1' : return print("You go ahead in the dungeon without touching the chest.")
    print("You try to open it...")
    inside = ply.dice()
    if inside == 1 :
        hp = int(ply.maxhp*0.3)
        rprint(f"It was trapped. You lose {ply.take_damage(hp)} hp.")
    elif inside == 2 :
        uprint(f"The chest is empty...")
    elif inside < 6 :
        it = item_generator(ply)
        uprint(f"A {it.name} was in the chest. It's now in your inventory")
        ply.add_item(it)
    else :
        it = item_generator(ply)
        it1 = item_generator(ply)
        uprint(f"Lucky day ! The chest was full of objects ! You found {it.name} and {it1.name} !")
        ply.add_item(it)
        ply.add_item(it1)

def fire_camp(ply) :
    fire = random.randint(0, len(safe_room)-1)
    print(safe_room[fire])
    nprint("Do you want to take a nap ?\n1 : yes\n2 : no ! I'm not a child.\n3 : I prefer to save the game !\n4 : I'd like to check my inventory.")
    heal = input("--> ")
    while heal not in ['1', '2', '3', '4'] :
        heal = input("--> ")

    match heal :
        case '2' :
            return print("Ok ok, no need to shout out... So, you can continue.")
        case '1' :
            ply.hp += int(ply.maxhp/2)
            if ply.hp > ply.maxhp : ply.hp = ply.maxhp
            ply.mana += int(ply.maxma/2)
            if ply.mana > ply.maxma : ply.mana = ply.maxma
            uprint(f"You rested sucessfully. You feel better : {ply.hp}/{ply.maxhp} hp, {ply.mana}/{ply.maxma} mana.")
        case '3' :
            try :
                file = "save/" + ply.name + ".json"
                if not exists("save"):
                    os.mkdir("save")
                ok = save_game(ply, file)
                if ok : print("Game successfully saved. You can continue !")
            except Exception as e :
                print(f"Sorry smt went wrong. For now, no specific error management has been done, because I don't know what to expect.\nThis error is : {e}.")
        case '4' :
            print(ply.get_inventory())
            while True:
                choice = input("Witch item to use ? 0 to use nothing.\n --> ")
                if not choice.isdigit(): continue
                if choice == '0':
                    break
                try:
                    item = ply.inventory[int(choice) - 1]
                    ply.use_item(item)
                    break
                except IndexError:
                    continue
        case _ :
            return "It seems something went wrong, so you just continue your adventure in the dungeon."


EVENT_TABLE = [
    {'event' : chest, 'weight' : 10},
    {'event' : fire_camp, 'weight' : 10},
    {'event' : enemy_generator, 'weight' : 40}
]

def event_generator(ply) :
    event = random.choices(EVENT_TABLE, weights=[e["weight"] for e in EVENT_TABLE])[0]

    eny = event['event'](ply)
    if eny :
        enemy_encounter(eny)
        return eny
    else :
        wait_key()
        return False