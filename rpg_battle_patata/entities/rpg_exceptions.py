#from rpg_battle_patata.game.language_manager import rpg_exceptions_dict
from rpg_battle_patata.game.language_manager import get_dict
from ..game.utils import replace_variables

class GameObject :
    def __init__(self, name):
        self.name = name

class RPGException(BaseException) :
    pass

class LoadingError(RPGException) :
    def __init__(self):
        print(self.__str__())

    def __str__(self):
        rpg_exceptions_dict = get_dict("rpg_exceptions_dict")
        return rpg_exceptions_dict["LoadingError.__str__"]

class NoSavedGame(LoadingError) :
    def __init__(self):
        print(self.__str__())
    def __str__(self):
        rpg_exceptions_dict = get_dict("rpg_exceptions_dict")
        return rpg_exceptions_dict["NoSavedGame.__str__"]

class ItemNotFound(RPGException) :
    def __str__(self):
        rpg_exceptions_dict = get_dict("rpg_exceptions_dict")
        return rpg_exceptions_dict["ItemNotFound.__str__"]

class ToMuchWearable(RPGException) :
    def __init__(self):
        from ..game.display import bprint
        bprint(self.__str__())
    def __str__(self):
        rpg_exceptions_dict = get_dict("rpg_exceptions_dict")
        return rpg_exceptions_dict["ToMuchWearable.__str__"]

class DeadCharacter(RPGException) :
    def __init__(self, char) :
        self.dead = char

    def __str__(self):
        from .characters import Player
        rpg_exceptions_dict = get_dict("rpg_exceptions_dict")
        if isinstance(self.dead, Player) :
            return rpg_exceptions_dict["DeadCharacter.__str__.player"]
        else :
            return replace_variables( rpg_exceptions_dict["DeadCharacter.__str__.eny"], {"self.dead.name" : self.dead.name})

    def __repr__(self):
        return self.__str__()