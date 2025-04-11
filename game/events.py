import msvcrt, os, json
from .characters import *
from .items import *
from genericpath import exists


def save_game(player, filename="save/savegame.json"):
    try :
        with open(filename, "w") as f:
            json.dump(player.to_dict(), f, indent=4)
            return True
    except OSError as e:  # Spécifie une exception liée au système

        print("The file could not be opened:", os.strerror(e.errno))
        return False
    except Exception as e:
        print(f"Erreur ({type(e).__name__}) :", str(e))
        return False

def load_game(filename="savegame.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return Player.from_dict(data)
    except FileNotFoundError:
        print(
            "Sorry, we were unable to find your file. Do you want to try again ?\n1 : try again\n2 : start a new game")
        rep = input("--> ")
        while rep not in ['1', '2']:
            rep = input("--> ")

        if rep == '1':
            return openning()
        else:
            return chose_player()


    except OSError as e:  # Spécifie une exception liée au système

        print("The file could not be opened:", os.strerror(e.errno))
    except Exception as e:
        print(f"Erreur ({type(e).__name__}) :", str(e))



def display_stats(ply, adv) :
    nbchar = len(adv.__str__()) if len(adv.__str__()) > len(ply.__str__()) else len(ply.__str__())

    up = " ." + (4+nbchar)*"_" + "."
    sply = "|  " + ply.__str__() + (nbchar - len(ply.__str__()) + 2)*" " + "|"
    sadv = "|  " + adv.__str__() + (nbchar - len(adv.__str__()) + 2)*" " + "|"
    bot = "|" + (5+nbchar-1)*"_" + "|"
    #print(up,sply,sadv,bot)
    print(up)
    bprint(sply)
    rprint(sadv)
    print(bot)

def name_gen() :
    firstname = ['Rex', 'Gertrude', 'Ferdinand', 'Loan', 'Yseult', 'Rudolf', 'Vlad', 'Robert']
    adj = ['Little', 'Bloody', 'Rude', 'Bad', 'Kind', 'Clever', 'Big', 'Asshole', 'Lost', 'Crazy', 'Sleepy', 'King','Lazy']
    f = random.randint(0, len(firstname)-1)
    a = random.randint(0, len(adj)-1)
    return adj[a] + ' ' + firstname[f]

def enemy_generator(ply) :
    eny_list = ['dog', 'oldman']
    elite = True if (Eny.nb_eny % 5 ==0 and Eny.nb_eny %2 !=0) else False #elite enemy when nb_eni ends by 5 only
    boss = True if (Eny.nb_eny %10 ==0 and Eny.nb_eny != 0) else False #boss enemy every 10 monsters
    choice = random.randint(0, len(eny_list)-1)
    try :
        eny = eny_list[choice]
    except IndexError :
        eny = '0'
    hp = int(random.randint(0,5)+ ply.lvl * 7)
    att = int(random.randint(0, 1)+ ply.lvl * 1.5)
    df = int(random.randint(0,1) + ply.lvl * 1.5)
    name = name_gen()
    if elite :
        hp += int(hp*0.5)
        att += int(att*0.5)
        df += int(df*0.5)
        name += ' Elite'
    elif boss :
        hp *=2
        att*=2
        df*=2
        name = 'Boss ' + name

    eny_gen = None
    match eny :
        case 'dog' :
            eny_gen = EnyRageDog(name, hp = hp, att = att, df = df)
        case 'oldman' :
            eny_gen = EnyOldMan(name, hp = hp, att = att, df = df)
        case '0' :
            eny_gen = EnyRageDog('Weakest Mouse', hp = 1, att = 1, df = 1)

    return eny_gen

def openning() :
    print("Welcome to the wonderful game RPG battle patata. You will explore an infinite dungeon full of dangers.\nDo you want to load a game, or start a new one ?")
    nprint("1 : Load a game\n2 : Start a new one")
    rep = input("--> ")
    while rep not in ['1', '2'] :
        rep = input("--> ")

    if rep == '2' :
        return chose_player()
    else :
        print("To load a game, the game file need to be a '.json'. You need to write exactly were this file is (the full path to it, including the file name and the .json extension), otherwise, it will bug and you'll juste start a new game.")
        file = input("--> ")

        try :
            file = file.replace('"','')
            ply = load_game(file)
            print("Character successfully loaded. Have fun :).")
            return ply

        except Exception as e :
            print(
                f"Sorry something went wrong. For now, no specific error management has been done, because I don't know what to expect.\nThis error is : {e}.")
            return chose_player()


def chose_player() :
    nprint("What is your name ?")
    name = input("--> ").strip()
    while len(name) == 0 :
        name = input("--> ").strip()
    print(f"\nHello {name}. What kind of player are you ?\n")
    nprint(f"  1 : {Baker.definition}\n  2 : {NarcissicPerverse.definition}\n  3 : {Gambler.definition}\n")
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
    os.system('cls' if os.name == 'nt' else 'clear')

def enemy_encounter(eny) :
    story = ["After several meters in the dungeon, you meet ","You open a door and then... ", "You smell something strange. It's ", "You hear something behind you. You just have time to pivot to see "]
    num = random.randint(0, len(story)-1)
    rprint(f"{story[num]}{eny.name}! \nIt can be defined by : {eny.definition} You have to fight for your life !")
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
                return Eatable('Adaptive Health potion', attribut ='adaptive', hp = 1)
            case 3 :
                return Eatable('Mana potion', mana=mana)
            case 4 :
                return Eatable('Adaptive Mana potion', attribut='adaptive', mana=1)
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
    nprint("You can let it alone (1), or open it (2).")
    op = input("--> ")
    while op not in ['1', '2'] :
        op = input("--> ")
    if op == '1' : return print("You go ahead in the dungeon without touching the chest.")
    print("You try to open it...")
    inside = ply.dice()
    if inside == 1 :
        hp = int(ply.maxhp*0.3)
        rprint(f"It was trapped. You lose {ply.take_damage(hp)} hp.")
    elif inside == 2 :
        uprint(f"The chest is empty...")
    elif inside < 6 :
        it = item_generator(ply)
        uprint(f"A {it.name} was in the chest. It's now in your inventory")
        ply.add_item(it)
    else :
        it = item_generator(ply)
        it1 = item_generator(ply)
        uprint(f"Lucky day ! The chest was full of objects ! You found {it.name} and {it1.name} !")
        ply.add_item(it)
        ply.add_item(it1)

def fire_camp(ply) :
    print("You just arrived to a peacefull place in this horrible dungeon. You can get some rest and be healed by half of your total hp.")
    nprint("Do you want to take a nap ?\n1 : yes\n2 : no ! I'm not a child.\n3 : I prefer to save the game !")
    heal = input("--> ")
    while heal not in ['1', '2', '3'] :
        heal = input("--> ")

    match heal :
        case '2' :
            return print("Ok ok, no need to shout out... So, you can continue.")
        case '1' :
            ply.hp += int(ply.maxhp/2)
            if ply.hp > ply.maxhp : ply.hp = ply.maxhp
            ply.mana += int(ply.maxma/2)
            if ply.mana > ply.maxma : ply.mana = ply.maxma
            uprint(f"You rested sucessfully. You feel better : {ply.hp}/{ply.maxhp} hp, {ply.mana}/{ply.maxma} mana.")
        case '3' :
            try :
                file = "save/" + ply.name + ".json"
                if not exists("save"):
                    os.mkdir("save")
                ok = save_game(ply, file)
                if ok : print("Game successfully saved. You can continue !")
            except Exception as e :
                print(f"Sorry smt went wrong. For now, no specific error management has been done, because I don't know what to expect.\nThis error is : {e}.")
        case _ :
            return "It seems something went wrong, so you just continue your adventure in the dungeon."


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