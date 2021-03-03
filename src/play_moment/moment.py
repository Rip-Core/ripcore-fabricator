from rlbot.utils.game_state_util import GameState, BallState, CarState, GameInfoState
import pickle
import json


class Moment:
    def __init__(self):
        self.packet = []
        self.num_cars = None
        self.starting_time = None
        self.found_time = None
        self.starting_state = None
        self.game_state = None
        self.car_state = None
        self.ball_state = None
        self.game_info_state = None
        self.current_goal = 0
        self.current_save = 0
        self.found_score = False
        self.found_save = False
        self.snap_count = 0
        self.car_index = None

    def init_count(self):
        with open("src/Snapshot/count.json", "r") as cc:
            count = json.load(cc)["snap_count"]
            if count:
                self.snap_count = count
            else:
                self.snap_count = 0

    def load_packet(self) -> bool:
        try:
            with open("src/Snapshot/dumper/snapshot#{}.pickle".format(self.snap_count), "rb") as fp:
                self.packet = pickle.load(fp)
            self.num_cars = self.packet[len(self.packet) - 1].num_cars
            self.check_for_score()
            self.check_for_save()
            if self.found_score or self.found_save:
                for key, buffer in enumerate(self.packet):
                    if round(buffer.game_info.seconds_elapsed) == round(self.starting_time):
                        self.starting_state = buffer
                return True
            return False
        except Exception as e:
            print(e)

    def get_state(self):
        try:
            self.game_state = GameState.create_from_gametickpacket(
                self.starting_state)
            self.car_state = self.game_state.cars[self.car_index].__dict__
            self.ball_state = self.game_state.ball.__dict__
            self.game_info_state = self.game_state.game_info
        except Exception as e:
            print(e)

    def load_state(self) -> GameState:
        try:
            car_state = CarState(
                physics=self.car_state["physics"], boost_amount=self.car_state["boost_amount"])
            ball_state = BallState(physics=self.ball_state["physics"])
            game_info_state = GameInfoState(self.game_info_state)

            game_state = GameState(ball=ball_state, cars={
                self.car_index: car_state}, game_info=game_info_state)

            with open(f"src/Snapshot/training_pack/test#{self.snap_count}.pack", "wb") as gs:
                pickle.dump(game_state, gs)
            return game_state
        except Exception as e:
            print(e)

    def check_for_score(self):
        for buffer in self.packet:
            for index in range(self.num_cars):
                if buffer.game_cars[index].score_info.goals > self.current_goal:
                    if not buffer.game_cars[index].is_bot:
                        self.current_goal = buffer.game_cars[index].score_info.goals
                        self.found_time = buffer.game_info.seconds_elapsed
                        self.starting_time = self.found_time - 3
                        self.car_index = index
                        self.found_score = True

    def check_for_save(self):
        if self.found_score:
            return
        for buffer in self.packet:
            for index in range(self.num_cars):
                if buffer.game_cars[index].score_info.saves > self.current_save:
                    if not buffer.game_cars[index].is_bot:
                        self.current_save = buffer.game_cars[index].score_info.saves
                        self.found_time = buffer.game_info.seconds_elapsed
                        self.starting_time = self.found_time - 6
                        self.car_index = index
                        self.found_save = True
