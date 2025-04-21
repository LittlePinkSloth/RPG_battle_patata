from ..game.utils import file_paths
from .rpg_exceptions import ItemNotFound, GameObject

class Item(GameObject):
    def __init__(self, item, hp = 0, mana= 0, att = 0, df = 0, **kwargs):
        super().__init__(item)
        self.hp = hp
        self.mana = mana
        self.att = att
        self.df = df
        self.attribut = None #attribut is polymorphe and highly depends of item's class

    def __str__(self):
        pres = f"{self.name} : {self.hp} hp / {self.mana} mana / {self.att} attack / {self.df} defense."
        return pres

    def __repr__(self):
        return f"{self.name} / class : {self.__class__.__name__} / attribut : {self.attribut}"

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "hp": self.hp,
            "mana": self.mana,
            "att": self.att,
            "df": self.df,
            "attribut": self.attribut
        }

    @staticmethod
    def from_dict(data) :
        item_type = data["type"]
        item_class = ITEM_CLASSES[item_type]
        if item_type not in ITEM_CLASSES:
            raise ItemNotFound(item_type)
        item_attributes = {k: v for k, v in data.items() if k != "type"}
        return item_class(**item_attributes)


class AntiStatus(Item) :
    def __init__(self, name, **kwargs) :
        super().__init__(name)
        self.attribut = self.set_attribut()

    def __str__(self):
        return f"{self.name} used to cure {self.attribut}."

    def set_attribut(self):
        from rpg_battle_patata.game.events import load_datas
        status = load_datas(file_paths['status'])['status_table']
        for stat in status :
            if stat['item'] == self.name.lower() : return stat['status']

    def use(self, ply):
        if ply.status == self.attribut :
            ply.status = None
            return f"You're not suffering {self.attribut} anymore."
        else :
            return f"It does nothing because you aren't suffering {self.attribut}."


class Eatable(Item) :
    def __init__(self, name, attribut='normal', hp = 0, mana= 0, att = 0, df = 0, **kwargs):
        super().__init__(name, hp = hp, mana= mana, att = att, df = df)
        self.attribut = attribut

    def __str__(self):
        return super().__str__() + f" Type : {self.attribut}."

    def use(self, ply):
        if self.attribut == 'adaptive' :
            ply.hp += int(ply.maxhp * 0.3)
            ply.mana += int(ply.maxma * 0.3)
        else :
            ply.hp += self.hp
            ply.mana += self.mana
            ply.att += self.att
            ply.df += self.df
        if ply.hp > ply.maxhp: ply.hp = ply.maxhp
        if ply.mana > ply.maxma: ply.mana = ply.maxma

class Wearable(Item) :
    def __init__(self, hp=0, mana=0, att=0, df=0, attribut = False, **kwargs):
        self.name = self.name_gen()
        super().__init__(self.name, hp=hp, mana=mana, att=att, df=df)
        self.attribut = attribut #if true, item Worn

    def __str__(self):
        return super().__str__() + f" {'Worn' if self.attribut else 'Not worn'}."

    @staticmethod
    def name_gen():
        import random
        from rpg_battle_patata.data.ambiance import item_adjectives, equipable_items
        adj = random.randint(0, len(item_adjectives) - 1)
        obj = random.randint(0, len(equipable_items) - 1)
        name = item_adjectives[adj] + ' ' + equipable_items[obj]
        return name

    def use(self, ply):
        if not self.attribut :
            self.attribut = True
            ply.maxhp += self.hp
            ply.hp += self.hp
            ply.maxma += self.mana
            ply.mana += self.mana
            ply.att += self.att
            ply.df += self.df
        else :
            self.attribut = False
            ply.maxhp -= self.hp
            ply.hp -= self.hp
            ply.maxma -= self.mana
            ply.mana -= self.mana
            ply.att -= self.att
            ply.df -= self.df


ITEM_CLASSES = {
    "Eatable": Eatable,
    "Wearable": Wearable,
    "AntiStatus": AntiStatus,
    "Item" : Item
}

