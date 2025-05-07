from rpg_battle_patata.entities.characters import CHARACTER_CLASSES
from rpg_battle_patata.entities.items import Wearable
from rpg_battle_patata.entities.rpg_exceptions import DeadCharacter
from rpg_battle_patata.game.events import chest, rest, enemy_generator, enemy_encounter, generate_event_type, \
    place_generator
from rpg_battle_patata.game.language_manager import get_dict
import random

class GameManager:
    def __init__(self, player = None):
        self.player = player
        self.enemy = None
        self.turn_order = []
        self.step_in_turn = 0
        self.last_action_result = []
        self.game_over = False
        self.victory = False
        self.messages = []
        self.finish_event = False
        self.equiped_item = 0 if not self.player else len(self.player.equipment)
        self.unequiped_item = 0 if not self.player else len([it for it in self.player.inventory if isinstance(it, Wearable)])
        self.consumable_item = 0 if not self.player else len([it for it in self.player.inventory if not isinstance(it, Wearable)])

    def set_player(self, class_name : str, player_name : str):
        self.player = CHARACTER_CLASSES[class_name](player_name)
        """self.player.maxhp = 2000
        self.player.hp = 2000
        self.player.df = 100
        self.player.att = 200
        self.player.lvl = 5"""
        self.set_enemy()

    def set_enemy(self):
        self.enemy = enemy_generator(self.player)[0]
        self.messages.append(enemy_encounter(self.enemy))
        self.start_new_turn()

    def start_new_turn(self):
        self.turn_order = random.sample(['enemy', 'player'], k=2)
        self.step_in_turn = 0
        try :
            status = self.player.apply_all_status()[0]
            if status :
                self.last_action_result.append(status)
        except DeadCharacter as dead:
            self.victory = False
            self.game_over = True
            self.last_action_result.append(dead.__str__())

    def next_turn_action(self, player_action=None):
        actor = self.turn_order[self.step_in_turn]
        result = ''
        try :
            if actor == 'enemy':
                result = self.enemy.myturn(self.player)
                if isinstance(result, list) :
                    for txt in result :
                        self.last_action_result.append(txt)
                else :
                    self.last_action_result.append(result)
                self.step_in_turn += 1
                self.player.is_alive()

            elif actor == 'player' and player_action:
                if player_action == 'attack':
                    result = self.player.attack_target(self.enemy)[0]
                elif player_action == 'special':
                    result = self.player.special_attack(self.enemy)[0]
                self.last_action_result.append(result)
                self.step_in_turn += 1
                msg = self.enemy.is_alive()
                if isinstance(msg, str) : self.last_action_result.append(msg)
        except DeadCharacter as dead:
            if self.enemy.name in dead.__str__():
                self.victory = True
                self.game_over = True
                self.last_action_result.append(self.player.gain_xp(self.enemy))
            else:
                self.victory = False
                self.game_over = True
                self.last_action_result.append(dead.__str__())

        if self.step_in_turn >= 2:
            if not self.game_over:
                self.start_new_turn()

    def event_generator(self):
        event_type = generate_event_type(self.player)['event']
        event_table = {"chest" : self.resolve_chest_event, "fire_camp" : self.resolve_firecamp_event, "enemy_generator" : self.set_enemy, "magic_places" :self.resolve_magicplace_event}

        if event_type == "fire_camp" :
            return 'firecamp'
        elif event_type == "chest" :
            return 'chest'
        elif event_type == "magic_places" :
            return 'magicplace'
        else :
            event_table[event_type]()
            return 'battle'

    def resolve_chest_event(self, player_action = None):
        storytelling = get_dict("storytelling")
        events_dict = get_dict("events_dict")
        webapp_dict = get_dict("webapp_dict")
        if player_action :
            self.finish_event = True
            if player_action == 'open' :
                try :
                    self.last_action_result.append(chest(self.player)[0])
                    self.player.is_alive()
                except DeadCharacter as dead :
                    self.victory = False
                    self.game_over = True
                    self.last_action_result.append(dead.__str__())

            else :
                self.last_action_result.append(events_dict["chest.no"])

        else :
            ns = random.randint(0, len(storytelling["chest_discovery"]) - 1)
            message = storytelling["chest_discovery"][ns]
            self.messages.append(message)
            self.messages.append(webapp_dict["resolve_chest_event.open"])

    def player_use_item(self, itid : int):
        for it in self.player.inventory:
            if it.id == itid:
                self.last_action_result.append(self.player.use_item(it))

    def player_wearable(self, action:str, itid : int):
        if action == "equip" :
            for it in self.player.inventory :
                if it.id == itid :
                    self.last_action_result.append(self.player.equip_wearable(it))
                    self.equiped_item += 1
                    self.unequiped_item -= 1
        elif action == "unequip" :
            for it in self.player.equipment :
                if it.id == itid :
                    self.last_action_result.append(self.player.unequip_wearable(it))
                    self.equiped_item -= 1
                    self.unequiped_item += 1

    def resolve_firecamp_event(self, player_action = None):
        storytelling = get_dict("storytelling")
        events_dict = get_dict("events_dict")
        if player_action :
            self.finish_event = True
            if player_action == 'rest' :
                self.last_action_result.append(rest(self.player)[0])
            else :
                self.last_action_result.append(events_dict["fire_camp.no"])

        else :
            if len(self.messages) == 0 :
                ns = random.randint(0, len(storytelling["safe_room"]) - 1)
                message = storytelling["safe_room"][ns] + events_dict["fire_camp.nap"]
                self.messages.append(message)

    def resolve_magicplace_event(self, player_action = None):
        storytelling = get_dict("storytelling")
        events_dict = get_dict("events_dict")
        if player_action:
            self.finish_event = True
            if player_action == 'action':
                message = place_generator(self.player)[0]
                self.last_action_result.append(message)
            else:
                self.last_action_result.append(events_dict["magic_places.no"])
        else:
            self.messages.append(random.choices(storytelling['magic_place'])[0])

    def restart_game(self):
        self.__init__(player = self.player)
