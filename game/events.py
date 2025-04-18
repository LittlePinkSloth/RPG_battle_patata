import os.path
from ..entities.characters import *
from ..entities.eny import *
from ..entities.items import *
from genericpath import exists
from ..data.ambiance import *
from .utils import *

def enemy_generator(ply) :
    #Eny stats management from player stats
    hp = random.randint(0, 5) + ply.lvl * 7
    att = random.randint(0, 1) + ply.lvl * 1.5
    df = random.randint(0, 1) + ply.lvl * 1.5

    #Strengh and eny class management from json file
    eny_data = load_datas(file_paths['enemies'])
    available_strh = [entry for entry in eny_data['strh'] if ply.lvl >= entry["min_level"]]
    eny_strh = random.choices(available_strh, weights=[e["weight"] for e in available_strh])[0]
    chosen_class = random.choices(eny_data['enemies'], weights=[e["weight"] for e in eny_data['enemies']])[0]
    eny_class = ENEMY_CLASSES[chosen_class['class']]

    if eny_strh["message"]:
        display_big_message(eny_strh["message"], Fore.MAGENTA)
        wait_key()

    return eny_class(hp, att, df, eny_strh["strengh"])

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



def enemy_encounter(eny) :
    num = random.randint(0, len(meeting)-1)
    rprint(f"{meeting[num]} \nIt's {eny.name}! \nIt can be defined by : {eny.definition} You have to fight for your life !")
    wait_key()
    clear_console()

def item_generator(ply) :
    #initiliazing item stats
    item_type = ply.dice()
    hp = random.randint(0, (4 + int(ply.lvl * 1.2)))
    mana = random.randint(0, (2 + int(ply.lvl * 1.2)))
    att = random.randint(0, (int(ply.lvl * 1.1)))
    df = random.randint(0, (int(ply.lvl * 1.1)))
    stats_table = {"hp": hp, "mana": mana, "att": att, "df": df}

    #loading dictionnary from json files
    items = load_datas(file_paths['items'])
    status = load_datas(file_paths['status'])

    if item_type == 1 :
        chosen = random.choices(status['status_table'], weights=[e["weight"] for e in status['status_table']])[0]
        return AntiStatus(chosen['item'].capitalize())
    elif item_type < 6 :
        chosen = random.choices(items["items"], weights=[e["weight"] for e in items["items"]])[0]
        item_stats = {
            k: stats_table[k] if k in stats_table else v
            for k, v in chosen.items()
        }
        it_class = ITEM_CLASSES[chosen["class"]]
        return it_class(**item_stats)

    else :
        return Wearable(hp=hp, mana=mana, att=att, df=df)



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
        uprint(f"{it.name} was in the chest. It's now in your inventory")
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
                dirs = file_paths['save']
                if not exists(dirs):
                    os.mkdir(dirs)
                file = dirs  + ply.name + ".json"
                ok = save_game(ply.to_dict(), file)
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


def event_generator(ply) :
    events = load_datas(file_paths['events'])
    event = random.choices(events['events'], weights=[e["weight"] for e in events['events']])[0]

    event_correspondance = {"chest" : chest, "fire_camp" : fire_camp, "enemy_generator" : enemy_generator}
    ev = event_correspondance[event['event']]

    eny = ev(ply)
    if eny :
        enemy_encounter(eny)
        return eny
    else :
        wait_key()
        return False