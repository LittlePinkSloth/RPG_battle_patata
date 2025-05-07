import unittest, os
from rpg_battle_patata.game.utils import save_game, load_datas

class TestSaveGame(unittest.TestCase):
    def test_save_and_load(self):
        data = {"name": "Bob", "level": 2}
        save_game(data, "test_save.json")
        loaded = load_datas("test_save.json")
        self.assertEqual(data, loaded)
        os.remove("test_save.json")