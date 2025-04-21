import os.path
from ..entities.eny import *
from ..entities.items import *
from genericpath import exists
from ..data.ambiance import *
from .utils import *
from .display import *


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

def event_generator(ply) :
    events = load_datas(file_paths['events'])
    event = random.choices(events['events'], weights=[e["weight"] for e in events['events']])[0]

    event_correspondance = {"chest" : chest, "fire_camp" : fire_camp, "enemy_generator" : enemy_generator}
    ev = event_correspondance[event['event']]

    eny = ev(ply)
    if isinstance(eny, Character) :
        display_msg(enemy_encounter(eny), False)
        wait_key()
        clear_console()
        return eny
    else :
        display_msg(*eny)
        wait_key()
        return False

def chest(ply) :
    ns = random.randint(0, len(chest_discovery)-1)
    message = chest_discovery[ns]
    list_choices = ['Well... I prefer to let it alone', 'Of course I open it !']
    choice = wait_for_input(display_list(list_choices, message))
    if choice == 0 : return "You go ahead in the dungeon without touching the chest.", -1

    msg = "You try to open it...\n"
    inside = ply.dice()
    if inside == 1 :
        hp = int(ply.maxhp*0.3)
        return msg + f"It was trapped. You lose {ply.take_damage(hp)} hp.", False
    elif inside == 2 :
        return msg + f"The chest is empty...", 2
    elif inside < 6 :
        it = item_generator(ply)
        ply.add_item(it)
        return msg + f"{it.name} was in the chest. It's now in your inventory", 2
    else :
        it = item_generator(ply)
        it1 = item_generator(ply)
        ply.add_item(it)
        ply.add_item(it1)
        return msg + f"Lucky day ! The chest was full of objects ! You found {it.name} and {it1.name} !", 2


def fire_camp(ply) :
    fire = random.randint(0, len(safe_room)-1)
    message = safe_room[fire] + "\n" + "Do you want to take a nap ?"
    list_choices = ["Why not, this place looks good !","Never ! I'm not a child.", "I prefer to save the game !", "I'd like to check my inventory."]
    choice = wait_for_input(display_list(list_choices, message))

    match choice :
        case 1 :
            return "Ok ok, no need to shout out... So, you can continue.", -1
        case 0 :
            ply.hp += int(ply.maxhp/2)
            if ply.hp > ply.maxhp : ply.hp = ply.maxhp
            ply.mana += int(ply.maxma/2)
            if ply.mana > ply.maxma : ply.mana = ply.maxma
            return f"You rested sucessfully. You feel better : {ply.hp}/{ply.maxhp} hp, {ply.mana}/{ply.maxma} mana.", 1
        case 2 :
            try :
                dirs = file_paths['save']
                if not exists(dirs):
                    os.mkdir(dirs)
                file = dirs  + "ignore_" + ply.name + ".json"
                ok = save_game(ply.to_dict(), file)
                if ok : return "Game successfully saved. You can continue !", -1
            except Exception as e :
               return f"Sorry smt went wrong. For now, no specific error management has been done, because I don't know what to expect.\nThis error is : {e}."
        case 3 :
            choice = wait_for_input(display_list(ply.inventory), True)
            if choice == -1 :
                return fire_camp(ply)
            try :
                item = ply.inventory[choice]
                return ply.use_item(item), True
            except IndexError :
                return "It seems something went wrong, so you just continue your adventure in the dungeon.", -1
        case _ :
            return "It seems something went wrong, so you just continue your adventure in the dungeon.", -1


