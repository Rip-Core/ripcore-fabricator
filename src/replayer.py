from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
import keyboard
from Replayer.recap import Recap
from configparser import ConfigParser


class MyBot(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.replayer = None

    def initialize_agent(self):
        self.replayer = Recap()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """
        controls = SimpleControllerState()

        if keyboard.is_pressed("-"):
            self.replayer.init()
            self.replayer.replayer(self.set_game_state)
        self.check_file()

        return controls

    def check_file(self):
        config = ConfigParser()
        config.read("src/config.ini")
        if config["REPLAYER"]["save_as"]:
            self.replayer.save_pack(config["REPLAYER"]["save_as"])
