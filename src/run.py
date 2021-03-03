if __name__ == "__main__":
    from rlbot.setup_manager import SetupManager

    manager = SetupManager()
    manager.early_start_seconds = 5
    manager.connect_to_game()
    manager.game_interface.load_interface(
        wants_quick_chat=False, wants_game_messages=False, wants_ball_predictions=False)
    manager.load_config(config_location="src/match.cfg")
    manager.launch_early_start_bot_processes()
    manager.start_match()
    manager.launch_bot_processes()
    manager.infinite_loop()
