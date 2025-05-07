import json, os
from flask import session
from ..paths import DATA_DIR

language = {
    'English' : ('english', "Chose language"),
    'Français' : ('french', "Sélectionnez une langue"),
    'Español' : ('spanish', "Escoger una lengua")
}

_language_cache = {}

def get_current_language():
    try :
        return session.get('lang', 'english')
    except RuntimeError : #handle the error with the console mode and correctly returns the langage chosen by the user at the begining of the game
        for key in _language_cache.keys() :
            return key
        return 'english'

def get_dict(name):
    lang = get_current_language()
    if lang not in _language_cache:
        load_language(lang)
    return _language_cache[lang].get(name, {})

def load_language(lang):
    filepath = os.path.join(DATA_DIR, f"text_{lang}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    _language_cache[lang] = data


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

"""_dict = {}
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
webapp_dict =  {}

def load_langage(filepath) :
    global _dict, storytelling, items_dict, characters_dict, eny_dict, display_dict, rpg_exceptions_dict, events_dict, engine_dict, main_dict, status_dict, webapp_dict
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
    webapp_dict = _dict["webapp_dict"]"""

