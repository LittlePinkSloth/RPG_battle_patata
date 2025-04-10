from .data import GameObject

class Item(GameObject):
    def __init__(self, item, hp = 0, mana= 0, att = 0, df = 0):
        super().__init__(item)
        self.hp = hp
        self.mana = mana
        self.att = att
        self.df = df

    def __str__(self):
        pres = f"{self.name} : {self.hp} hp / {self.mana} mana / {self.att} attack / {self.df} defense."
        return pres


class Eatable(Item) :
    def __init__(self, name, kind='normal', hp = 0, mana= 0, att = 0, df = 0):
        super().__init__(name, hp = hp, mana= mana, att = att, df = df)
        self.kind = kind

    def __str__(self):
        return super().__str__() + f" Type : {self.kind}."

    def use(self, ply):
        if self.kind == 'adaptive' :
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
        self.worn = False

    def __str__(self):
        return super().__str__() + f" {"Worn" if self.worn else "Not worn"}."

    def use(self, ply):
        if not self.worn :
            self.worn = True
            ply.maxhp += self.hp
            ply.hp += self.hp
            ply.maxma += self.mana
            ply.mana += self.mana
            ply.att += self.att
            ply.df += self.df
        else :
            self.worn = False
            ply.maxhp -= self.hp
            ply.hp -= self.hp
            ply.maxma -= self.mana
            ply.mana -= self.mana
            ply.att -= self.att
            ply.df -= self.df