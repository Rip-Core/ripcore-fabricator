import configparser
import pickle
from rlbot.utils.game_state_util import BallState, GameState, CarState, Rotator, Physics, Vector3
import time
import keyboard
import sys


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
        self.bot_index = None

    def init(self):
        config = configparser.ConfigParser()
        config.read("src/config.ini")
        self.file = config["REPLAYER"]["file"]
        self.start_time = float(config["REPLAYER"]["start_time"])
        self.end_time = float(config["REPLAYER"]["end_time"])
        self.load = False
        self.players_index = []
        self.create_pack.clear()
        self.seventh_is_human = False
        self.state_list = []
        self.tick_count = 0
        self.tick_count = 0
        with open(f"src/Snapshot/dumper/{self.file}", "rb") as testi:
            self.packet = pickle.load(testi)
        self.num_cars = self.packet[len(self.packet) - 1].num_cars
        self.pack_start = self.packet[0].game_info.seconds_elapsed
        self.replay_start = self.pack_start + self.start_time
        self.replay_stop = self.pack_start + self.end_time
        index = None
        for car in list(self.packet[0].game_cars):
            if car.is_bot:
                index = list(self.packet[0].game_cars).index(car)
                break
        if index is not None:
            if len(self.packet[0].game_cars) > 6 and self.num_cars > 6:
                if not self.packet[0].game_cars[6].is_bot:
                    self.seventh_is_human = True
        for ind, paks in enumerate(self.packet):
            if float("%.1f" % paks.game_info.seconds_elapsed) == float("%.1f" % self.replay_start):
                self.start_index = ind
            if float("%.1f" % paks.game_info.seconds_elapsed) == float("%.1f" % self.replay_stop):
                self.end_index = ind
        for pic in self.packet[self.start_index:self.end_index]:
            tmp_state = GameState.create_from_gametickpacket(pic)
            if self.seventh_is_human:
                tmp_state.cars[index], tmp_state.cars[6] = tmp_state.cars[6], tmp_state.cars[index]
            self.state_list.append(tmp_state)


    def replayer(self, set_game_state, id):

            # print(index)

            # for pack in self.packet:
            #     for ind, bot in enumerate(pack.game_cars):
            #         if bot.is_bot:
            #             self.bot_index = ind
            # for ind in range(self.num_cars):
            #     if ind != self.bot_index:
            # self.players_index.append(ind)


        if self.load:
            # print(self.tick_count)
            # print(self.state_list)
            if self.tick_count +1 > len(self.state_list):
                self.load=False
                return;
            state = self.state_list[self.tick_count]
            # for index in range(self.num_cars):
            #     if index != self.bot_index:
            if keyboard.is_pressed("+"):
                self.load = False
                self.tick_count  = 0
                self.init()
                return

            # print(state.cars, "!2222222222222222")
            # print(index)
            # # print("NUMBER OF CARS ",)
            # if index is not None:
            #     if self.seventh_is_human:
            #         # print(self.seventh_is_human)
            #         state.cars[index], state.cars[6] = state.cars[6], state.cars[index]
            #     else:
            #         del state.cars[index]
                # print("REMOVED BOT CAR!")
            self.create_pack.append(state)
            # if(id==index):
                # print("ID is ", id)
                # break
            # print(state.cars, "!111111111111111111111")
            if(id>min(self.num_cars, len(state.cars))-1):
                # print(self.num_cars)
                # print(id, "")
                # return
                return
            else:
                # print(id, self.num_cars, len(state.cars))
                carsta0 = CarState(physics=state.cars[id].physics, boost_amount = state.cars[id].boost_amount)

            if(id==0):
                ballsta = BallState(physics=state.ball.physics)

                gamesta = GameState(ball=ballsta, cars={
                                    id: carsta0})
            else:
                gamesta = GameState(cars={id: carsta0})

            set_game_state(game_state=gamesta)
            # time.sleep(0.016) #0.0078125 both are almost close (1/60-1/120) or 1/64-1/128

            self.tick_count += 1
            self.load=False


    def save_pack(self, name):
        with open(f"{name}", "wb") as trapacks:
            pickle.dump(self.create_pack, trapacks)
        self.create_pack.clear()
        config = configparser.ConfigParser()
        config.read("src/config.ini")
        config["REPLAYER"]["save_as"] = ""
        with open("src/config.ini", "w") as cfg:
            config.write(cfg)