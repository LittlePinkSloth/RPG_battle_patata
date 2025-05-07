from ..game.utils import file_paths, replace_variables
from .rpg_exceptions import ItemNotFound, GameObject
#from rpg_battle_patata.game.language_manager import items_dict, status_dict, storytelling
import secrets
from rpg_battle_patata.game.language_manager import get_dict


class Item(GameObject):
    def __init__(self, item, hp = 0, mana= 0, att = 0, df = 0, attribut= None, **kwargs):
        super().__init__(item)
        self.hp = hp
        self.mana = mana
        self.att = att
        self.df = df
        self.attribut = attribut #attribut is polymorphe and highly depends of item's class
        self.loc_vars = {"self.attribut": self.attribut, "self.name" : self.name, "self.hp" : self.hp, "self.mana" : self.mana, "self.att" : self.att, "self.df" : self.df, }
        self.id = secrets.randbelow(1_000_000)

    def __str__(self):
        stats_dict = get_dict("stats_dict")
        if self.hp :
            hp = f"{str(self.hp)} {stats_dict['hp']}"
        else :
            hp = 0
        if self.mana :
            mana = f"{str(self.mana)} {stats_dict['mana']}"
        else :
            mana = 0
        if self.att :
            att = f"{str(self.att)} {stats_dict['att']}"
        else :
            att = 0
        if self.df :
            df = f"{str(self.df)} {stats_dict['df']}"
        else :
            df = 0
        
        pres = f"{self.name} : "
        before = False
        for val in [hp, mana,att,df] :
            if val :
                if before :
                    pres += " / " + val
                else :
                    before = True
                    pres += val

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
        self.name = name
        self.attribut = self.set_attribut()
        super().__init__(self.name, attribut=self.attribut)


    def __str__(self):
        items_dict = get_dict("items_dict")
        return f"{self.name} : {items_dict['AntiStatus.__str__']}{self.attribut}."

    def set_attribut(self):
        status_dict = get_dict("status_dict")
        from rpg_battle_patata.game.events import load_datas
        status = load_datas(file_paths['status'])['status_table']

        for stat in status :
            if status_dict[stat['item']].lower() == self.name.lower() : return status_dict[stat['status']]

    def use(self, ply):
        items_dict = get_dict("items_dict")
        to_cure = []
        for stat in ply.status :
            if stat.status == self.attribut :
                to_cure.append(stat)
        for stat in to_cure :
            ply.cure_status(stat)
        if len(to_cure)>0 : return replace_variables(items_dict["AntiStatus.use.ok"], self.loc_vars)
        else : return replace_variables(items_dict["AntiStatus.use.no"], self.loc_vars)

class BuffingItem(AntiStatus) :
    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.bonus = self.set_bonus()

    def __str__(self):
        items_dict = get_dict("items_dict")
        return f"{self.name} : {items_dict['BuffingItem.__str__']} {self.attribut}."

    def use(self, ply):
        items_dict = get_dict("items_dict")
        ply.set_status(self.create_status())
        return items_dict["BuffingItem.use"]

    def set_bonus(self):
        from rpg_battle_patata.game.events import load_datas
        status_table = load_datas(file_paths['status'])['status_table']

        for stat in status_table :
            status_dict = get_dict("status_dict")
            if status_dict[stat['status']] == self.attribut :
                return stat['effect']
        return "hp"

    def create_status(self):
        from .status import Status
        duration = 5
        strengh = 1
        once = True if self.bonus in ["att", "df", "luck", "maxhp", "maxma"] else False
        reversible = True if self.bonus in ["att", "df", "luck"] else False
        return Status(self.attribut, duration=duration, strengh=strengh, once=once, reversible=reversible)

class Eatable(Item) :
    def __init__(self, name, attribut='normal', hp = 0, mana= 0, att = 0, df = 0, **kwargs):
        self.attribut = attribut
        hpa = 1 if attribut=='adaptive' and hp else hp
        manaa = 1 if attribut=='adaptive' and mana else mana
        super().__init__(name, hp=hpa, mana=manaa, att=att, df=df, attribut = self.attribut)

    def use(self, ply):
        if self.attribut == 'adaptive' :
            ply.hp += int(ply.maxhp * 0.3 * self.hp)
            ply.mana += int(ply.maxma * 0.3 * self.mana)
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
        self.attribut = attribut  # if true, item Worn
        super().__init__(self.name, hp=hp, mana=mana, att=att, df=df, attribut=self.attribut)

    @staticmethod
    def name_gen():
        import random
        storytelling = get_dict("storytelling")
        adj = random.randint(0, len(storytelling["item_adjectives"]) - 1)
        obj = random.randint(0, len(storytelling["equipable_items"]) - 1)
        name = storytelling["item_adjectives"][adj] + ' ' + storytelling["equipable_items"][obj]
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
    "BuffingItem" : BuffingItem,
    "Item" : Item
}

