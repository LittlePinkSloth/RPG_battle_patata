import random
from .items import Item, Wearable
from ..game.display import wait_for_input, display_list, display_msg, display_player_turn
from .rpg_exceptions import DeadCharacter, ToMuchWearable, GameObject

class Character(GameObject) :
    def __init__(self, name, maxhp : int = 20, maxma : int = 10, att : int = 2, df : int = 2):
        super().__init__(name)
        self.maxhp = int(maxhp)
        self.hp = self.maxhp
        self.maxma = int(maxma)
        self.mana = self.maxma
        self.att = int(att)
        self.df = int(df)
        self.status = None

    def __repr__(self):
        return f"Character(name={self.name}, hp={self.hp}/{self.maxhp}, mana={self.mana}/{self.maxma}, att={self.att}, df={self.df})"

    def __str__(self):
        pres = f"{self.name} : {self.hp}/{self.maxhp} HP | {self.mana}/{self.maxma} mana | {self.att} ATK | {self.df} DEF"
        return pres

    def set_status(self, status):
        self.status = status

    def take_damage(self, dmg):
        realdmg = dmg - self.df if (dmg - self.df) >= 0 else 0
        self.hp -=realdmg
        self.is_alive()
        return realdmg

    def is_alive(self):
        if self.hp > 0 : return True
        else : raise DeadCharacter(self)

    def dice(self):
        return random.randint(1,6)

    def attack_target(self, enemy):
        dc = self.dice()
        if dc == 1:
            return f"{self.name} attacks and... Failed. {enemy.name} is laughing.", isinstance(self, Player)
        elif dc < 5 :
            atk = self.att
        elif 5 == dc:
            atk = self.att * 2
        else:
            #6 et + : true damage
            enemy.hp -= self.att
            enemy.is_alive()
            return f"{self.name} attacked and dealt {self.att} damage.", isinstance(self, Player)

        dmg = int(enemy.take_damage(atk))
        return f"{self.name} attacked and dealt {dmg} damage.", isinstance(self, Player)

class Player(Character) :
    def __init__(self, name, special =('', 0), maxhp = 20, maxma = 10, att = 2, df = 2):
        super().__init__(name, maxhp =maxhp, maxma =maxma, att =att, df =df)
        self.inventory = []
        self.equipment = []
        self.exp = 0
        self.lvl = 1
        self.luck = 0
        self.status = None
        self.special = special

    def __str__(self):
        if self.status :
            return super().__str__() + f' | Status : {self.status}'
        else :
            return super().__str__()

    def lvl_up(self):
        #xp_to_lvl = 0
        if self.lvl < 5 :
            xp_to_lvl = self.lvl * 10
        elif self.lvl < 11 :
            xp_to_lvl = self.lvl * 15
        else :
            xp_to_lvl = self.lvl * 20

        if self.exp >= xp_to_lvl :
            self.lvl += 1
            self.exp -= xp_to_lvl
            self.att += int(1+self.lvl/6)
            self.df += int(1+self.lvl/6)
            self.maxhp += int(2 + self.lvl*1.1)
            self.hp += int(2 + self.lvl*1.1)
            self.maxma += int(1 + self.lvl*1)
            self.mana += int(1 + self.lvl*1)
            return f"Congratulations, you leveled up to level : {self.lvl} ! You're stronger now (+ {int(self.maxhp / 4)} hp, + {int(self.maxma / 5)} mana, + {1 + int(self.att / 4)} attack, + {1 + int(self.df / 4)} defense)."
        else :
            return f"You have {self.exp}/{xp_to_lvl} exp to level {self.lvl + 1}."

    def gain_xp(self, xp):
        self.exp += xp
        return self.lvl_up()

    def special_attack(self, enemy):
        msg = "It seems you do not have any special attack. You just attack the enemy. "
        res = self.attack_target(enemy)
        return msg + res[0], res[1]

    def myturn(self, adv):
        self.is_alive()
        list_choices = ["Attack",f"Special capacity : {self.special[0]} (cost {self.special[1]} mana)","Use an item from your inventory"]
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
        if isinstance(item, Wearable) : return self.equip_wearable(item)

        msg = item.use(self)
        self.is_alive()
        del self.inventory[self.inventory.index(item)]
        if msg :
            return f"You use {item.name}." + " " + msg
        else :
            return f"You use {item.name}."

    def equip_wearable(self, item):
        try :
            if len(self.equipment) > 4 :
                raise ToMuchWearable
            item.use(self)
            del self.inventory[self.inventory.index(item)]
            self.equipment.append(item)
            return f"You've equiped {item.name}."
        except ToMuchWearable :
            return self.change_wearable(item)

    def change_wearable(self, item):
        choice = wait_for_input(display_list(self.equipment), True)
        if choice == -1 :
            return
        try:
            uitem = self.equipment[int(choice) - 1]
            self.unequip_wearable(uitem)
            return self.equip_wearable(item)
        except IndexError:
            pass

    def unequip_wearable(self, item):
        item.use(self)
        del self.equipment[self.equipment.index(item)]
        self.inventory.append(item)

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
            "status" : self.status
        }

    @staticmethod
    def from_dict(data):
        char_class = data["class"]
        if char_class == "Baker":
            char = Baker(data["name"])
        elif char_class == "NarcissicPerverse":
            char = NarcissicPerverse(data["name"])
        elif char_class == "Gambler":
            char = Gambler(data["name"])
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
        char.status = data["status"]
        return char

class Baker(Player) :
    definition = "Baker : player who has more hp and attack. Special attack (cost 5 mana) : strong gluten. Divides by 2 the ennemy attack, and if you have luck, divides the defense too."
    def __init__(self, name):
        self.special = ("Strong gluten", 5)
        super().__init__(name, special = self.special, maxhp = 25, att = 3)

    def special_attack(self, enemy):
        if self.mana >= self.special[1] :
            self.mana -= self.special[1]
            msg = f"You invoke {self.special[0]}.\n"
            de = self.dice()
            if de == 6 :
                enemy.att = int(enemy.att/2)
                enemy.df = int(enemy.df/ 2)
                return msg + "Critical hit ! Enemy attack and defense are divided by 2.", True
            else :
                enemy.att = int(enemy.att / 2)
                return msg + "Enemy attack is divided by 2.", True
        else :
            return "Not enough mana. That's sad, you've lost time so it's your enemy's turn...", True

class NarcissicPerverse(Player) :
    definition = "Narcissic perverse : player who has more mana. Special attack (5) : Guiltifying ! Deals some damages to enemy and heal of half."
    def __init__(self, name):
        self.special = ("Guiltifying", 5)
        super().__init__(name, maxma=15, special=self.special)

    def special_attack(self, enemy):
        if self.mana >= self.special[1] :
            self.mana -= self.special[1]
            msg = f"You invoke {self.special[0]}.\n"
            dmg = int(4*1.2*self.lvl)
            self.hp += int(dmg/2)
            if self.hp > self.maxhp : self.hp = self.maxhp
            enemy.hp -= dmg
            enemy.is_alive()
            return msg + f"{enemy.name} enemy lost {dmg} hp while you healed by {int(dmg/2)}.", True
        else :
            return "Not enough mana. That's sad, you've lost time so it's your enemy's turn...", True

class Gambler(Player) :
    definition = "Gambler : player who has a better luck. Special attack (3) : Spring rolls. If 6 or higher, inflicts half of the enemy max hp damages."
    def __init__(self, name):
        self.special = ("Spring rolls",3)
        super().__init__(name, df=3,maxhp=22, special = self.special)
        self.luck = 2

    def special_attack(self, enemy):
        if self.mana >= self.special[1] :
            self.mana -= self.special[1]
            msg = f"\nYou invoke {self.special[0]}.\n"
            de = self.dice()
            if de == 5 :
                dmg = int(enemy.maxhp / 4)
                enemy.hp -= dmg
                enemy.is_alive()
                return msg + f"{de}... Not that bad ! {enemy.name} suffers {dmg}.", True
            elif 6<= de <= 8 :
                dmg = int(enemy.maxhp/2)
                enemy.hp -= dmg
                enemy.is_alive()
                return msg + f"{de} ! {enemy.name} suffers {dmg} damages.", True
            elif de > 8 :
                l = random.randint(1, de-8)
                dmg = int(enemy.maxhp / 2)
                msg += f"{de} ! {enemy.name} suffers {dmg} damages. \n"
                enemy.hp -= int(enemy.maxhp / 2)
                enemy.is_alive()

                match l :
                    case 1,2 :
                        msg += f"{enemy.name} also lost {int(enemy.att / 4)} attack."
                        enemy.att -= int(enemy.att / 4)
                    case 3,4 :
                        msg += f"{enemy.name} also lost {int(enemy.df / 4)} defense."
                        enemy.df -= int(enemy.df / 4)
                    case _ :
                        msg += f"{enemy.name} also lost {int(enemy.att / 4)} attack and {int(enemy.df / 4)} defense."
                        enemy.att -= int(enemy.att / 4)
                        enemy.df -= int(enemy.df / 4)
                return msg, True
            else :
                return f"{de}... Nice try but it does nothing.", True
        else :
            return "Not enough mana. That's sad, you've lost time so it's your enemy's turn...", True

    def dice(self):
        return random.randint(1, 6+self.luck)

    def lvl_up(self):
        msg = super().lvl_up()
        if self.lvl % 5 == 0 :
            self.luck +=1
            msg += "You also increase your luck by 1."
        return msg

