from .data import GameObject

class Item(GameObject):
    def __init__(self, item, hp = 0, mana= 0, att = 0, df = 0):
        super().__init__(item)
        self.hp = hp
        self.mana = mana
        self.att = att
        self.df = df
        self.attribut = None

    def __str__(self):
        pres = f"{self.name} : {self.hp} hp / {self.mana} mana / {self.att} attack / {self.df} defense."
        return pres

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
    def from_dict(data):
        item_type = data["type"]
        if item_type == "Eatable":
            return Eatable(data["name"], hp = data["hp"], attribut = data["attribut"], mana = data["mana"], att = data["att"], df = data["df"])
        elif item_type == "Wearable":
            item = Wearable(data["name"], hp = data["hp"],  mana = data["mana"], att = data["att"], df = data["df"])
            item.attribut = data["attribut"]
            return item
        else:
            item = Item(data["name"], hp=data["hp"], mana=data["mana"], att=data["att"], df=data["df"])
            item.attribut = data["attribut"]
            return item


class Eatable(Item) :
    def __init__(self, name, attribut='normal', hp = 0, mana= 0, att = 0, df = 0):
        super().__init__(name, hp = hp, mana= mana, att = att, df = df)
        self.attribut = attribut

    def __str__(self):
        return super().__str__() + f" Type : {self.attribut}."

    def use(self, ply):
        if self.attribut == 'adaptive' :
            ply.hp += (self.hp * int(ply.maxhp * 0.3))
            ply.mana += (self.mana * int(ply.maxma * 0.3))
        else :
            ply.hp += self.hp
            ply.mana += self.mana
            ply.att += self.att
            ply.df += self.df
        if ply.hp > ply.maxhp: ply.hp = ply.maxhp
        if ply.mana > ply.maxma: ply.mana = ply.maxma

class Wearable(Item) :
    def __init__(self, name, hp=0, mana=0, att=0, df=0):
        super().__init__(name, hp=hp, mana=mana, att=att, df=df)
        self.attribut = False

    def __str__(self):
        return super().__str__() + f" {"Worn" if self.attribut else "Not worn"}."

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