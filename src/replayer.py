from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.game_state_util import BallState, GameState, CarState, Rotator, Physics, Vector3
import keyboard
import pickle
import time


class MyBot(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)

    def initialize_agent(self):
        self.replay = False

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """
        controls = SimpleControllerState()

        if keyboard.is_pressed("-"):
            with open("src/Snapshot/dumper/snapshot#74.pickle", "rb") as testi:
                packi = pickle.load(testi)
            starting_state = GameState.create_from_gametickpacket(
                packi[140])
            carsta0 = CarState(
                physics=starting_state.cars[1].physics, boost_amount=starting_state.boosts)
            carsta1 = CarState(
                physics=starting_state.cars[2].physics, boost_amount=starting_state.boosts)
            carsta2 = CarState(
                physics=starting_state.cars[3].physics, boost_amount=starting_state.boosts)
            starting_gamestate = GameState(ball=starting_state.ball, cars={
                0: carsta0, 1: carsta1, 2: carsta2})
            self.set_game_state(starting_gamestate)

            for pic in packi[140:]:
                state = GameState.create_from_gametickpacket(pic)
                # carsta0 = CarState(
                #     physics=state.cars[0].physics)
                carsta1 = CarState(
                    physics=state.cars[1].physics)
                carsta2 = CarState(
                    physics=state.cars[2].physics)
                # ballsta = BallState(physics=state.ball.physics)

                gamesta = GameState(cars={
                    0: carsta1, 1: carsta2})
                self.set_game_state(game_state=gamesta)
                time.sleep(0.1)

        return controls
