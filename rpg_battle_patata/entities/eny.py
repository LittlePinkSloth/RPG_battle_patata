import random
from ..entities.characters import Character
from ..entities.status import Status
from ..game.display import display_eny_turn, display_msg
from rpg_battle_patata.game.language_manager import eny_dict, storytelling, status_dict
from ..game.utils import replace_variables, load_datas, file_paths


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

class EnyElementaryBug(Eny) :
    def __init__(self, strengh='normal', **kwargs):
        self.common_name = eny_dict["EnyElementaryBug.common_name"]
        self.definition = eny_dict["EnyElementaryBug.definition"]
        super().__init__(hp=1, att=0, df=0, strengh=strengh, common_name=self.common_name)
        self.life = self.setlife()
        self.element = self.set_element()
        self.malus = self.set_malus()

    def set_malus(self) :
        status_table = load_datas(file_paths['status'])
        available_status = [s for s in status_table['status_table'] if s['type'] == 0]
        element_table = {k: (status_dict[v["status"]], v["effect"]) for k, v in zip(eny_dict['element_list'], available_status)}
        return element_table[self.element]

    @staticmethod
    def set_element():
        return eny_dict["element_list"][random.randint(0, len(eny_dict["element_list"])-1)]

    def setlife(self):
        if self.strengh == 'normal' :
            return 1
        elif self.strengh == 'elite' :
            return 2
        else :
            return 3

    def is_alive(self):
        if self.hp <= 0 and self.life :
            self.hp = 1
            self.life -= 1
            display_msg(eny_dict["EnyElementaryBug.still_alive"])
            return True
        else :
            super().is_alive()

    def create_status(self):
        duration = 2 + self.life
        strengh = self.life if self.life else 1
        once = True if self.malus[1] in ["att", "df", "luck"] else False
        reversible = True if self.malus[1] in ["att", "df", "luck"] else False

        return Status(self.malus[0], duration=duration, strengh=strengh, once=once, reversible=reversible)

    def myturn(self, adv):
        self.is_alive()
        self.apply_all_status()
        adv.set_status(self.create_status())
        msg = eny_dict["EnyElementaryBug.myturn"]
        loc_vars = {"self.name" : self.name, "self.malus[0]" : self.malus[0]}
        display_eny_turn(replace_variables(msg, loc_vars))




ENEMY_CLASSES = {
    "EnyRageDog": EnyRageDog,
    "EnyOldMan": EnyOldMan,
    "Eny": Eny,
    "EnyElementaryBug" : EnyElementaryBug
}