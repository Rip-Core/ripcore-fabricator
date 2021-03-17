import configparser
import pickle
from rlbot.utils.game_state_util import BallState, GameState, CarState, Rotator, Physics, Vector3
import time
import keyboard


class Recap:
    def __init__(self):
        self.file = None
        self.start_time = 0
        self.end_time = 0
        self.pack_start = None
        self.pack_end = None
        self.replay_start = 0
        self.replay_stop = 0
        self.packet = None
        self.start_index = 0
        self.end_index = 0
        self.load = False
        self.num_cars = None
        self.create_pack = []

    def init(self):
        config = configparser.ConfigParser()
        config.read("src/config.ini")
        self.file = config["REPLAYER"]["file"]
        self.start_time = float(config["REPLAYER"]["start_time"])
        self.end_time = float(config["REPLAYER"]["end_time"])
        self.load = False

    def replayer(self, set_game_state):
        if not self.load:
            with open(f"src/Snapshot/dumper/{self.file}", "rb") as testi:
                self.packet = pickle.load(testi)
            self.num_cars = self.packet[len(self.packet) - 1].num_cars
            self.pack_start = self.packet[0].game_info.seconds_elapsed
            self.replay_start = self.pack_start + self.start_time
            self.replay_stop = self.pack_start + self.end_time
            for ind, paks in enumerate(self.packet):
                if float("%.1f" % paks.game_info.seconds_elapsed) == float("%.1f" % self.replay_start):
                    self.start_index = ind
                if float("%.1f" % paks.game_info.seconds_elapsed) == float("%.1f" % self.replay_stop):
                    self.end_index = ind
            self.load = True
        for pic in self.packet[self.start_index:self.end_index]:
            if keyboard.is_pressed("+"):
                break
            state = GameState.create_from_gametickpacket(pic)
            self.create_pack.append(state)
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

    def save_pack(self, name):
        with open(f"{name}", "wb") as trapacks:
            pickle.dump(self.create_pack, trapacks)
        self.create_pack.clear()
        config = configparser.ConfigParser()
        config.read("src/config.ini")
        config["REPLAYER"]["save_as"] = ""
        with open("src/config.ini", "w") as cfg:
            config.write(cfg)
