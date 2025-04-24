import json

language = {
    'English' : ('rpg_battle_patata/data/text_english.json', "Chose language"),
    'Français' : ('rpg_battle_patata/data/text_french.json', "Sélectionnez une langue"),
    'Español' : ('rpg_battle_patata/data/text_spanish.json', "Escoger una lengua")
}

def chose_langage() -> str :
    list_choices = [k for k in language.keys()]
    message = str([v[1] for k, v in language.items()]).replace(",", " - ").replace("[", "").replace("]", "")
    print(message)
    for i, v in enumerate(list_choices) :
        print(f"|   {i+1} - {v}")
    choice = input("--> ")
    while choice not in [str(i+1) for i in range(len(list_choices))] :
        choice = input('--> ')
    return language[list_choices[int(choice)-1]][0]

_dict = {}
storytelling = {}
items_dict =  {}
characters_dict = {}
eny_dict =  {}
display_dict =  {}
rpg_exceptions_dict = {}
events_dict =  {}
engine_dict =  {}
main_dict =  {}
status_dict =  {}

def load_langage(filepath) :
    global _dict, storytelling, items_dict, characters_dict, eny_dict, display_dict, rpg_exceptions_dict, events_dict, engine_dict, main_dict, status_dict
    with open(filepath, 'r', encoding='utf-8') as f:
        _dict = json.load(f)

    storytelling = _dict["storytelling"]
    items_dict = _dict["items_dict"]
    characters_dict = _dict["characters_dict"]
    eny_dict = _dict["eny_dict"]
    display_dict = _dict["display_dict"]
    rpg_exceptions_dict = _dict["rpg_exceptions_dict"]
    events_dict = _dict["events_dict"]
    engine_dict = _dict["engine_dict"]
    main_dict = _dict["main_dict"]
    status_dict = _dict["status_dict"]
