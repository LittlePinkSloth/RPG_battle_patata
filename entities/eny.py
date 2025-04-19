import random
from ..entities.characters import Character
from ..data.ambiance import *
from ..game.utils import rprint


class Eny(Character) :
    def __init__(self, hp=20, att=2, df=2, strengh='normal', common_name = '', **kwargs):
        self.name = self.name_gen()
        if strengh == 'elite' :
            hp += hp * 0.5
            att += att * 0.5
            df += df * 0.5
            self.name += ' Elite'
        elif strengh == 'boss':
            hp *= 2
            att *= 2
            df *= 2
            self.name = 'Boss ' + self.name
        elif common_name == '' :
            hp /= 2
            att /= 2
            df /= 2
        super().__init__(name=self.name, maxhp=hp, att=att, df=df)
        self.strengh = strengh
        self.common_name = common_name if common_name else self.set_common_name()
        if common_name == '' :
            self.definition = 'just a ' + self.common_name.lower() + '.'

    def __str__(self):
        pres = f"{self.name} : {self.hp}/{self.maxhp} HP | {self.att} ATK | {self.df} DEF | Strengh : {self.strengh} | Type : {self.common_name}"
        return pres

    @staticmethod
    def name_gen():
        f = random.randint(0, len(char_names) - 1)
        a = random.randint(0, len(char_adjectives) - 1)
        return char_adjectives[a] + ' ' + char_names[f]

    @staticmethod
    def set_common_name():
        i = random.randint(0, len(eny_random_type)-1)
        return eny_random_type[i]

    def myturn(self, adv):
        self.is_alive()
        self.attack_target(adv)


class EnyOldMan(Eny) :
    def __init__(self, hp, att, df, strengh='normal', **kwargs):
        self.common_name = 'Old man'
        self.definition = "An old man bothered by your presence. He sometimes forgot things."
        super().__init__(hp = hp-2, att = att, df = df*0, strengh=strengh, common_name=self.common_name)

    def myturn(self, adv):
        self.is_alive()
        i = self.dice()
        if i < 3 :
            rprint(f"{self.name} forgot of your presence and does nothing.")
        else :
            self.attack_target(adv)

class EnyRageDog(Eny) :
    def __init__(self, hp, att, df, strengh='normal', **kwargs):
        self.common_name = 'Rage dog'
        self.definition = "A strange dog with white slobber. It can attack twice, be carefull."
        super().__init__(hp=hp, att=att+1, df=df-1, strengh=strengh, common_name=self.common_name)

    def myturn(self, adv):
        self.is_alive()
        i = self.dice()
        self.attack_target(adv)
        if i > 4 :
            rprint(f"{self.name} bites again !")
            self.attack_target(adv)


ENEMY_CLASSES = {
    "EnyRageDog": EnyRageDog,
    "EnyOldMan": EnyOldMan,
    "Eny": Eny
}