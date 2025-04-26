import unittest
from rpg_battle_patata.game import language_manager
language_manager.load_langage('rpg_battle_patata/data/text_english.json')
from rpg_battle_patata.entities.status import Status

class TestStatus(unittest.TestCase) :
    def test_name_effect_rate(self):
        status1 = Status('poison')
        status2 = Status('poison', strengh=2)
        status3 = Status('poison', strengh=0.5)
        self.assertEqual(status1.name, "poison")
        self.assertEqual(status2.name, "serious poison")
        self.assertEqual(status3.name, "slight poison")
        self.assertGreater(status3.rate, status1.rate)
        self.assertGreater(status1.rate, status2.rate)

        status4 = Status('in love')
        self.assertEqual(status4.buff, 1)

    def test_from_dict(self):
        status = Status('poison')

        dict1 = status.to_dict()
        status2 = Status.from_dict(dict1)
        dict2 = status2.to_dict()
        self.assertEqual(dict1, dict2)

    def test_effects(self):
        status = Status('poison', once = True)
        effect, rate = status.get_status_effect()
        self.assertEqual(effect, "hp")
        self.assertGreater(1, rate)
        status.apply_effect(10)
        effect, rate = status.get_status_effect()
        self.assertFalse(effect)
        self.assertFalse(rate)
        effect, value = status.reverse_effect()
        self.assertFalse(effect)
        self.assertFalse(value)

        status1 = Status('poison', reversible=True)
        status1.apply_effect(10)
        effect, value = status1.reverse_effect()
        self.assertEqual(effect, "hp")
        self.assertEqual(value, 10)