import unittest
from rpg_battle_patata.game import language_manager
language_manager.load_langage('rpg_battle_patata/data/text_english.json')
from rpg_battle_patata.entities.characters import Player

def funcname(name) :
    return print(f"--> Current test : {name}")

class TestCharacters(unittest.TestCase):

    def test_player_gain_xp_and_level_up(self):
        funcname('test_player_gain_xp_and_level_up')
        player = Player("Bob", maxhp=0, maxma=0, att=0, df=0)
        player.exp = 5
        player.lvl = 1
        player.gain_xp(6)
        self.assertEqual(player.lvl, 2)
        self.assertEqual(player.exp, 1)
        self.assertGreater(player.hp, 0)
        self.assertGreater(player.mana, 0)
        self.assertGreater(player.att, 0)
        self.assertGreater(player.df, 0)

    def test_inventory_use_item(self):
        funcname("test_inventory_use_item")
        player = Player("Bob")
        class DummyItem :
            name = "Test"
            def use(self, ply):
                pass

        item = DummyItem()

        player.add_item(item)
        self.assertEqual(len(player.inventory), 1)

        player.use_item(item)
        self.assertEqual(len(player.inventory), 0)

    def test_equip_unequip_wearable(self):
        funcname("test_equip_unequip_wearable")
        player = Player("Bob")
        class DummyItem :
            name = "Test"
            def use(self, ply):
                pass

        item = DummyItem()

        player.add_item(item)
        player.equip_wearable(item)
        self.assertEqual(len(player.inventory), 0)
        self.assertEqual(len(player.equipment), 1)

        player.unequip_wearable(item)
        self.assertEqual(len(player.inventory), 1)
        self.assertEqual(len(player.equipment), 0)

    """def test_change_wearable(self):
        funcname("test_change_wearable")
        player = Player("Bob")
        class DummyItem:
            def __init__(self, name):
                self.name = name

            def use(self, ply):
                pass

        item1 = DummyItem('Test1')
        item2 = DummyItem('Test2')

        player.add_item(item1)
        player.add_item(item2)
        player.equip_wearable(item1)

        self.assertEqual(player.equipment[0], item1)
        self.assertNotIn(item1, player.inventory)
        self.assertIn(item2, player.inventory)

        player.change_wearable(item2)
        self.assertEqual(len(player.inventory), 1)
        self.assertEqual(len(player.equipment), 1)

        self.assertNotIn(item1, player.equipment)
        self.assertIn(item2, player.equipment)"""

    def test_to_from_dict(self):
        funcname("test_to_from_dict")
        player = Player('Bob')
        plydict = player.to_dict()
        player2 = Player.from_dict(plydict)
        ply2dict = player2.to_dict()

        self.assertEqual(plydict, ply2dict)

