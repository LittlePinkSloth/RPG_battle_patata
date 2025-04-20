import unittest, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RPG_battle_patata.game.utils import save_game, load_datas
from test_characters import funcname

class TestSaveGame(unittest.TestCase):

    def test_save_and_load(self):
        funcname("test_save_and_load")
        data = {"name": "Bob", "level": 2}
        save_game(data, "test_save.json")
        loaded = load_datas("test_save.json")
        self.assertEqual(data, loaded)
        os.remove("test_save.json")