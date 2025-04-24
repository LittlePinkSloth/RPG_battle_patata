from rpg_battle_patata.game import language_manager

def main() :
    lang = language_manager.chose_langage()
    language_manager.load_langage(lang)
    from .main import start_game
    start_game()


if __name__ == "__main__":
    main()
