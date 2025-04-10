import msvcrt, os
from .characters import *
from .items import *

def display_stats(ply, adv) :
    nbchar = len(adv.__str__()) if len(adv.__str__()) > len(ply.__str__()) else len(ply.__str__())

    up = " ." + (4+nbchar)*"_" + ".\n"
    sply = "|  " + ply.__str__() + (nbchar - len(ply.__str__()) + 2)*" " + "|\n"
    sadv = "|  " + adv.__str__() + (nbchar - len(adv.__str__()) + 2)*" " + "|\n"
    bot = "|" + (5+nbchar-1)*"_" + "|"
    print(up,sply,sadv,bot)

def name_gen() :
    firstname = ['Rex', 'Gertrude', 'Ferdinand', 'Loan', 'Yseult', 'Rudolf', 'Vlad', 'Robert']
    adj = ['Little', 'Bloody', 'Rude', 'Bad', 'Kind', 'Clever', 'Big', 'Asshole', 'Lost', 'Crazy', 'Sleepy']
    f = random.randint(0, len(firstname)-1)
    a = random.randint(0, len(adj)-1)
    return adj[a] + ' ' + firstname[f]

def enemy_generator(ply) :
    eny_list = ['dog', 'oldman']
    choice = random.randint(0, len(eny_list)-1)
    try :
        eny = eny_list[choice]
    except IndexError :
        eny = '0'
    hp = int(random.randint(0,5)+ ply.lvl * 5)
    att = int(random.randint(0, 1)+ ply.lvl * 2)
    df = int(random.randint(0,1) + ply.lvl * 2)
    name = name_gen()
    eny_gen = None
    match eny :
        case 'dog' :
            eny_gen = EnyRageDog(name, hp = hp, att = att, df = df)
        case 'oldman' :
            eny_gen = EnyOldMan(name, hp = hp, att = att, df = df)
        case '0' :
            eny_gen = EnyRageDog('Weakest Mouse', hp = 1, att = 1, df = 1)

    return eny_gen

def chose_player() :
    name = input("What is your name ?\n--> ").strip()
    print(f"\nHello {name}. What kind of player are you ?\n")
    print(f"  1 : {Baker.definition}\n  2 : {NarcissicPerverse.definition}\n  3 : {Gambler.definition}\n")
    choice = input("--> ")
    while choice not in ['1', '2', '3'] :
        choice = input("--> ")

    match choice :
        case '1' :
            return Baker(name)
        case '2' :
            return NarcissicPerverse(name)
        case '3' :
            return Gambler(name)

def wait_key() :
    print("--> ")
    msvcrt.getch()  # Attend n'importe quelle touche, sans besoin d'appuyer sur Entrée

def clear_console() :
    os.system('cls')

def enemy_encounter(eny) :
    story = ["After several meters in the dungeon, you meet ","You open a door and then... ", "You smell something strange. It's ", "You hear something behind you. You just have time to pivot to see "]
    num = random.randint(0, len(story)-1)
    print(f"{story[num]}{eny.name}! \nIt can be defined by : {eny.definition} You have to fight for your life !")
    wait_key()
    clear_console()

def item_generator(ply) :
    item_type = ply.dice()
    hp = 4 + ply.lvl*2
    mana = 2 + int(ply.lvl*1.5)
    att = int(ply.lvl*1.5)
    df = int(ply.lvl*1.5)
    if item_type < 6 :
        match item_type :
            case 1 :
                return Eatable('Health potion', hp = hp)
            case 2 :
                return Eatable('Adaptive Health potion', kind ='adaptive', hp = 1)
            case 3 :
                return Eatable('Mana potion', mana=mana)
            case 4 :
                return Eatable('Adaptive Mana potion', kind='adaptive', mana=1)
            case 5 :
                return Eatable('Bread and cheese', hp = hp, mana = mana)
    else :
        adj = ['Thin','Black', 'Little', 'Strange','Old','Uggly','Heavy']
        obj = ['Hat','Stick','Cloak','Pants','Stone','Crown']
        nba = random.randint(0, len(adj)-1)
        nbo = random.randint(0, len(obj)-1)
        name = adj[nba] + ' ' + obj[nbo]
        return Wearable(name, random.randint(0,1)*hp, random.randint(0,1)*mana, random.randint(0,1)*att, random.randint(0,1)*df)

def chest(ply) :
    story = ["Your left foot hit something... It's a chest !", "You open a door. The room is empty, but a big chest is in the middle. ",
             "You smell something strange. It's from an old chest. ", "You find a little bright box. It's not locked. "]
    ns = random.randint(0, len(story)-1)
    print(story[ns])
    op = input("You can let it alone (1), or open it (2).\n--> ")
    while op not in ['1', '2'] :
        op = input("--> ")
    if op == '1' : return print("You go ahead in the dungeon without touching the chest.")
    print("You try to open it...")
    inside = ply.dice()
    if inside == 1 :
        hp = int(ply.maxhp*0.3)
        print(f"It was trapped. You lose {ply.take_damage(hp)} hp.")
    elif inside == 2 :
        print(f"The chest is empty...")
    elif inside < 6 :
        it = item_generator(ply)
        print(f"A {it.name} was in the chest. It's now in your inventory")
        ply.add_item(it)
    else :
        it = item_generator(ply)
        it1 = item_generator(ply)
        print(f"Lucky day ! The chest was full of objects ! You found {it.name} and {it1.name} !")
        ply.add_item(it)
        ply.add_item(it1)

def fire_camp(ply) :
    print("You just arrived to a peacefull place in this horrible dungeon. You can get some rest and be healed by half of your total hp.")
    heal = input("Do you want to take a nap ?\n1 : yes\n2 : no ! I'm not a child.\n--> ")
    while heal not in ['1', '2'] :
        heal = input("--> ")
    if heal == '2' : return print("Ok ok, no need to shout out... So, you can continue.")

    ply.hp += int(ply.maxhp/2)
    if ply.hp > ply.maxhp : ply.hp = ply.maxhp
    ply.mana += int(ply.maxma/2)
    if ply.mana > ply.maxma : ply.mana = ply.maxma

    print(f"You rested sucessfully. You feel better : {ply.hp}/{ply.maxhp} hp, {ply.mana}/{ply.maxma} mana.")

def event_generator(ply) :
    event = random.randint(1,5)
    if event == 4 :
        chest(ply)
        wait_key()
        return False
    elif event == 5 :
        fire_camp(ply)
        wait_key()
        return False
    else :
        eny = enemy_generator(ply)
        enemy_encounter(eny)
        return eny