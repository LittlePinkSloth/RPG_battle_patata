import random
from .items import Item, Wearable
from ..game.display import wait_for_input, display_list, display_msg, display_player_turn
from .rpg_exceptions import DeadCharacter, ToMuchWearable, GameObject
from ..game.utils import replace_variables, replace_variables_list
from rpg_battle_patata.game.language_manager import get_dict
from .status import Status

class Character(GameObject) :
    def __init__(self, name, maxhp : int = 20, maxma : int = 10, att : int = 2, df : int = 2, luck = 0):
        super().__init__(name)
        self.maxhp = int(maxhp)
        self.hp = self.maxhp
        self.maxma = int(maxma)
        self.mana = self.maxma
        self.att = int(att)
        self.df = int(df)
        self.status = []
        self.luck = luck


    def __repr__(self):
        return f"Character(name={self.name}, hp={self.hp}/{self.maxhp}, mana={self.mana}/{self.maxma}, att={self.att}, df={self.df})"

    def __str__(self):
        pres = f"{self.name} : {self.hp}/{self.maxhp} HP | {self.mana}/{self.maxma} mana | {self.att} ATK | {self.df} DEF"
        if self.status :
            pres += f' | Status : {self.status}'
        return pres

    def set_status(self, status) :
        self.status.append(status)

    def cure_status(self, status) :
        characters_dict = get_dict("characters_dict")
        i = self.status.index(status)
        name = status.name
        if status.reversible :
            effect, value = status.reverse_effect()
            match effect :
                case "maxhp" :
                    self.maxhp -= value
                case "maxma" :
                    self.maxma -= value
                case "att" :
                    self.att -= value
                case "df" :
                    self.df -= value
                case "luck" :
                    self.luck -= value
                case _ :
                    pass
        del self.status[i]
        return replace_variables(characters_dict["character.cure_status"], {"name" : name.capitalize()})

    def match_status_effect(self, effect, rate):
        match effect:
            case "hp":
                val = int(self.maxhp * rate)
                self.hp += val
                return val
            case "maxhp":
                val = int(self.maxhp * rate)
                self.maxhp += val
                if self.hp > self.maxhp : self.hp = self.maxhp
                return val
            case "luck":
                val = rate
                self.luck += val
                return val
            case "att":
                val = int(self.att * rate)
                self.att += val
                return val
            case "df":
                val = int(self.df * rate)
                self.df += val
                return val
            case "maxma":
                val = int(self.maxma * rate)
                self.maxma += val
                if self.mana > self.maxma : self.mana = self.maxma
                return val
            case "mana":
                val = int(self.maxma * rate)
                self.mana += val
                if self.mana < 0 : self.mana = 0
                return val
            case _:
                return 0

    def apply_all_status(self):
        msg = ''
        for stat in reversed(self.status) :
            msg += f"{self.impact_status(stat)}\n"
        return msg, isinstance(self, Player)

    def impact_status(self, status):
        characters_dict = get_dict("characters_dict")
        stats_dict = get_dict('stats_dict')
        effect, rate = status.get_status_effect()
        if effect and rate :
            loc_vars = {"status.name": status.name, "effect": stats_dict[effect], "value" : self.match_status_effect(effect, rate)}
            status.apply_effect(loc_vars['value'])
            return replace_variables(characters_dict["character.impact_status"], loc_vars)
        else :
            return self.cure_status(status)

    def take_damage(self, dmg):
        realdmg = dmg - self.df if (dmg - self.df) >= 0 else 0
        self.hp -=realdmg
        return realdmg

    def is_alive(self):
        if self.hp > 0 : return True
        else : raise DeadCharacter(self)

    def dice(self):
        return random.randint(1,6+self.luck)

    def attack_target(self, enemy):
        characters_dict = get_dict("characters_dict")
        loc_vars = {"self.name" : self.name, "enemy.name" : enemy.name}
        dc = self.dice()

        if dc == 1:
            return replace_variables(characters_dict["attack_target.failed"], loc_vars), isinstance(self, Player)
        elif dc < 5 :
            dmg = int(enemy.take_damage(self.att))
        elif 5 == dc:
            dmg = int(enemy.take_damage(self.att * 2))
        else:
            #6 et + : true damage
            enemy.hp -= self.att
            #enemy.is_alive()
            dmg = self.att

        loc_vars['dmg'] = dmg
        return replace_variables(characters_dict["attack_target.atk"], loc_vars), isinstance(self, Player)

class Player(Character) :
    def __init__(self, name, special =('', 0), maxhp = 20, maxma = 10, att = 2, df = 2, luck=0):
        super().__init__(name, maxhp =maxhp, maxma =maxma, att =att, df =df, luck=luck)
        self.inventory = []
        self.equipment = []
        self.exp = 0
        self.lvl = 1
        self.status = []
        self.special = special


    def lvl_up(self):
        characters_dict = get_dict("characters_dict")
        if self.lvl < 5 :
            xp_to_lvl = self.lvl * 10
        elif self.lvl < 11 :
            xp_to_lvl = self.lvl * 15
        else :
            xp_to_lvl = self.lvl * 20

        if self.exp >= xp_to_lvl :
            aatt = int(1+self.lvl/6)
            adf = int(1+self.lvl/6)
            ahp = int(2 + self.lvl*1.1)
            amana = int(1 + self.lvl*1)
            self.lvl += 1
            self.exp -= xp_to_lvl
            self.att += aatt
            self.df += adf
            self.maxhp += ahp
            self.hp += ahp
            self.maxma += amana
            self.mana += amana
            loc_vars = {"self.lvl" : self.lvl, "aatt" : aatt, "adf" : adf, "amana" : amana, "ahp" : ahp}
            return replace_variables(characters_dict["lvl_up.yes"], loc_vars)
        else :
            loc_vars = {"self.lvl + 1" : self.lvl + 1, "self.exp" : self.exp, "xp_to_lvl" : xp_to_lvl}
            return replace_variables(characters_dict["lvl_up.no"], loc_vars)

    def gain_xp(self, enemy):
        self.exp += int(enemy.maxhp/1.5)
        return self.lvl_up()

    def special_attack(self, enemy):
        characters_dict = get_dict("characters_dict")
        msg = characters_dict["player.special_attack"]
        res = self.attack_target(enemy)
        return msg + res[0], res[1]

    def myturn(self, adv):
        characters_dict = get_dict("characters_dict")
        self.is_alive()
        display_msg(*self.apply_all_status())
        loc_vars = {"self.special[0]" : self.special[0], "self.special[1]" : self.special[1]}
        list_choices = replace_variables_list(characters_dict["player.myturn"], loc_vars)
        todo = wait_for_input(display_player_turn(list_choices), False)
        match todo :
            case 0 :
                display_msg(*self.attack_target(adv))
            case 1 :
                display_msg(*self.special_attack(adv))
            case 2 :
                choice = wait_for_input(display_list(self.inventory), True)
                if choice == -1 :
                    return self.myturn(adv)
                try:
                    item = self.inventory[choice]
                    display_msg(self.use_item(item), True)
                except IndexError:
                    pass

    def add_item(self, item):
        self.inventory.append(item)

    def use_item(self, item):
        characters_dict = get_dict("characters_dict")
        if isinstance(item, Wearable) : return self.equip_wearable(item)
        message = replace_variables(characters_dict["player.use_item"], {"item.name" : item.name})
        msg = item.use(self)
        self.is_alive()
        del self.inventory[self.inventory.index(item)]
        if msg :
            return message + " " + msg
        else :
            return message

    def equip_wearable(self, item):
        characters_dict = get_dict("characters_dict")
        try :
            if len(self.equipment) > 4 :
                raise ToMuchWearable
            item.use(self)
            del self.inventory[self.inventory.index(item)]
            self.equipment.append(item)
            return replace_variables(characters_dict["player.equip_wearable"], {"item.name" : item.name})
        except ToMuchWearable :
            return self.change_wearable(item)

    def change_wearable(self, item):
        characters_dict = get_dict("characters_dict")
        choice = wait_for_input(display_list(self.equipment), True)
        if choice == -1 :
            return characters_dict["player.change_wearable.no"]
        try:
            uitem = self.equipment[int(choice) - 1]
            self.unequip_wearable(uitem)
            return self.equip_wearable(item)
        except IndexError:
            pass

    def unequip_wearable(self, item):
        characters_dict = get_dict("characters_dict")
        item.use(self)
        del self.equipment[self.equipment.index(item)]
        self.inventory.append(item)
        return replace_variables(characters_dict["player.unequip_wearable"], {"item.name": item.name})


    def to_dict(self):
        return {
            "class": self.__class__.__name__,
            "name": self.name,
            "hp": self.hp,
            "maxhp": self.maxhp,
            "exp": self.exp,
            "lvl" : self.lvl,
            "mana" : self.mana,
            "maxma" : self.maxma,
            "att" : self.att,
            "df" : self.df,
            "luck" : self.luck,
            "inventory": [item.to_dict() for item in self.inventory],
            "equipment" : [item.to_dict() for item in self.equipment],
            "status" : [status.to_dict() for status in self.status]
        }

    @staticmethod
    def from_dict(data):
        char_class = data["class"]
        if char_class in CHARACTER_CLASSES :
            char = CHARACTER_CLASSES[char_class](data["name"])
        else:
            char = Player(data["name"])  # fallback

        char.hp = data["hp"]
        char.maxhp = data["maxhp"]
        char.mana = data["mana"]
        char.maxma = data["maxma"]
        char.att = data["att"]
        char.luck = data["luck"]
        char.lvl = data["lvl"]
        char.df = data["df"]
        char.exp = data["exp"]
        char.inventory = [Item.from_dict(item_data) for item_data in data["inventory"]]
        char.equipment = [Item.from_dict(item_data) for item_data in data["equipment"]]
        char.status = [Status.from_dict(status_data) for status_data in data["status"]]
        return char

class Baker(Player) :
    characters_dict = get_dict("characters_dict")
    definition = characters_dict["Baker.definition"]
    def __init__(self, name):
        characters_dict = get_dict("characters_dict")
        self.special = (characters_dict["Baker.special"], 5)
        super().__init__(name, special = self.special, maxhp = 25, att = 3)
        self.class_definition = characters_dict["Baker.definition"]
        self.class_name = characters_dict["Baker.class"]

    def special_attack(self, enemy):
        characters_dict = get_dict("characters_dict")
        if self.mana >= self.special[1] :
            self.mana -= self.special[1]
            msg = replace_variables(characters_dict["AnyClass.special_attack.invoke"], {"self.special[0]" : self.special[0]})
            de = self.dice()
            if de >= 6 :
                enemy.att = int(enemy.att/2)
                enemy.df = int(enemy.df/ 2)
                return msg + characters_dict["Baker.special_attack.critical"], True
            else :
                enemy.att = int(enemy.att / 2)
                return msg + characters_dict["Baker.special_attack.ok"], True
        else :
            return characters_dict["AnyClass.special_attack.nomana"], True

class NarcissicPerverse(Player) :
    characters_dict = get_dict("characters_dict")
    definition = characters_dict["NarcissicPerverse.definition"]
    def __init__(self, name):
        characters_dict = get_dict("characters_dict")
        self.special = (characters_dict["NarcissicPerverse.special"], 5)
        super().__init__(name, maxma=15, special=self.special)
        self.class_definition = characters_dict["NarcissicPerverse.definition"]
        self.class_name = characters_dict["NarcissicPerverse.class"]


    def special_attack(self, enemy):
        characters_dict = get_dict("characters_dict")
        if self.mana >= self.special[1] :
            self.mana -= self.special[1]
            msg = replace_variables(characters_dict["AnyClass.special_attack.invoke"], {"self.special[0]" : self.special[0]})
            dmg = int(4*1.2*self.lvl)
            self.hp += int(dmg/2)
            if self.hp > self.maxhp : self.hp = self.maxhp
            enemy.hp -= dmg
            loc_vars = {"enemy.name":enemy.name, "int(dmg/2)" : int(dmg/2) , "dmg": dmg, "hp" :get_dict("stats_dict")["hp"] }
            return msg + replace_variables(characters_dict["NarcissicPerverse.special_attack.ok"], loc_vars), True
        else :
            return characters_dict["AnyClass.special_attack.nomana"], True

class Gambler(Player) :
    characters_dict = get_dict("characters_dict")
    definition = characters_dict["Gambler.definition"]
    def __init__(self, name):
        characters_dict = get_dict("characters_dict")
        self.special = (characters_dict["Gambler.special"],3)
        super().__init__(name, df=3,maxhp=22, special = self.special)
        self.luck = 2
        self.class_definition = characters_dict["Gambler.definition"]
        self.class_name = characters_dict["Gambler.class"]


    def special_attack(self, enemy):
        characters_dict = get_dict("characters_dict")
        if self.mana >= self.special[1] :
            self.mana -= self.special[1]
            msg = replace_variables(characters_dict["AnyClass.special_attack.invoke"], {"self.special[0]" : self.special[0]})
            de = self.dice()
            dmg = int(enemy.maxhp / 4) if de==5 else int(enemy.maxhp/2)
            loc_vars = {"de" : de, "dmg" : dmg, "enemy.name" : enemy.name}
            if 5 <= de <= 8 :
                enemy.hp -= dmg
                return msg + replace_variables(characters_dict["Gambler.special_attack.yes"], loc_vars), True
            elif de > 8 :
                l = random.randint(1, de-8)
                msg += replace_variables(characters_dict["Gambler.special_attack.yes"], loc_vars)
                enemy.hp -= dmg
                atk = int(enemy.att / 4)
                df = int(enemy.df / 4)
                loc_vars["atk"] = atk
                loc_vars["df"] = df
                match l :
                    case 1,2 :
                        msg += replace_variables(characters_dict["Gambler.special_attack.atk"], loc_vars)
                        enemy.att -= atk
                    case 3,4 :
                        msg += replace_variables(characters_dict["Gambler.special_attack.df"], loc_vars)
                        enemy.df -= df
                    case _ :
                        msg += replace_variables(characters_dict["Gambler.special_attack.atkdf"], loc_vars)
                        enemy.att -= atk
                        enemy.df -= df
                return msg, True
            else :
                return replace_variables(characters_dict["Gambler.special_attack.no"], loc_vars), True
        else :
            return characters_dict["AnyClass.special_attack.nomana"], True

    def lvl_up(self):
        characters_dict = get_dict("characters_dict")
        msg = super().lvl_up()
        if self.lvl % 5 == 0 :
            self.luck +=1
            msg += characters_dict["Gambler.lvl_up"]
        return msg


CHARACTER_CLASSES = {
    "Baker" : Baker,
    "NarcissicPerverse" : NarcissicPerverse,
    "Gambler" : Gambler
}