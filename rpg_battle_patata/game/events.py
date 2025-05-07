import os.path
from ..entities.eny import *
from ..entities.items import *
from genericpath import exists
from .utils import *
from .display import *
from rpg_battle_patata.game.language_manager import get_dict

def buff_generator(duration : int = -1, strengh : int = 1) :
    status_dict = get_dict("status_dict")
    buff_datas = load_datas(file_paths['status'])['status_table']
    buff_table = [b for b in buff_datas if b['type'] == 1]
    chosen = random.choices(buff_table, weights=[b['weight'] for b in buff_table])[0]
    return Status(status_dict[chosen['status']], once = True, reversible=True, duration=duration, strengh=strengh)

def enemy_generator(ply) :
    events_dict = get_dict('events_dict')
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
    if eny_strh["message"] :
        msg = events_dict[eny_strh["message"]]
    else :
        msg = 0

    return eny_class(hp = hp, att=att, df=df, strengh = eny_strh["strengh"]), msg

def enemy_encounter(eny) :
    storytelling = get_dict("storytelling")
    events_dict = get_dict("events_dict")
    num = random.randint(0, len(storytelling["eny_meeting"])-1)
    story = storytelling["eny_meeting"][num]
    loc_vars = {"eny.name" : eny.name, "eny.definition" : eny.definition,"story" : story }
    return replace_variables(events_dict["eny_encounter"], loc_vars)


def item_generator(ply) :
    #initiliazing item stats
    item_type = ply.dice()
    hp = random.randint(0, (4 + int(ply.lvl * 1.2)))
    mana = random.randint(0, (2 + int(ply.lvl * 1.2)))

    stats_table = {"hp": hp, "mana": mana}

    #loading dictionnary from json files
    items = load_datas(file_paths['items'])
    status = load_datas(file_paths['status'])
    status_dict = get_dict("status_dict")
    items_dict = get_dict("items_dict")

    if item_type == 1 :
        chosen = random.choices(status['status_table'], weights=[e["weight"] for e in status['status_table']])[0]
        if chosen['type'] :
            return BuffingItem(status_dict[chosen['item']].capitalize())
        else :
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
        att = random.randint(0, (int(ply.lvl * 1.1)))
        df = random.randint(0, (int(ply.lvl * 1.1)))
        return Wearable(hp=hp, mana=mana, att=att, df=df)

def generate_event_type(ply) :
    events = load_datas(file_paths['events'])
    event_avail = [e for e in events['events'] if e['min_level'] <= ply.lvl]
    event = random.choices(event_avail, weights=[e["weight"] for e in event_avail])[0]
    return event

def event_generator(ply) :
    event = generate_event_type(ply)
    ev = event_correspondance[event['event']]
    if event['event'] == "enemy_generator" :
        eny, msg = ev(ply)
        if msg : display_big_message(msg, Fore.MAGENTA)
    else :
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

def resolve_chest_event(ply) :
    storytelling = get_dict("storytelling")
    events_dict = get_dict("events_dict")
    ns = random.randint(0, len(storytelling["chest_discovery"]) - 1)
    message = storytelling["chest_discovery"][ns]
    list_choices = events_dict["chest.list_choices"]
    choice = wait_for_input(display_list(list_choices, message))
    if choice == 0: return events_dict["chest.no"], -1
    else : return chest(ply)

def chest(ply) :
    events_dict = get_dict("events_dict")
    stats_dict = get_dict("stats_dict")
    msg = events_dict["chest.try"]

    inside = ply.dice()
    if inside == 1 :
        hp = int(ply.maxhp*0.3)
        return msg + replace_variables(events_dict["chest.trap"],{"ply.take_damage(hp)" : ply.take_damage(hp), "{hp.full}" : stats_dict["hp.full"]}), False
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

def rest(ply) :
    events_dict = get_dict("events_dict")
    ply.hp += int(ply.maxhp / 2)
    if ply.hp > ply.maxhp: ply.hp = ply.maxhp
    ply.mana += int(ply.maxma / 2)
    if ply.mana > ply.maxma: ply.mana = ply.maxma
    loc_vars = {"ply.hp": ply.hp, "ply.maxhp": ply.maxhp, "ply.mana": ply.mana, "ply.maxma": ply.maxma}
    return replace_variables(events_dict["fire_camp.rest"], loc_vars), 1

def fire_camp(ply) :
    storytelling = get_dict("storytelling")
    events_dict = get_dict("events_dict")
    fire = random.randint(0, len(storytelling["safe_room"])-1)
    message = storytelling["safe_room"][fire] + events_dict["fire_camp.nap"]
    list_choices = events_dict["fire_camp.list_choices"]
    choice = wait_for_input(display_list(list_choices, message))

    match choice :
        case 1 :
            return events_dict["fire_camp.no"], -1
        case 0 :
            return rest(ply)
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

def place_generator(ply) :
    events_dict = get_dict("events_dict")
    place = random.randint(0,len(events_dict["place_generator.place"])-1)
    name = events_dict["place_generator.place"][place]
    match place :
        case 0:
            duration = random.randint(4,6)
            stat = buff_generator(duration,random.randint(1,2))
            ply.set_status(stat)
            loc_vars = {"stat.name" : stat.name, "name" : name, "duration" : duration}
            return replace_variables(events_dict["place_generator.blessing"], loc_vars), 1
        case 1 :
            malus = [m for m in ply.status if m.buff == 0]
            for m in malus :
                ply.cure_status(m)
            return events_dict["place_generator.healing"], 1
        case 2 :
            malus = [m for m in ply.status if m.buff == 0]
            for m in malus:
                if m.duration >= 0 :
                    m.duration += 3
            return events_dict["place_generator.cursed"], 0
        case _ :
            return events_dict["place_generator.wrong"] + " place_generator", -1

def magic_places(ply) :
    events_dict = get_dict("events_dict")
    storytelling = get_dict("storytelling")
    story = random.choices(storytelling['magic_place'])[0]
    choices = events_dict["magic_places.choices"]
    choice = wait_for_input(display_list(choices, story))
    match choice :
        case 0 :
            return place_generator(ply)
        case 1 :
            return events_dict["magic_places.no"], -1
        case _ :
            return events_dict["place_generator.wrong"] + " magic_places", -1

event_correspondance = {"chest" : resolve_chest_event, "fire_camp" : fire_camp, "enemy_generator" : enemy_generator, "magic_places" : magic_places}
