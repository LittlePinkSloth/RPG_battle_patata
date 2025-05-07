import unittest
from rpg_battle_patata.entities.characters import Player

class TestCharacters(unittest.TestCase):
    def test_status_effect(self):
        class DummyStatus:
            name = 'poison'
            effect = "hp"
            rate = -0.5
            reversible = False
            applied = 5

        player = Player('Bob')
        status = DummyStatus()
        player.set_status(status)
        self.assertIn(status, player.status)
        value = player.match_status_effect(status.effect, status.rate)
        self.assertGreater(player.maxhp, player.hp)
        self.assertEqual(player.hp - player.maxhp, value)
        player.cure_status(status)
        self.assertNotIn(status, player.status)

    def test_player_gain_xp_and_level_up(self):
        class DummyEny :
            maxhp = 9


        player = Player("Bob", maxhp=0, maxma=0, att=0, df=0)
        player.exp = 5
        player.lvl = 1
        player.gain_xp(DummyEny())
        self.assertEqual(player.lvl, 2)
        self.assertEqual(player.exp, 1)
        self.assertGreater(player.hp, 0)
        self.assertGreater(player.mana, 0)
        self.assertGreater(player.att, 0)
        self.assertGreater(player.df, 0)

    def test_inventory_use_item(self):
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

    def test_to_from_dict(self):
        player = Player('Bob')
        plydict = player.to_dict()
        player2 = Player.from_dict(plydict)
        ply2dict = player2.to_dict()

        self.assertEqual(plydict, ply2dict)

