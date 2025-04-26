import os.path
from ..entities.eny import *
from ..entities.items import *
from genericpath import exists
from rpg_battle_patata.game.language_manager import events_dict, storytelling, items_dict, status_dict
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
    available_eny = [entry for entry in eny_data['enemies'] if ply.lvl >= entry["min_level"]]
    chosen_class = random.choices(available_eny, weights=[e["weight"] for e in available_eny])[0]
    eny_class = ENEMY_CLASSES[chosen_class['class']]

    if eny_strh["message"]:
        display_big_message(events_dict[eny_strh["message"]], Fore.MAGENTA)
        wait_key()

    return eny_class(hp = hp, att=att, df=df, strengh = eny_strh["strengh"])

def enemy_encounter(eny) :
    num = random.randint(0, len(storytelling["eny_meeting"])-1)
    story = storytelling["eny_meeting"][num]
    loc_vars = {"eny.name" : eny.name, "eny.definition" : eny.definition,"story" : story }
    return replace_variables(events_dict["eny_encounter"], loc_vars)


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
        return AntiStatus(status_dict[chosen['item']].capitalize())
    elif item_type < 6 :
        chosen = random.choices(items["items"], weights=[e["weight"] for e in items["items"]])[0]
        item_stats = {
            k: stats_table[k] if k in stats_table else v
            for k, v in chosen.items()
        }
        item_stats["name"] = items_dict[chosen["name"]]
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
    ns = random.randint(0, len(storytelling["chest_discovery"])-1)
    message = storytelling["chest_discovery"][ns]
    list_choices = events_dict["chest.list_choices"]
    choice = wait_for_input(display_list(list_choices, message))
    if choice == 0 : return events_dict["chest.no"], -1

    msg = events_dict["chest.try"]
    inside = ply.dice()
    if inside == 1 :
        hp = int(ply.maxhp*0.3)
        return msg + replace_variables(events_dict["chest.trap"],{"ply.take_damage(hp)" : ply.take_damage(hp)}), False
    elif inside == 2 :
        return msg + events_dict["chest.empty"], 2
    elif inside < 6 :
        it = item_generator(ply)
        ply.add_item(it)
        return msg + replace_variables(events_dict["chest.inside_1"], {"it.name" : it.name}), 2
    else :
        it = item_generator(ply)
        it1 = item_generator(ply)
        ply.add_item(it)
        ply.add_item(it1)
        return msg + replace_variables(events_dict["chest.inside_2"], {"it.name" : it.name, "it1.name" : it1.name}), 2


def fire_camp(ply) :
    fire = random.randint(0, len(storytelling["safe_room"])-1)
    message = storytelling["safe_room"][fire] + events_dict["fire_camp.nap"]
    list_choices = events_dict["fire_camp.list_choices"]
    choice = wait_for_input(display_list(list_choices, message))

    match choice :
        case 1 :
            return events_dict["fire_camp.no"], -1
        case 0 :
            ply.hp += int(ply.maxhp/2)
            if ply.hp > ply.maxhp : ply.hp = ply.maxhp
            ply.mana += int(ply.maxma/2)
            if ply.mana > ply.maxma : ply.mana = ply.maxma
            loc_vars = {"ply.hp" : ply.hp, "ply.maxhp" : ply.maxhp, "ply.mana" : ply.mana, "ply.maxma" :ply.maxma }
            return replace_variables(events_dict["fire_camp.rest"], loc_vars), 1
        case 2 :
            try :
                dirs = file_paths['save']
                if not exists(dirs):
                    os.mkdir(dirs)
                file = dirs  + "ignore_" + ply.name + ".json"
                ok = save_game(ply.to_dict(), file)
                if ok : return events_dict["fire_camp.save"], -1
            except Exception as e :
               return replace_variables(events_dict["fire_camp.error"], {"e" : e})
        case 3 :
            choice = wait_for_input(display_list(ply.inventory), True)
            if choice == -1 :
                return fire_camp(ply)
            try :
                item = ply.inventory[choice]
                return ply.use_item(item), True
            except IndexError :
                return events_dict["fire_camp.wrong"], -1
        case _ :
            return events_dict["fire_camp.wrong"], -1


