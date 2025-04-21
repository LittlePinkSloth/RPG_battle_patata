class GameObject :
    def __init__(self, name):
        self.name = name

class RPGException(BaseException) :
    pass

class LoadingError(RPGException) :
    def __init__(self):
        print(self.__str__())

    def __str__(self):
        return "We were unable to load your file. You'll start a new game."

class NoSavedGame(LoadingError) :
    def __init__(self):
        print(self.__str__())
    def __str__(self):
        return "No saved game in the save/ directory. You'll start a new game."

class ItemNotFound(RPGException) :
    def __str__(self, item = ''):
        return f"You do not have this item ({item}) in your inventory."

class ToMuchWearable(RPGException) :
    def __init__(self):
        from ..game.display import bprint
        bprint(self.__str__())
    def __str__(self):
        return "You can only wear 5 items at one time, please unequip something before."

class DeadCharacter(RPGException) :
    def __init__(self, char) :
        self.dead = char

    def __str__(self):
        from .characters import Player
        if isinstance(self.dead, Player) :
            return "Sorry, you died. Heroically, but still... You're dead."
        else :
            return f"{self.dead.name} enemy died. You won."

    def __repr__(self):
        return self.__str__()