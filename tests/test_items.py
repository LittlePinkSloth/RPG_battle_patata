import unittest
from rpg_battle_patata.game import language_manager
language_manager.load_langage('rpg_battle_patata/data/text_english.json')
from rpg_battle_patata.entities.items import Eatable, Wearable, AntiStatus


class TestItems(unittest.TestCase):
    def test_eatable_use(self):
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
        item = AntiStatus('Antidote')
        class DummyPlayer:
            hp = 50
            maxhp = 100
            mana = 0
            maxma = 0
            att = 10
            df = 0
            status = []
            def cure_status(self, stat):
                i = self.status.index(stat)
                del self.status[i]

        class DummyStatus :
            name = 'gros poison'
            status = 'poison'
            reversible = False
            applied = 0
        status = DummyStatus()
        player = DummyPlayer()
        player.status.append(status)
        self.assertEqual(player.status[0].status, 'poison')
        item.use(player)
        self.assertEqual(len(player.status), 0)