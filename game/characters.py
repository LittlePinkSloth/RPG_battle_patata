import random
from .data import GameObject
from .items import Item


class RPGException (BaseException) :
    pass

class DeadCharacter(RPGException) :
    def __init__(self, char) :
        self.dead = char

    def __str__(self):
        if isinstance(self.dead, Player) :
            return "Sorry, you died. Heroically, but still... You're dead."
        else :
            return f"{self.dead.name} enemy died. You won."

class ItemNotFound(RPGException) :
    def __str__(self):
        return "You do not have this item in your inventory."

class Character(GameObject) :
    def __init__(self, name, maxhp = 20, maxma = 10, att = 2, df = 2):
        super().__init__(name)
        self.maxhp = maxhp
        self.hp = self.maxhp
        self.maxma = maxma
        self.mana = self.maxma
        self.att = att
        self.df = df

    def __repr__(self):
        return f"Character(name={self.name}, hp={self.hp}/{self.maxhp}, mana={self.mana}/{self.maxma}, att={self.att}, df={self.df})"

    def __str__(self):
        pres = f"{self.name} : {self.hp}/{self.maxhp} HP | {self.mana}/{self.maxma} mana | {self.att} ATK | {self.df} DEF"
        return pres

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
        if dc == 1 :
            print(f"{self.name} attacks and... Failed. {enemy.name} is laughing.")
            return
        elif 5 <= dc :
            atk = self.att * 2
        else :
            atk = self.att
        try :
            dmg = enemy.take_damage(atk)
            print(f"{self.name} attacked and dealt {dmg} damage.")
        except DeadCharacter :
            print(f"{self.name} attacked. {enemy.name} took too much damage.")

class Player(Character) :
    def __init__(self, name, maxhp = 20, maxma = 10, att = 2, df = 2):
        super().__init__(name, maxhp =maxhp, maxma =maxma, att =att, df =df)
        self.inventory = []
        self.exp = 0
        self.lvl = 1
        self.luck = 0


    def lvl_up(self):
        xp_to_lvl = self.lvl * 10
        if self.exp >= xp_to_lvl :
            self.lvl += 1
            self.exp -= xp_to_lvl
            self.att += (1+int(self.att/4))
            self.df += (1+int(self.df/4))
            self.maxhp += int(self.maxhp/4)
            self.hp += int(self.maxhp/5)
            self.maxma += int(self.maxma/5)
            self.mana += int(self.maxma/5)
            print(f"Congratulations, you leveled up to level : {self.lvl} ! You're stronger now (+ {int(self.maxhp / 4)} hp, + {int(self.maxma / 5)} mana, + {1 + int(self.att / 4)} attack, + {1 + int(self.df / 4)} defense).")
        else :
            print(f"You have {self.exp}/{xp_to_lvl} exp to next level.")

    def gain_xp(self, xp):
        self.exp += xp
        self.lvl_up()

    def get_inventory(self):
        inv = ""
        for i in range(len(self.inventory)) :
            inv += f"  {i + 1} --> {self.inventory[i]}\n"
        return inv

    def special_attack(self, enemy):
        print("It seems you do not have any special attack. You just attack the enemy.")
        self.attack_target(enemy)

    def myturn(self, adv):
        self.is_alive()
        goodchoices = ['1','2','3']
        text_input = "." + 3*"_" + "YOUR TURN" + 3*"_" + ".\n" + "|   1 - Attack\n" + "|   2 - Special capacity\n" + "|   3 - Use an item from your inventory.\n" + "|   --> "
        todo = input(text_input)
        while todo not in goodchoices :
            todo = input("Please chose 1, 2 or 3. \n--> ")
        match todo :
            case '1' :
                self.attack_target(adv)
            case '2' :
                self.special_attack(adv)
            case '3' :
                print(self.get_inventory())
                while True :
                    choice = input("Witch item to use ? 0 to use nothing.\n --> ")
                    if not choice.isdigit() : continue
                    if choice == '0' :
                        #si le joueur ne veut pas utiliser d'item, il recommence son tour
                        self.myturn(adv)
                        break
                    try :
                        item = self.inventory[int(choice)-1]
                        self.use_item(item)
                        if item.__class__.__name__ == 'Wearable' : break
                        else : del self.inventory[int(choice)-1]
                        break
                    except IndexError :
                        pass

    def add_item(self, item):
        self.inventory.append(item)

    def use_item(self, item):
        try :
            item.use(self)
            print(f"You use {item.name}.")
            self.is_alive()
        except DeadCharacter as dd :
            print(dd)
        except Exception as e :
            print(f"Sorry, something went wrong with your item : {e}")

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
            "inventory": [item.to_dict() for item in self.inventory]
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
        return char

class Baker(Player) :
    definition = "Baker : player who has more hp and attack. Special attack (5) : strong gluten. Divides by 2 the ennemy attack, and if you have luck, divides the defense too."
    def __init__(self, name):
        super().__init__(name, maxhp = 25, att = 3)
        self.__special = "Strong gluten"

    def special_attack(self, enemy):
        if self.mana >= 5 :
            self.mana -= 5
            print(f"You invoke {self.__special}.")
            de = self.dice()
            if de == 6 :
                print("Critical hit ! Enemy attack and defense are divided by 2.")
                enemy.att = int(enemy.att/2)
                enemy.df = int(enemy.df/ 2)
            else :
                print("Enemy attack is divided by 2.")
                enemy.att = int(enemy.att / 2)
        else :
            print("Not enough mana. That's sad, you've lost time so it's your enemy's turn...")

class NarcissicPerverse(Player) :
    definition = "Narcissic perverse : player who has more mana. Special attack (5) : deals some damages to enemy and heal of half."
    def __init__(self, name):
        super().__init__(name, maxma=15)
        self.__special = "Guiltifying"

    def special_attack(self, enemy):
        if self.mana >= 5 :
            self.mana -= 5
            print(f"You invoke {self.__special}.")
            dmg = int(4*1.5*self.lvl)
            self.hp += int(dmg/2)
            if self.hp > self.maxhp : self.hp = self.maxhp
            enemy.hp -= dmg
            print(f"{enemy.name} enemy lost {dmg} hp while you healed by {int(dmg/2)}.")
            try :
                enemy.is_alive()
            except DeadCharacter :
                print("Enemy dead.")
        else :
            print("Not enough mana. That's sad, you've lost time so it's your enemy's turn...")

class Gambler(Player) :
    definition = "Gambler : player who has a better luck. Special attack (3) : roll a dice. If 6 or higher, inflicts half of the enemy max hp damages."
    def __init__(self, name):
        super().__init__(name)
        self.luck = 1
        self.__special = "Spring rolls"

    def special_attack(self, enemy):
        if self.mana >= 3 :
            self.mana -= 3
            print(f"You invoke {self.__special}.")
            de = self.dice()
            if de >= 6 :
                print(f"{de} ! {enemy.name} suffers {int(enemy.maxhp/2)} damages.")
                enemy.hp -= int(enemy.maxhp/2)
                try:
                    enemy.is_alive()
                except DeadCharacter:
                    print("Enemy dead.")
            else :
                print(f"{de}... Nice try but it does nothing.")

    def dice(self):
        return random.randint(1, 6+self.luck)

    def lvl_up(self):
        super().lvl_up()
        if self.lvl % 5 == 0 :
            self.luck +=1
            print("You alse increase your luck by 1.")

class EnyOldMan(Character) :
    definition = "An old man bothered by your presence. He sometimes forgot things."
    def __init__(self, name, hp, att, df):
        super().__init__(name = name, maxhp = hp-2, att = att, df = df*0)

    def __str__(self):
        pres = " | Type : Old man"
        return super().__str__() + pres

    def myturn(self, adv):
        self.is_alive()
        i = self.dice()
        if i < 3 :
            print(f"{self.name} forgot of your presence and does nothing.")
        else :
            self.attack_target(adv)

class EnyRageDog(Character) :
    definition = "A strange dog with white slobber. It can attack twice, be carefull."
    def __init__(self, name, hp, att, df):
        super().__init__(name=name, maxhp=hp, att=att+1, df=df-1)

    def __str__(self):
        pres = " | Type : Agressive dog"
        return super().__str__() + pres

    def myturn(self, adv):
        self.is_alive()
        i = self.dice()
        self.attack_target(adv)
        if i > 4 :
            print(f"{self.name} bites again !")
            self.attack_target(adv)