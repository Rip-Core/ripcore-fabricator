from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
import keyboard
from Replayer.recap import Recap


class MyBot(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.replayer = None
        # self.counter = 3
        # self.load = False

    def initialize_agent(self):
        self.replayer = Recap()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """
        controls = SimpleControllerState()

        if keyboard.is_pressed("-"):
            # self.start = False
            # self.counter = 3
            # self.renderer.begin_rendering()
            self.replayer.init()
            # self.renderer.draw_string_2d(
            #     20, 500, 2, 2, count_text, self.renderer.white())
            # self.counter -= 1
            # if self.counter == 0:
            #     self.start = True
            # self.renderer.end_rendering()
            # if self.start:
            self.replayer.replayer(self.set_game_state)

        return controls
