from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
import keyboard
from Replayer.recap import Recap
from configparser import ConfigParser


class MyBot(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.replayer = None
        self.running = False
        self.Id = 0
        if(len(self.name.split('('))>1):
            self.Id= int(self.name.split('(')[1].split(')')[0])-1
        
    def initialize_agent(self):
        self.replayer = Recap()
        self.replayer.init()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """
 
            # import time
            # time.sleep(1 )

        controls = SimpleControllerState()

        if keyboard.is_pressed("-"):
            self.running = True
        if keyboard.is_pressed("+"):
            self.running = False
            self.replayer.load = False
            self.replayer.tick_count = 0

        if self.running:
            self.replayer.load = True
            self.replayer.replayer(self.set_game_state, self.Id)
        self.check_file()

        return controls

    def check_file(self):
        config = ConfigParser()
        config.read("src/config.ini")
        if config["REPLAYER"]["save_as"]:
            self.replayer.save_pack(config["REPLAYER"]["save_as"])