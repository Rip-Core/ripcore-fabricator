from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
import keyboard
from Replayer.recap import Recap
from rlbot.utils.game_state_util import BallState, GameState, CarState, Rotator, Physics, Vector3
import time
import pickle


class MyBot(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.replayer = None
        self.toggle_replay = False

    def initialize_agent(self):
        self.replayer = Recap()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """
        controls = SimpleControllerState()

        if keyboard.is_pressed("-"):
            if self.toggle_replay:
                self.toggle_replay = False
            else:
                self.toggle_replay = True

        if self.toggle_replay:
            self.replayer.init()
            self.replayer.replayer(self.set_game_state)

        return controls
