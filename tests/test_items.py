import unittest, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RPG_battle_patata.entities.items import Eatable, Wearable, AntiStatus
from test_characters import funcname

class TestItems(unittest.TestCase):

    def test_eatable_use(self):
        funcname("test_eatable_use")
        item = Eatable("Potion", hp=20, mana=10)
        class DummyPlayer:
            hp = 50
            maxhp = 100
            mana = 5
            maxma = 50
            att = 0
            df = 0

        player = DummyPlayer()
        item.use(player)
        self.assertEqual(player.hp, 70)
        self.assertEqual(player.mana, 15)

    def test_wearable_toggle(self):
        funcname("test_wearable_toggle")
        item = Wearable(hp=10, att=5)
        class DummyPlayer:
            hp = 50
            maxhp = 100
            mana = 0
            maxma = 0
            att = 10
            df = 0

        player = DummyPlayer()
        item.use(player)
        self.assertTrue(item.attribut)
        self.assertEqual(player.hp, 60)
        self.assertEqual(player.maxhp, 110)
        self.assertEqual(player.att, 15)

        item.use(player)
        self.assertFalse(item.attribut)
        self.assertEqual(player.hp, 50)
        self.assertEqual(player.maxhp, 100)
        self.assertEqual(player.att, 10)

    def test_antistatus(self):
        funcname("test_antistatus")
        item = AntiStatus('Antidote')
        class DummyPlayer:
            hp = 50
            maxhp = 100
            mana = 0
            maxma = 0
            att = 10
            df = 0
            status = 'poison'

        player = DummyPlayer()
        self.assertEqual(player.status, 'poison')
        item.use(player)
        self.assertFalse(player.status)