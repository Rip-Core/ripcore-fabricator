import configparser
import pickle
from rlbot.utils.game_state_util import BallState, GameState, CarState, Rotator, Physics, Vector3
import time


class Recap:
    def __init__(self):
        self.file = None
        self.start_time = 10

    def init(self):
        config = configparser.ConfigParser()
        config.read("src/config.ini")
        self.file = config["REPLAYER"]["file"]
        self.start_time = float(config["REPLAYER"]["start_time"])

    def replayer(self, set_game_state):
        with open("src/Snapshot/dumper/snapshot#127.pickle", "rb") as testi:
            packi = pickle.load(testi)
        # starting_state = GameState.create_from_gametickpacket(
        #     packi[0])
        # carsta0 = CarState(
        #     physics=starting_state.cars[1].physics, boost_amount=starting_state.boosts)
        # carsta1 = CarState(
        #     physics=starting_state.cars[2].physics, boost_amount=starting_state.boosts)
        # carsta2 = CarState(
        #     physics=starting_state.cars[3].physics, boost_amount=starting_state.boosts)
        # starting_gamestate = GameState(ball=starting_state.ball, cars={
        #     0: carsta0, 1: carsta1, 2: carsta2})
        # self.set_game_state(starting_gamestate)

        for pic in packi:
            state = GameState.create_from_gametickpacket(pic)
            carsta0 = CarState(
                physics=state.cars[0].physics)
            carsta1 = CarState(
                physics=state.cars[1].physics)
            carsta2 = CarState(
                physics=state.cars[2].physics)
            carsta3 = CarState(
                physics=state.cars[3].physics)
            carsta4 = CarState(
                physics=state.cars[4].physics)
            carsta5 = CarState(
                physics=state.cars[5].physics)
            ballsta = BallState(physics=state.ball.physics)

            gamesta = GameState(ball=ballsta, cars={
                0: carsta0, 1: carsta1, 2: carsta2, 3: carsta3, 4: carsta4, 5: carsta5})
            set_game_state(game_state=gamesta)
            time.sleep(0.1)
