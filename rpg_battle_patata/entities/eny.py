import random
from ..entities.characters import Character
from ..game.display import display_eny_turn
from rpg_battle_patata.game.language_manager import eny_dict, storytelling
from ..game.utils import replace_variables

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
            self.definition = eny_dict["Eny.definition"] + self.common_name.lower() + '.'

    def __str__(self):
        pres = f"{self.name} : {self.hp}/{self.maxhp} HP | {self.att} ATK | {self.df} DEF | {eny_dict['Eny.__str__.strengh']} : {self.strengh} | Type : {self.common_name}"
        return pres

    @staticmethod
    def name_gen():
        f = random.randint(0, len(storytelling["char_names"]) - 1)
        a = random.randint(0, len(storytelling["char_adjectives"]) - 1)
        return storytelling["char_adjectives"][a] + ' ' + storytelling["char_names"][f]

    @staticmethod
    def set_common_name():
        i = random.randint(0, len(storytelling["eny_random_type"])-1)
        return storytelling["eny_random_type"][i]

    def myturn(self, adv):
        self.is_alive()
        display_eny_turn(self.attack_target(adv)[0])


class EnyOldMan(Eny) :
    def __init__(self, hp, att, df, strengh='normal', **kwargs):
        self.common_name = eny_dict["EnyOldMan.common_name"]
        self.definition = eny_dict["EnyOldMan.definition"]
        super().__init__(hp = hp-2, att = att, df = df*0, strengh=strengh, common_name=self.common_name)

    def myturn(self, adv):
        self.is_alive()
        i = self.dice()
        if i < 3 :
            display_eny_turn(replace_variables(eny_dict["EnyOldMan.myturn"], {"self.name" : self.name}))
        else :
            display_eny_turn(self.attack_target(adv)[0])

class EnyRageDog(Eny) :
    def __init__(self, hp, att, df, strengh='normal', **kwargs):
        self.common_name = eny_dict["EnyRageDog.common_name"]
        self.definition = eny_dict["EnyRageDog.definition"]
        super().__init__(hp=hp, att=att+1, df=df-1, strengh=strengh, common_name=self.common_name)

    def myturn(self, adv):
        self.is_alive()
        i = self.dice()
        msg = self.attack_target(adv)[0]
        if i > 4 :
            display_eny_turn(msg, replace_variables(eny_dict["EnyRageDog.myturn"],{"self.name" : self.name}), self.attack_target(adv)[0])
        else :
            display_eny_turn(msg)

ENEMY_CLASSES = {
    "EnyRageDog": EnyRageDog,
    "EnyOldMan": EnyOldMan,
    "Eny": Eny
}